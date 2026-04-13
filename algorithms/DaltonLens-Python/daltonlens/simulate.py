from daltonlens import convert
from daltonlens.utils import array_to_C_decl, normalized

from collections import namedtuple

import logging
import math
import numpy as np
import sys

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# Module-level cached LMS model instances.
# WHY: LMSModel.__init__ calls np.linalg.inv twice; recomputing per call is wasteful.
_lms_cache: dict = {}

from enum import Enum
class Deficiency(Enum):
    PROTAN   = 0
    DEUTAN   = 1
    TRITAN   = 2
    ACHROMAT = 3  # Rod monochromacy (complete achromatopsia, all cones absent)
    BCM      = 4  # Blue-cone monochromacy (OPN1LW/OPN1MW absent; S-cones + rods only)

def name_of_deficiency(d: Deficiency):
    if d == Deficiency.PROTAN:   return "protan"
    if d == Deficiency.DEUTAN:   return "deutan"
    if d == Deficiency.TRITAN:   return "tritan"
    if d == Deficiency.ACHROMAT: return "achromat"
    if d == Deficiency.BCM:      return "bcm"
class Simulator (ABC):
    """Base class for all CVD simulators."""

    def __init__(self):
        self.dumpPrecomputedValues = False
        self.imageEncoding = convert.ImageEncoding.SRGB

    def simulate_cvd (self, image_srgb_uint8, deficiency: Deficiency, severity: float):
        """Simulate the appearance of an image for the given color vision deficiency

        Parameters
        ==========
        image_srgb_uint8 : array of shape (M,N,3) with dtype uint8
            The input sRGB image, with values in [0,255].

        deficiency: Deficiency
            The deficiency to simulate.

        severity: float
            The severity between 0 (normal vision) and 1 (complete dichromacy).

        Returns
        =======
        im : array of shape (M,N,3) with dtype uint8
            The simulated sRGB image with values in [0,255].

        Raises
        ======
        TypeError
            If image_srgb_uint8 is not a numpy array, or if deficiency is not a
            Deficiency enum member.
        ValueError
            If the image does not have shape (H, W, 3), if the dtype is not uint8,
            or if severity is outside [0.0, 1.0].
        """
        if not isinstance(image_srgb_uint8, np.ndarray):
            raise TypeError(
                f"image_srgb_uint8 must be a numpy ndarray, got {type(image_srgb_uint8).__name__}"
            )
        if image_srgb_uint8.dtype != np.uint8:
            raise ValueError(
                f"image_srgb_uint8 must have dtype uint8, got {image_srgb_uint8.dtype}"
            )
        if image_srgb_uint8.ndim != 3 or image_srgb_uint8.shape[2] != 3:
            raise ValueError(
                f"image_srgb_uint8 must have shape (H, W, 3), got {image_srgb_uint8.shape}"
            )
        if not isinstance(deficiency, Deficiency):
            raise TypeError(
                f"deficiency must be a Deficiency enum member, got {type(deficiency).__name__}"
            )
        if not (0.0 <= severity <= 1.0):
            raise ValueError(
                f"severity must be in [0.0, 1.0], got {severity}"
            )
        im_linear_rgb = convert.as_float32(image_srgb_uint8)        
        if (self.imageEncoding == convert.ImageEncoding.SRGB):
            im_linear_rgb = convert.linearRGB_from_sRGB(im_linear_rgb)
        elif (self.imageEncoding == convert.ImageEncoding.GAMMA_22):
            im_linear_rgb = convert.linearRGB_from_gamma22(im_linear_rgb)

        im_cvd_linear_rgb = self._simulate_cvd_linear_rgb(im_linear_rgb, deficiency, severity)
        
        if (self.imageEncoding == convert.ImageEncoding.SRGB):
            im_cvd_float = convert.sRGB_from_linearRGB(im_cvd_linear_rgb)
        elif (self.imageEncoding == convert.ImageEncoding.GAMMA_22):
            im_cvd_float = convert.gamma22_from_linearRGB(im_cvd_linear_rgb)
        else:
            im_cvd_float = im_cvd_linear_rgb
        return convert.as_uint8(im_cvd_float)

    @abstractmethod
    def _simulate_cvd_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        """All subclasses must implement this."""
        pass

class DichromacySimulator (Simulator):
    """Base class for CVD simulators that only support dichromacy
    
        Anomalous trichromacy will be implemented on top of the
        dichromacy simulator by linearly interpolating between the
        original image and the dichromat version. 
        
        This is not backed back a strong theory, but it works well in
        practice and is similar in spirit to the 
        'So that's what you see": building understanding with personalized
        simulations of colour vision deficiency'
        paper by D. Flatla and C. Gutwin, with the difference that they
        use a fixed step.
    """

    def _simulate_cvd_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        im_dichromacy = self._simulate_dichromacy_linear_rgb(image_linear_rgb_float32, deficiency)
        if severity < 0.99999:
            return im_dichromacy*severity + image_linear_rgb_float32*(1.0-severity)
        else:
            return im_dichromacy

    @abstractmethod
    def _simulate_dichromacy_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        pass

