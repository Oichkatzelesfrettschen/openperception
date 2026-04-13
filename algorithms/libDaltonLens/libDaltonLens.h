/* libDaltonLens - public domain library - http://daltonlens.org
                                  no warranty implied; use at your own risk

    Author: Nicolas Burrus <nicolas@burrus.name>

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    For more information, please refer to <https://unlicense.org>
*/

#include <stddef.h>

enum DLDeficiency
{
    DLDeficiency_Protan,
    DLDeficiency_Deutan,
    DLDeficiency_Tritan,
    DLDeficiency_Achromat, /* Rod monochromacy (achromatopsia, all cones absent) */
    DLDeficiency_BCM       /* Blue-cone monochromacy (OPN1LW/OPN1MW absent)     */
};

/*
    Automatically picks the best CVD simulation algorithm (Brettel 1997 for
    tritanopia, Viénot 1999 for protanopia and deuteranopia).

    For a comparison of the available algorithms see:
    https://daltonlens.org/opensource-cvd-simulation/

    For more information about the math of the chosen algorithms see
    https://daltonlens.org/understanding-cvd-simulation/

    'srgba_image' is expected to be in the RGBA32 format, 8 bits per channel,
    encoded as sRGB.

    'severity' should be between 0.0 and 1.0 and is implemented via a linear
    interpolation with the original image.

    'bytesPerRow' can be 0, in which case it'll be automatically computed as
    width*4.
*/
void dl_simulate_cvd (enum DLDeficiency deficiency, float severity, unsigned char *srgba_image, size_t width, size_t height, size_t bytesPerRow);

/*
    Implements the algorithm proposed in 1997 by 
    Brettel, H. and Viénot, F. and Mollon, J. D.

    'Computerized simulation of color appearance for dichromats'
    Journal of the Optical Society of America. A, Optics, Image Science, and Vision    

    It works well for all kinds of dichromacies, but is a bit more expensive
    than Viénot 1999.

    This version is adapted to modern sRGB monitors.
*/
void dl_simulate_cvd_brettel1997 (enum DLDeficiency deficiency, float severity, unsigned char* srgba_image, size_t width, size_t height, size_t bytesPerRow);

/*
    Implements the algorithm proposed in 1999 by
    Viénot, F. and Brettel, H. and Mollon, J. D.

    Digital video colourmaps for checking the legibility of displays by dichromats
	Color Research & Application

    It works well for protanopia and deuteranopia, but NOT for tritanopia.

    This version is adapted to modern sRGB monitors.
*/
void dl_simulate_cvd_vienot1999 (enum DLDeficiency deficiency, float severity, unsigned char* srgba_image, size_t width, size_t height, size_t bytesPerRow);

/*
    Simulates rod monochromacy (achromatopsia / complete color blindness).

    Maps every pixel to its BT.709 photopic luminance:
        Y = 0.2126 * R_linear + 0.7152 * G_linear + 0.0722 * B_linear

    All three output channels are set to Y. Consistent with WCAG relative
    luminance, enabling direct cross-checking with contrast validation.

    'deficiency' parameter is ignored; use DLDeficiency_Achromat for clarity.
*/
void dl_simulate_cvd_achromat (float severity, unsigned char* srgba_image, size_t width, size_t height, size_t bytesPerRow);

/*
    Simulates blue-cone monochromacy (BCM / X-linked incomplete achromatopsia).

    BCM subjects lack L and M cones (OPN1LW / OPN1MW mutations). Only S-cones
    and rods are functional. L and M cone responses are replaced by a
    luminance-scaled neutral; the S-cone response is preserved.

    Uses a precomputed 3x3 matrix derived from the Smith-Pokorny 1975 LMS
    model adapted to sRGB (same model as Brettel 1997 and Vienot 1999).

    Regenerate matrix:
        from daltonlens import convert; import numpy as np
        model = convert.LMSModel_sRGB_SmithPokorny75()
        w = model.LMS_from_linearRGB @ np.ones(3)
        bt709 = np.array([0.2126, 0.7152, 0.0722])
        A = np.vstack([w[0]*bt709, w[1]*bt709, model.LMS_from_linearRGB[2]])
        BCM = model.linearRGB_from_LMS @ A

    'deficiency' parameter is ignored; use DLDeficiency_BCM for clarity.
*/
void dl_simulate_cvd_bcm (float severity, unsigned char* srgba_image, size_t width, size_t height, size_t bytesPerRow);

/*
    Implements anomalous trichromacy simulation using the method of Machado,
    Oliveira and Fernandes (2009).

    "A physiologically-based model for simulation of color vision deficiency"
    IEEE Transactions on Visualization and Computer Graphics

    Supports DLDeficiency_Protan, DLDeficiency_Deutan, and DLDeficiency_Tritan.
    For severity 1.0 (dichromacy), the result matches Vienot 1999.

    'severity' ranges from 0.0 (normal vision) to 1.0 (complete dichromacy).
    Values between 0 and 1 simulate anomalous trichromacy by interpolating
    between precomputed matrices.
*/
void dl_simulate_cvd_machado2009 (enum DLDeficiency deficiency, float severity, unsigned char* srgba_image, size_t width, size_t height, size_t bytesPerRow);
