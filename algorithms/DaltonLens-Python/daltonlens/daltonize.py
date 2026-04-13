"""
Daltonization algorithms for color vision deficiency correction.

Daltonization adjusts colors in an image to help people with color vision
deficiency distinguish colors that would otherwise appear similar or identical.

This module implements several daltonization algorithms:
- Fidaner et al. (2006): Classic error-diffusion method
- Simple color enhancement: Lightweight approach for real-time use

References
----------
Fidaner, O., Lin, P., & Ozguner, U. (2006). A multi-resolution approach
to color quantization for image analysis and enhancement.
"""

import numpy as np
from daltonlens import convert, simulate
from daltonlens.simulate import Deficiency


def daltonize_fidaner(
    image_srgb_uint8: np.ndarray,
    deficiency: Deficiency,
    severity: float = 1.0,
    simulator: simulate.Simulator = None,
) -> np.ndarray:
    """
    Daltonize an image using the Fidaner et al. error-diffusion method.

    This algorithm:
    1. Simulates what a colorblind person would see
    2. Calculates the color error (difference between original and simulated)
    3. Shifts the error to color channels the person CAN perceive
    4. Adds the shifted error back to the original image

    Parameters
    ----------
    image_srgb_uint8 : np.ndarray
        Input sRGB image with shape (H, W, 3) and dtype uint8.
    deficiency : Deficiency
        Type of color vision deficiency (PROTAN, DEUTAN, or TRITAN).
    severity : float, optional
        Severity of correction from 0.0 to 1.0. Default is 1.0.
    simulator : Simulator, optional
        CVD simulator to use. Defaults to Simulator_Brettel1997.

    Returns
    -------
    np.ndarray
        Daltonized sRGB image with shape (H, W, 3) and dtype uint8.

    Notes
    -----
    The error shifting matrix moves information from the confused color
    channels into channels that the dichromat can still perceive:
    - Protanopia/Deuteranopia: Red-green confusion -> shift to blue
    - Tritanopia: Blue-yellow confusion -> shift to red/green
    """
    if simulator is None:
        simulator = simulate.Simulator_Brettel1997(
            convert.LMSModel_sRGB_SmithPokorny75()
        )

    # Convert to float for processing
    image_float = convert.as_float32(image_srgb_uint8)
    image_linear = convert.linearRGB_from_sRGB(image_float)

    # Simulate CVD to get what the colorblind person sees
    simulated = simulator.simulate_cvd(image_srgb_uint8, deficiency, severity=1.0)
    simulated_float = convert.as_float32(simulated)
    simulated_linear = convert.linearRGB_from_sRGB(simulated_float)

    # Calculate the error (what information is lost)
    error = image_linear - simulated_linear

    # Error shifting matrices
    # These matrices redistribute the lost color information to visible channels
    if deficiency in (Deficiency.PROTAN, Deficiency.DEUTAN):
        # For red-green blindness, shift error to blue channel
        # Also add some to green to increase overall contrast
        error_shift_matrix = np.array([
            [0.0, 0.0, 0.0],
            [0.7, 1.0, 0.0],
            [0.7, 0.0, 1.0],
        ])
    else:  # TRITAN
        # For blue-yellow blindness, shift error to red/green channels
        error_shift_matrix = np.array([
            [1.0, 0.0, 0.7],
            [0.0, 1.0, 0.7],
            [0.0, 0.0, 0.0],
        ])

    # Apply error shift
    shifted_error = convert.apply_color_matrix(error, error_shift_matrix)

    # Add shifted error back to original (with severity scaling)
    daltonized_linear = image_linear + shifted_error * severity

    # Clamp to valid range and convert back to sRGB
    daltonized_linear = np.clip(daltonized_linear, 0.0, 1.0)
    daltonized_srgb = convert.sRGB_from_linearRGB(daltonized_linear)

    return convert.as_uint8(daltonized_srgb)


def daltonize_simple(
    image_srgb_uint8: np.ndarray,
    deficiency: Deficiency,
    strength: float = 1.0,
) -> np.ndarray:
    """
    Simple daltonization using color channel enhancement.

    A lightweight daltonization method suitable for real-time applications.
    Enhances contrast in the confused color channels by adjusting saturation
    and shifting hues.

    Parameters
    ----------
    image_srgb_uint8 : np.ndarray
        Input sRGB image with shape (H, W, 3) and dtype uint8.
    deficiency : Deficiency
        Type of color vision deficiency.
    strength : float, optional
        Enhancement strength from 0.0 to 1.0. Default is 1.0.

    Returns
    -------
    np.ndarray
        Enhanced sRGB image with shape (H, W, 3) and dtype uint8.
    """
    image_float = convert.as_float32(image_srgb_uint8)

    if deficiency in (Deficiency.PROTAN, Deficiency.DEUTAN):
        # Enhance red-green distinction by shifting reds toward orange
        # and greens toward cyan
        r, g, b = image_float[:, :, 0], image_float[:, :, 1], image_float[:, :, 2]

        # Calculate red-green difference
        rg_diff = r - g

        # Shift reds (positive rg_diff) toward orange (add to green)
        # Shift greens (negative rg_diff) toward cyan (add to blue)
        enhancement = rg_diff * strength * 0.5

        new_g = np.clip(g + np.maximum(enhancement, 0), 0, 1)
        new_b = np.clip(b - np.minimum(enhancement, 0), 0, 1)

        result = np.stack([r, new_g, new_b], axis=2)

    else:  # TRITAN
        # Enhance blue-yellow distinction
        r, g, b = image_float[:, :, 0], image_float[:, :, 1], image_float[:, :, 2]

        # Calculate blue vs yellow (red+green) difference
        yellow = (r + g) / 2
        by_diff = b - yellow

        # Shift blues toward purple, yellows toward orange
        enhancement = by_diff * strength * 0.5

        new_r = np.clip(r + np.maximum(enhancement, 0), 0, 1)
        new_g = np.clip(g - np.minimum(enhancement, 0), 0, 1)

        result = np.stack([new_r, new_g, b], axis=2)

    return convert.as_uint8(result)


# Default daltonize function
def daltonize(
    image_srgb_uint8: np.ndarray,
    deficiency: Deficiency,
    severity: float = 1.0,
    method: str = "fidaner",
    **kwargs,
) -> np.ndarray:
    """
    Daltonize an image to help colorblind viewers distinguish colors.

    Parameters
    ----------
    image_srgb_uint8 : np.ndarray
        Input sRGB image with shape (H, W, 3) and dtype uint8.
    deficiency : Deficiency
        Type of color vision deficiency (PROTAN, DEUTAN, or TRITAN).
    severity : float, optional
        Correction strength from 0.0 to 1.0. Default is 1.0.
    method : str, optional
        Daltonization method: "fidaner" (default) or "simple".
    **kwargs : dict
        Additional arguments passed to the specific method.

    Returns
    -------
    np.ndarray
        Daltonized sRGB image with shape (H, W, 3) and dtype uint8.

    Examples
    --------
    >>> from daltonlens import daltonize
    >>> from daltonlens.simulate import Deficiency
    >>> import numpy as np
    >>> from PIL import Image
    >>>
    >>> img = np.array(Image.open("input.png"))
    >>> corrected = daltonize.daltonize(img, Deficiency.DEUTAN)
    >>> Image.fromarray(corrected).save("daltonized.png")
    """
    if method == "fidaner":
        return daltonize_fidaner(image_srgb_uint8, deficiency, severity, **kwargs)
    elif method == "simple":
        return daltonize_simple(image_srgb_uint8, deficiency, severity)
    else:
        raise ValueError(f"Unknown daltonization method: {method}")