def plane_projection_matrix(plane_normal, deficiency: Deficiency):
    """Utility function for Vienot and Brettel.
    
    Given the projection plane normal, it returns the projection
    matrix along the deficiency axis that will project an LMS
    color to the plane. We don't need to take an origin since
    black (0,0,0) is always on the plane.
    """
    n = plane_normal
    # Projection along the L axis
    if deficiency == Deficiency.PROTAN:
        return np.array([
            [0., -n[1]/n[0], -n[2]/n[0]],
            [0, 1, 0],
            [0, 0, 1]
        ])
    # Projection along the M axis
    if deficiency == Deficiency.DEUTAN:
        return np.array([
            [1, 0, 0],
            [-n[0]/n[1], 0, -n[2]/n[1]],
            [0, 0, 1]
        ])
    # Projection along the S axis
    if deficiency == Deficiency.TRITAN:
        return np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-n[0]/n[2], -n[1]/n[2], 0]
        ])
    return None

def lms_confusion_axis(deficiency: Deficiency):
    """Return the LMS axis along which a dichromat will confuse the colors.
    """
    
    if deficiency == Deficiency.PROTAN: return np.array([1.0, 0.0, 0.0])
    if deficiency == Deficiency.DEUTAN: return np.array([0.0, 1.0, 0.0])
    if deficiency == Deficiency.TRITAN: return np.array([0.0, 0.0, 1.0])
    return None

class Simulator_Vienot1999 (DichromacySimulator):
    """Algorithm of (Vienot, Brettel & Mollon, 1999).

    'Digital video colourmaps for checking the legibility of displays by dichromats.'

    Projects LMS colors onto the dichromat confusion plane using a single
    projection matrix derived from the blue (475 nm) and yellow (575 nm) anchors.

    When to use
    -----------
    - Protanopia or deuteranopia at full severity (severity=1.0).
    - Fastest of the accurate methods; well-suited for batch processing.
    - Do NOT use for tritanopia -- use Simulator_Brettel1997 instead.

    Notes
    -----
    Anomalous trichromacy (severity < 1.0) is handled by the DichromacySimulator
    base class via linear interpolation with the original image. This is an
    approximation; use Simulator_Machado2009 for a more principled severity model.
    """

    def __init__(self, color_model: convert.LMSModel = convert.LMSModel_sRGB_SmithPokorny75()):
        super().__init__()
        self.color_model = color_model

    def _simulate_dichromacy_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency):
        self.lms_projection_matrix = None
        if deficiency == Deficiency.PROTAN or deficiency == Deficiency.DEUTAN:
            lms_blue = self.color_model.LMS_from_linearRGB @ np.array([0.0, 0.0, 1.0])
            lms_yellow = self.color_model.LMS_from_linearRGB @ np.array([1.0, 1.0, 0.0])
            v_blue = lms_blue # - lms_black which is ommitted since it's zero
            v_yellow = lms_yellow # - lms_black which is ommitted since it's zero

            # Deutan and Protan plane normal
            n = np.cross(v_yellow, v_blue)
            self.lms_projection_matrix = plane_projection_matrix(n, deficiency)
        else:
            # print ("WARNING: Viénot 1999 is not accurate for tritanopia. Use Brettel 1997 instead.")
            v_red = self.color_model.LMS_from_linearRGB @ np.array([1.0, 0.0, 0.0]) # - lms_black which is ommitted since it's zero
            v_cyan = self.color_model.LMS_from_linearRGB @ np.array([0.0, 1.0, 1.0]) # - lms_black which is ommitted since it's zero
            n = np.cross(v_cyan, v_red)
            self.lms_projection_matrix = plane_projection_matrix(n, Deficiency.TRITAN)

        # Save it for external inspection.
        self.cvd_linear_rgb = self.color_model.linearRGB_from_LMS @ self.lms_projection_matrix @ self.color_model.LMS_from_linearRGB

        if self.dumpPrecomputedValues:
            print (array_to_C_decl(f"vienot_{name_of_deficiency(deficiency)}_rgbCvd_from_rgb", self.cvd_linear_rgb))

        return convert.apply_color_matrix(image_linear_rgb_float32, self.cvd_linear_rgb)

class Simulator_Brettel1997 (DichromacySimulator):
    """Algorithm of (Brettel, Viénot & Mollon, 1997).
    'Computerized simulation of color appearance for dichromats'

    This model is a bit more complex than (Viénot & Brettel & Mollon, 1999)
    but it works well for tritanopia. It is also the most solid reference
    in the literature.
    """

    def __init__(self, 
                 color_model: convert.LMSModel = convert.LMSModel_sRGB_SmithPokorny75(),
                 use_vischeck_anchors=False,
                 use_white_as_neutral=True):
        """    
        Parameters
        ==========
        use_vischeck_anchors : Boolean
            If true, the 475, 575, 485 and 660nm
            anchors will be taken from Vischeck. Not sure how they were computed
            exactly, but this option is useful to have a comparison point with
            the battle-tested Vischeck.

        use_white_as_neutral: Boolean If true, RGB white will be used as the
            white point and will be the diagonal of the projection plane. In
            theory we should pick an equal illuminant (X=Y=Z in XYZ), but
            picking white is a reasonable approximation that increases the valid
            gamut. Indeed, using E means that more colors will get projected
            on the plane outside of the LMS parallelepiped and thus get clamped.

            Also pure RGB white (255,255,255) will not be left unchanged if we
            use the equal energy illuminant, which is a bit annoying.

            This is also the approximation made by Viénot, Brettel & Mollon 1999 
            'Digital video colourmaps for checking the legibility of displays by dichromats.'
        """
        
        super().__init__()
        self.use_vischeck_anchors = use_vischeck_anchors
        self.color_model = color_model
        self.use_white_as_neutral = use_white_as_neutral

    def _simulate_dichromacy_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency):
        if self.use_vischeck_anchors:
            # From GIMP vischeck implementation. They define them in lms, but
            # we converted them to XYZ using their lms2rgb matrix and XYZ_from_rgb
            # https://github.com/GNOME/gimp/blob/master/modules/display-filter-color-blind.c
            # lms_475 = np.array([0.08008, 0.1579, 0.5897])
            # lms_575 = np.array([0.9856, 0.7325, 0.001079])
            # lms_485 = np.array([0.1284, 0.2237, 0.3636])
            # lms_660 = np.array([0.0914, 0.007009, 0.0])
            xyz_475 = np.array([ 1.22694,  0.87814,  7.85903])
            xyz_575 = np.array([ 5.65322,  6.43625, -0.2219 ])
            xyz_485 = np.array([ 0.79132,  1.4793 ,  4.85354])
            xyz_660 = np.array([ 0.90089,  0.21688, -0.04599])
        else:
            # This is how these were computed. Saving the values to avoid a dependency.
            # pip install colour-science
            # from daltonlens import cmfs
            # xyz_475 = cmfs.wavelength_to_XYZ_JuddVos(475)
            # xyz_575 = cmfs.wavelength_to_XYZ_JuddVos(575)
            # xyz_485 = cmfs.wavelength_to_XYZ_JuddVos(485)
            if self.color_model.usesJuddVosXYZ:
                # xyz_660 = cmfs.wavelength_to_XYZ_JuddVos(660)
                xyz_475 = np.array([0.13287, 0.11284, 0.9422 ])
                xyz_575 = np.array([0.84394, 0.91558, 0.00197])
                xyz_485 = np.array([0.05699, 0.16987, 0.5864 ])
                xyz_660 = np.array([0.16161, 0.061  , 0.00001])
            else:
                # Values ignoring the Judd-Vos transform, for
                # historical comparisons
                xyz_475 = np.array([ 0.1421,  0.1126,  1.0419])
                xyz_575 = np.array([ 0.8425,  0.9154,  0.0018])
                xyz_485 = np.array([ 0.05795, 0.1693,  0.6162])
                xyz_660 = np.array([ 0.1649,  0.0610,  0.0000])

        # The equal-energy white point. By construction of CIE XYZ it has X=Y=Z.
        # The normalization does not matter to define the diagonal direction,
        # picking 0.8 to make it close to sRGB white.
        if self.use_white_as_neutral:
            lms_W = self.color_model.LMS_from_linearRGB @ np.array([1.0,1.0,1.0])
            lms_neutral = lms_W
        else:
            xyz_E = [0.8, 0.8, 0.8]
            rgb_E = self.color_model.linearRGB_from_XYZ @ xyz_E
            lms_E = self.color_model.LMS_from_XYZ @ xyz_E
            lms_neutral = lms_E

        def compute_matrices(lms_on_wing1, lms_on_wing2):
            n1 = np.cross(lms_neutral, lms_on_wing1) # first plane
            n2 = np.cross(lms_neutral, lms_on_wing2) # second plane
            n_sep_plane = np.cross(lms_neutral, lms_confusion_axis(deficiency)) # separation plane going through the diagonal
            # Swap the input so that wing1 is on the positive side of the separation plane
            if np.dot(n_sep_plane, lms_on_wing1) < 0:
                n1, n2 = n2, n1
                lms_on_wing1, lms_on_wing2 = lms_on_wing2, lms_on_wing1
            H1 = plane_projection_matrix(n1, deficiency)
            H2 = plane_projection_matrix(n2, deficiency)
            return (H1, H2, n_sep_plane)

        H1 = H2 = n_sep_plane = None
        if deficiency == Deficiency.PROTAN or deficiency == Deficiency.DEUTAN:
            lms_475 = self.color_model.LMS_from_XYZ @ xyz_475
            lms_575 = self.color_model.LMS_from_XYZ @ xyz_575
            H1, H2, n_sep_plane = compute_matrices(lms_475, lms_575)
        else:
            lms_485 = self.color_model.LMS_from_XYZ @ xyz_485
            lms_660 = self.color_model.LMS_from_XYZ @ xyz_660
            H1, H2, n_sep_plane = compute_matrices(lms_485, lms_660)

        if self.dumpPrecomputedValues:            
            self._dump_brettel_data (deficiency, H1, H2, n_sep_plane)

        im_lms = convert.apply_color_matrix(image_linear_rgb_float32, self.color_model.LMS_from_linearRGB)
        im_H1 = convert.apply_color_matrix(im_lms, H1)
        im_H2 = convert.apply_color_matrix(im_lms, H2)
        H2_indices = np.dot(im_lms, n_sep_plane) < 0

        # Start with H1, then overwrite the pixels that are closer to plane 2 with im_H2
        im_H = im_H1
        im_H[H2_indices] = im_H2[H2_indices]
        im_linear_rgb = convert.apply_color_matrix(im_H, self.color_model.linearRGB_from_LMS)
        return im_linear_rgb

    def _dump_brettel_data(self, deficiency, H1, H2, n_sep_plane):
        deficiency_name = name_of_deficiency(deficiency)

        print ("""
struct DLBrettel1997Params
{
    // Transformation using plane 1 == rgbFromLms . projection1 . lmsFromRgb
    float rgbCvdFromRgb_1[9];
    
    // Full transformation using plane 2 == rgbFromLms . projection2 . lmsFromRgb
    float rgbCvdFromRgb_2[9];

    // Normal of the separation plane to pick the right transform, already in the RGB space.
    // == normalInLms . lmsFromRgb
    float separationPlaneNormalInRgb[3];
};""")

        # Save it in case someone wants it.
        self.n_sep_plane = n_sep_plane
        self.H1 = H1
        self.H2 = H2
        
        self.n_sep_plane_rgb = np.dot(n_sep_plane, self.color_model.LMS_from_linearRGB)
        # rgbCvdFromRgb 1 and 2
        self.T1 = self.color_model.linearRGB_from_LMS @ H1 @ self.color_model.LMS_from_linearRGB
        self.T2 = self.color_model.linearRGB_from_LMS @ H2 @ self.color_model.LMS_from_linearRGB

        print (f"""
static struct DLBrettel1997Params brettel_{deficiency_name}_params = {{
    {{
        {self.T1[0,0]:.5f}, {self.T1[0,1]:.5f}, {self.T1[0,2]:.5f},
        {self.T1[1,0]:.5f}, {self.T1[1,1]:.5f}, {self.T1[1,2]:.5f},
        {self.T1[2,0]:.5f}, {self.T1[2,1]:.5f}, {self.T1[2,2]:.5f},
    }},
    {{
        {self.T2[0,0]:.5f}, {self.T2[0,1]:.5f}, {self.T2[0,2]:.5f},
        {self.T2[1,0]:.5f}, {self.T2[1,1]:.5f}, {self.T2[1,2]:.5f},
        {self.T2[2,0]:.5f}, {self.T2[2,1]:.5f}, {self.T2[2,2]:.5f},
    }},
    {{ {self.n_sep_plane_rgb[0]:.5f}, {self.n_sep_plane_rgb[1]:.5f}, {self.n_sep_plane_rgb[2]:.5f} }}
}};""")

class Simulator_Vischeck (Simulator_Brettel1997):
    """Emulates Vischeck, as implemented in GIMP.

    The Vischeck code is based on Brettel. The main differences are:
    - The LMS model being used
    - The anchor points (the 475 / 485 / 575 / 660nm wavelength)
    - Using RGB white as the neutral instead of an equal energy illuminant in XYZ
    """
    def __init__(self):
        super().__init__(convert.LMSModel_Vischeck_GIMP(),
                         use_vischeck_anchors=True,
                         use_white_as_neutral=True)

"""
From https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html#Reference
Converted to numpy array by https://github.com/colour-science/colour/blob/develop/colour/blindness/datasets/machado2010.py
The severity key goes from 0.0 to 1.0 with 0.1 steps, but here the index is multiplied by 10 to make it an integer.
"""
machado_2009_matrices = {
    Deficiency.PROTAN: {
        0: np.array([ [1.000000, 0.000000, -0.000000], [0.000000, 1.000000, 0.000000], [-0.000000, -0.000000, 1.000000] ]),
        1: np.array([ [0.856167, 0.182038, -0.038205], [0.029342, 0.955115, 0.015544], [-0.002880, -0.001563, 1.004443] ]),
        2: np.array([ [0.734766, 0.334872, -0.069637], [0.051840, 0.919198, 0.028963], [-0.004928, -0.004209, 1.009137] ]),
        3: np.array([ [0.630323, 0.465641, -0.095964], [0.069181, 0.890046, 0.040773], [-0.006308, -0.007724, 1.014032] ]),
        4: np.array([ [0.539009, 0.579343, -0.118352], [0.082546, 0.866121, 0.051332], [-0.007136, -0.011959, 1.019095] ]),
        5: np.array([ [0.458064, 0.679578, -0.137642], [0.092785, 0.846313, 0.060902], [-0.007494, -0.016807, 1.024301] ]),
        6: np.array([ [0.385450, 0.769005, -0.154455], [0.100526, 0.829802, 0.069673], [-0.007442, -0.022190, 1.029632] ]),
        7: np.array([ [0.319627, 0.849633, -0.169261], [0.106241, 0.815969, 0.077790], [-0.007025, -0.028051, 1.035076] ]),
        8: np.array([ [0.259411, 0.923008, -0.182420], [0.110296, 0.804340, 0.085364], [-0.006276, -0.034346, 1.040622] ]),
        9: np.array([ [0.203876, 0.990338, -0.194214], [0.112975, 0.794542, 0.092483], [-0.005222, -0.041043, 1.046265] ]),
        10: np.array([ [0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998] ])
    },

    Deficiency.DEUTAN: {
        0: np.array([ [1.000000, 0.000000, -0.000000], [0.000000, 1.000000, 0.000000], [-0.000000, -0.000000, 1.000000] ]),
        1: np.array([ [0.866435, 0.177704, -0.044139], [0.049567, 0.939063, 0.011370], [-0.003453, 0.007233, 0.996220] ]),
        2: np.array([ [0.760729, 0.319078, -0.079807], [0.090568, 0.889315, 0.020117], [-0.006027, 0.013325, 0.992702] ]),
        3: np.array([ [0.675425, 0.433850, -0.109275], [0.125303, 0.847755, 0.026942], [-0.007950, 0.018572, 0.989378] ]),
        4: np.array([ [0.605511, 0.528560, -0.134071], [0.155318, 0.812366, 0.032316], [-0.009376, 0.023176, 0.986200] ]),
        5: np.array([ [0.547494, 0.607765, -0.155259], [0.181692, 0.781742, 0.036566], [-0.010410, 0.027275, 0.983136] ]),
        6: np.array([ [0.498864, 0.674741, -0.173604], [0.205199, 0.754872, 0.039929], [-0.011131, 0.030969, 0.980162] ]),
        7: np.array([ [0.457771, 0.731899, -0.189670], [0.226409, 0.731012, 0.042579], [-0.011595, 0.034333, 0.977261] ]),
        8: np.array([ [0.422823, 0.781057, -0.203881], [0.245752, 0.709602, 0.044646], [-0.011843, 0.037423, 0.974421] ]),
        9: np.array([ [0.392952, 0.823610, -0.216562], [0.263559, 0.690210, 0.046232], [-0.011910, 0.040281, 0.971630] ]),
        10: np.array([ [0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881] ])
    },

    Deficiency.TRITAN: {
        0: np.array([ [1.000000, 0.000000, -0.000000],  [ 0.000000, 1.000000, 0.000000], [-0.000000, -0.000000, 1.000000] ]),
        1: np.array([ [0.926670, 0.092514, -0.019184],  [ 0.021191, 0.964503, 0.014306], [0.008437, 0.054813, 0.936750] ]),
        2: np.array([ [0.895720, 0.133330, -0.029050],  [ 0.029997, 0.945400, 0.024603], [0.013027, 0.104707, 0.882266] ]),
        3: np.array([ [0.905871, 0.127791, -0.033662],  [ 0.026856, 0.941251, 0.031893], [0.013410, 0.148296, 0.838294] ]),
        4: np.array([ [0.948035, 0.089490, -0.037526],  [ 0.014364, 0.946792, 0.038844], [0.010853, 0.193991, 0.795156] ]),
        5: np.array([ [1.017277, 0.027029, -0.044306],  [-0.006113, 0.958479, 0.047634], [0.006379, 0.248708, 0.744913] ]),
        6: np.array([ [1.104996, -0.046633, -0.058363], [-0.032137, 0.971635, 0.060503], [0.001336, 0.317922, 0.680742] ]),
        7: np.array([ [1.193214, -0.109812, -0.083402], [-0.058496, 0.979410, 0.079086], [-0.002346, 0.403492, 0.598854] ]),
        8: np.array([ [1.257728, -0.139648, -0.118081], [-0.078003, 0.975409, 0.102594], [-0.003316, 0.501214, 0.502102] ]),
        9: np.array([ [1.278864, -0.125333, -0.153531], [-0.084748, 0.957674, 0.127074], [-0.000989, 0.601151, 0.399838] ]),
        10: np.array([ [1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900] ])
    }
}
class Simulator_Machado2009 (Simulator):
    """The model proposed by (Machado, Oliveira & Fernandes, 2009).

    'A physiologically-based model for simulation of color vision deficiency'

    Simulates anomalous trichromacy (partial severity) by shifting the peak
    wavelength of the affected cone type. This is physiologically motivated
    and produces more accurate intermediate-severity results than the linear
    interpolation used by DichromacySimulator subclasses.

    When to use
    -----------
    - Protanomaly or deuteranomaly (severity between 0.0 and 1.0 exclusive).
    - When severity-varying animation or comparison is needed.
    - Do NOT use for tritanopia -- use Simulator_Brettel1997 instead.

    Notes
    -----
    Precomputed 3x3 RGB matrices are stored in ``machado_2009_matrices`` at
    11 severity levels (0.0, 0.1, ..., 1.0). At runtime the two nearest
    matrices are linearly interpolated. No LMS model dependency at inference
    time -- the matrices are precomputed for sRGB/SmithPokorny75.
    """

    def _simulate_cvd_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        if deficiency not in machado_2009_matrices:
            raise ValueError(
                f"Simulator_Machado2009 does not support {deficiency!r}. "
                "Use Simulator_Achromat or Simulator_BCM instead."
            )
        assert severity >= 0.0 and severity <= 1.0
        severity_lower = int(math.floor(severity*10.0))
        severity_higher = min(severity_lower + 1, 10)
        m1 = machado_2009_matrices[deficiency][severity_lower]
        m2 = machado_2009_matrices[deficiency][severity_higher]

        # alpha = 0 => only m1, alpha = 1.0 => only m2
        alpha = (severity - severity_lower/10.0)
        m = alpha*m2 + (1.0-alpha)*m1

        return convert.apply_color_matrix(image_linear_rgb_float32, m)

class Simulator_Achromat (Simulator):
    """Simulates rod monochromacy (complete achromatopsia).

    All cone types are non-functional; perception is based solely on rod
    photoreceptors. At typical monitor luminance (100-400 cd/m^2) the
    perceptual weighting follows BT.709 photopic luminance:

        Y = 0.2126 * R_linear + 0.7152 * G_linear + 0.0722 * B_linear

    This is consistent with WCAG relative luminance, keeping GATE-007 achromat
    validation internally aligned with GATE-002 contrast validation.

    Alternative weights from CIE 1951 scotopic V'(lambda):
        [0.007, 0.519, 0.474]  (ixora ColorBlindness library)
    These are more physiologically accurate for rod-dominant vision but shift
    the effective luminance toward blue-green.

    Severity blending is implemented here (not via DichromacySimulator) because
    achromatopsia is not a form of dichromacy. The base Simulator class handles
    gamma encode/decode and uint8 conversion.

    References
    ----------
    - ITU-R BT.709-6, Section 3 (BT.709 luminance coefficients)
    - WCAG 2.1: https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
    - CIE (1951) scotopic luminosity function V'(lambda)
    """

    _BT709_Y = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)

    def _simulate_cvd_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        # Dot each pixel with BT.709 weights -> shape (H, W)
        Y = image_linear_rgb_float32 @ self._BT709_Y
        # Broadcast to 3 channels: shape (H, W, 3)
        gray = np.stack([Y, Y, Y], axis=-1)
        if severity < 0.99999:
            return gray * severity + image_linear_rgb_float32 * (1.0 - severity)
        return gray


class Simulator_BCM (Simulator):
    """Simulates blue-cone monochromacy (BCM / X-linked incomplete achromatopsia).

    BCM subjects carry mutations in OPN1LW and OPN1MW, eliminating functional
    L-cones and M-cones. Only S-cones (short-wavelength / blue-sensitive) and
    rod photoreceptors remain. They perceive a two-dimensional world: achromatic
    brightness from rods plus S-cone chromaticity.

    Algorithm (SmithPokorny75 LMS model, linear RGB space)
    -------------------------------------------------------
    1. Convert pixel to LMS.
    2. Replace L response with luminance-scaled neutral:
           L' = Y * white_L   (Y = BT.709 luminance, white_L = LMS[0] of D65 white)
    3. Replace M response with luminance-scaled neutral:
           M' = Y * white_M
    4. Keep S-cone response unchanged.
    5. Convert LMS' back to linear RGB.
    6. Desaturate to fit gamut (S-cone can push blue out of sRGB range).

    Steps 1-5 reduce to a single 3x3 matrix multiplication. The matrix is
    precomputed for the SmithPokorny75 + sRGB combination and stored in _BCM.

    Precomputation snippet (for reproducibility)
    --------------------------------------------
    ::

        from daltonlens import convert
        import numpy as np
        model  = convert.LMSModel_sRGB_SmithPokorny75()
        bt709  = np.array([0.2126, 0.7152, 0.0722])
        w_lms  = model.LMS_from_linearRGB @ np.ones(3)  # ~[0.65518, 0.34478, 0.01608]
        A      = np.vstack([w_lms[0]*bt709, w_lms[1]*bt709,
                            model.LMS_from_linearRGB[2]])
        BCM    = model.linearRGB_from_LMS @ A

    References
    ----------
    - Smith & Pokorny (1975) LMS model (via Vienot et al. 1999)
    - Sechrest & Bhatt (2023) BCM gene therapy review
    - Mancuso et al. (2009) BCM physiology in primates
    """

    # Precomputed BCM matrix (SmithPokorny75 + sRGB).
    # white_lms ~= [0.65518, 0.34478, 0.01608]
    _BCM = np.array([
        [ 0.17437,  0.59636,  0.22927],
        [ 0.24981,  0.83088, -0.08069],
        [-0.01452,  0.00907,  1.00546],
    ], dtype=np.float32)

    def _simulate_cvd_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        im_cvd = convert.apply_color_matrix(image_linear_rgb_float32, self._BCM)
        # Inline gamut fix using ellipsis indexing -- works for any shape (..., 3).
        # (convert.desaturate_linearRGB_to_fit_in_gamut uses im[:,0] which requires
        # 2D (N,3); we avoid the reshape by using ... indexing instead.)
        min_val = np.minimum(im_cvd[..., 0],
                  np.minimum(im_cvd[..., 1], im_cvd[..., 2]))
        min_val = np.minimum(min_val, 0.0)
        im_cvd  = np.clip(im_cvd - min_val[..., np.newaxis], 0.0, 1.0)
        # Severity blend AFTER gamut fix (blending out-of-gamut values corrupts mid-tones)
        if severity < 0.99999:
            return im_cvd * severity + image_linear_rgb_float32 * (1.0 - severity)
        return im_cvd


coblis_v1_matrices = {
    Deficiency.PROTAN: np.array([[0.567, 0.433, 0.000],
                                 [0.558, 0.442, 0.000],
                                 [0.000, 0.242, 0.758]]),

    Deficiency.DEUTAN: np.array([[0.625, 0.375, 0.000],
                                 [0.700, 0.300, 0.000],
                                 [0.000, 0.300, 0.700]]),

    Deficiency.TRITAN: np.array([[0.950,0.050,0.000],
                                 [0.000, 0.433, 0.567],
                                 [0.000, 0.475, 0.525]])
}

class Simulator_CoblisV1 (DichromacySimulator):
    """The first version of Coblis, as implemented by
    https://github.com/MaPePeR/jsColorblindSimulator
    for
    https://www.color-blindness.com/coblis-color-blindness-simulator/

    This model is very inaccurate and should not be used, it is only
    here for comparison purposes. You can read more about its history
    and accuracy in https://daltonlens.org/opensource-cvd-simulation/
    """

    def __init__(self):
        import warnings
        warnings.warn(
            "Simulator_CoblisV1 is deprecated and has very poor accuracy. "
            "Use Simulator_Brettel1997 or Simulator_Vienot1999 instead. "
            "See https://daltonlens.org/opensource-cvd-simulation/ for details.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()
        # No sRGB nor gamma correction at all in CoblisV1.
        self.imageEncoding = convert.ImageEncoding.LINEAR_RGB

    def _simulate_dichromacy_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency):
        m = coblis_v1_matrices[deficiency]
        return convert.apply_color_matrix(image_linear_rgb_float32, m)

coblis_v2_constants = {
    Deficiency.PROTAN: {'cpu': 0.735, 'cpv':  0.265, 'am': 1.273463, 'ayi': -0.073894},
    Deficiency.DEUTAN: {'cpu': 1.140, 'cpv': -0.140, 'am': 0.968437, 'ayi':  0.003331},
    Deficiency.TRITAN: {'cpu': 0.171, 'cpv': -0.003, 'am': 0.062921, 'ayi':  0.292119}
}

class Simulator_CoblisV2 (DichromacySimulator):
    """The second version of Coblis, as implemented by
    https://github.com/MaPePeR/jsColorblindSimulator
    for
    https://www.color-blindness.com/coblis-color-blindness-simulator/

    This was adapted from the HCIRN Color Blind Simulation function.
    
    It is not recommended as it lacks a proper background to assess
    its accuracy. You can read more about its history in 
    https://daltonlens.org/opensource-cvd-simulation/
    """

    def __init__(self):
        super().__init__()
        # CoblisV2 uses old CRTs gamma correction.
        self.imageEncoding = convert.ImageEncoding.GAMMA_22

    def _simulate_dichromacy_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency):
        # Implementation adapted from https://github.com/jkulesza/peacock by
        # moving it to numpy and restoring the original issue with large values.
        #
        # NOTE: This implementation allocates multiple intermediate arrays for
        # clarity and debugging. A production optimization could reduce memory
        # usage by ~50% through in-place operations, but the current approach
        # prioritizes readability for research purposes. For performance-critical
        # applications, use the C library (libDaltonLens) instead.
        wx = 0.312713
        wy = 0.329016
        wz = 0.358271

        cpu = coblis_v2_constants[deficiency]['cpu']
        cpv = coblis_v2_constants[deficiency]['cpv']
        am  = coblis_v2_constants[deficiency]['am']
        ayi = coblis_v2_constants[deficiency]['ayi']

        rgb2xyz = np.array([[0.430574, 0.341550, 0.178325],
                            [0.222015, 0.706655, 0.071330],
                            [0.020183, 0.129553, 0.939180]])
        crgb = image_linear_rgb_float32
        cxyz = convert.apply_color_matrix(crgb, rgb2xyz)
        cx = cxyz[:,:,0]
        cy = cxyz[:,:,1]
        sum_xyz = np.sum(cxyz, axis=2)

        with np.errstate(divide='ignore', invalid='ignore'):
            cu = cx / sum_xyz
            cv = cy / sum_xyz
            np.nan_to_num(cu, copy=False)
            np.nan_to_num(cv, copy=False)

        nx = wx * cy / wy
        nz = wz * cy / wy
        
        clm = (cpv - cv) / (cpu - cu)
        # clm[cu >= cpu] *= -1.0

        clyi = cv - np.multiply(cu, clm)
        du = np.divide((ayi - clyi), (clm - am))
        dv = np.multiply(clm, du) + clyi

        sxyz = np.zeros_like(cxyz)
        sx = sxyz[:,:,0] = np.divide(np.multiply(du, cy), dv)
        sy = sxyz[:,:,1] = cy
        sz = sxyz[:,:,2] = np.divide(np.multiply((1.0 - (du + dv)), cy), dv)
        
        xyz2rgb = np.array([[ 3.063218, -1.393325, -0.475802],
                            [-0.969243,  1.875966,  0.041555],
                            [ 0.067871, -0.228834,  1.069251]])
        srgb = convert.apply_color_matrix(sxyz, xyz2rgb)

        dxyz = np.zeros_like(sxyz)
        dx = dxyz[:,:,0] = nx - sx
        dy = dxyz[:,:,1] # = 0
        dz = dxyz[:,:,2] = nz - sz

        drgb = convert.apply_color_matrix(dxyz, xyz2rgb)
        
        adjrgb = np.zeros_like(drgb)
        # Note: peacock fixed some issues with large values by doing drgb > 0.0 instead.
        # It's unclear to me whether it can have drawbacks, but sticking to the original
        # behavior that only avoids exact zero for comparison purposes.
        with np.errstate(divide='ignore'):
            adjrgb = np.divide((np.where(srgb < 0.0, 0.0, 1.0) - srgb), drgb)
        np.nan_to_num(adjrgb, copy=False)

        adjust = adjrgb
        adjust[np.logical_or(adjrgb > 1.0, adjrgb < 0.0)] = 0.0
        adjust = np.amax(adjust, 2) # becomes (M,N,1) here
        srgb = srgb + np.multiply(drgb, adjust[..., np.newaxis])
        return srgb

class Simulator_AutoSelect (Simulator):
    """Automatically selects the best algorithm for the given deficiency and severity.

    Selection rules:

    - ACHROMAT (any severity) -> Simulator_Achromat  (BT.709 luminance projection)
    - BCM      (any severity) -> Simulator_BCM       (SmithPokorny75 S-cone preservation)
    - TRITAN   (any severity) -> Simulator_Brettel1997  (only accurate tritan model)
    - Protan/Deutan severity < 1.0  -> Simulator_Machado2009  (principled anomalous trichromacy)
    - Protan/Deutan severity = 1.0  -> Simulator_Vienot1999   (fast, accurate dichromacy)

    When to use
    -----------
    Use this class when you want the library to choose the most appropriate
    algorithm without hardcoding a specific one. It is the recommended default
    for new code that does not have a specific accuracy or performance requirement.

    Notes
    -----
    LMS model instances are cached at module level to avoid repeated matrix
    inversion. The cache key is the model name string.
    """
    def _simulate_cvd_linear_rgb (self, image_linear_rgb_float32, deficiency: Deficiency, severity: float):
        if deficiency == Deficiency.ACHROMAT:
            logger.debug("Choosing Simulator_Achromat for rod monochromacy")
            simulator = Simulator_Achromat()
        elif deficiency == Deficiency.BCM:
            logger.debug("Choosing Simulator_BCM for blue-cone monochromacy")
            simulator = Simulator_BCM()
        elif deficiency == Deficiency.TRITAN:
            logger.debug("Choosing Brettel 1997 for tritanopia / tritanomaly")
            model = _lms_cache.setdefault("SmithPokorny75", convert.LMSModel_sRGB_SmithPokorny75())
            simulator = Simulator_Brettel1997(model)
        elif severity < 0.999:
            logger.debug("Anomalous trichromacy requested, using Machado 2009")
            simulator = Simulator_Machado2009()
        else:
            logger.debug("Choosing Viénot 1999 for %s",
                         "protanopia" if deficiency == Deficiency.PROTAN else "deuteranopia")
            model = _lms_cache.setdefault("SmithPokorny75", convert.LMSModel_sRGB_SmithPokorny75())
            simulator = Simulator_Vienot1999(model)

        return simulator._simulate_cvd_linear_rgb (image_linear_rgb_float32, deficiency, severity)
