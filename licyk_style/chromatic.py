"""
chromatic effect for image

origin: https://github.com/KohakuBlueleaf/a1111-sd-webui-haku-img/tree/main/hakuimg/chromatic

thanks: KohakuBlueleaf
"""
import math
import numpy as np
from PIL import Image
from PIL.ImageFile import ImageFile
from typing import List


def cartesian_to_polar(data: np.ndarray) -> np.ndarray:
    """Returns the polar form of <data>"""
    width = data.shape[1]
    height = data.shape[0]
    assert width > 2
    assert height > 2
    assert width % 2 == 1
    assert height % 2 == 1
    perimeter = 2 * (width + height - 2)
    halfdiag = math.ceil(((width**2 + height**2) ** 0.5) / 2)
    halfw = width // 2
    halfh = height // 2
    ret = np.zeros((halfdiag, perimeter, 3))

    # Don't want to deal with divide by zero errors...
    ret[0: (halfw + 1), halfh] = data[halfh, halfw::-1]
    ret[0: (halfw + 1), height + width - 2 + halfh] = data[
        halfh, halfw: (halfw * 2 + 1)
    ]
    ret[0: (halfh + 1), height - 1 +
        halfw] = data[halfh: (halfh * 2 + 1), halfw]
    ret[0: (halfh + 1), perimeter - halfw] = data[halfh::-1, halfw]

    # Divide the image into 8 triangles, and use the same calculation on
    # 4 triangles at a time. This is possible due to symmetry.
    # This section is also responsible for the corner pixels
    for i in range(0, halfh):
        slope = (halfh - i) / (halfw)
        diagx = ((halfdiag**2) / (slope**2 + 1)) ** 0.5
        unit_xstep = diagx / (halfdiag - 1)
        unit_ystep = diagx * slope / (halfdiag - 1)
        for row in range(halfdiag):
            ystep = round(row * unit_ystep)
            xstep = round(row * unit_xstep)
            if (halfh >= ystep) and halfw >= xstep:
                ret[row, i] = data[halfh - ystep, halfw - xstep]
                ret[row, height - 1 - i] = data[halfh + ystep, halfw - xstep]
                ret[row, height + width - 2 +
                    i] = data[halfh + ystep, halfw + xstep]
                ret[row, height + width + height - 3 - i] = data[
                    halfh - ystep, halfw + xstep
                ]
            else:
                break

    # Remaining 4 triangles
    for j in range(1, halfw):
        slope = (halfh) / (halfw - j)
        diagx = ((halfdiag**2) / (slope**2 + 1)) ** 0.5
        unit_xstep = diagx / (halfdiag - 1)
        unit_ystep = diagx * slope / (halfdiag - 1)
        for row in range(halfdiag):
            ystep = round(row * unit_ystep)
            xstep = round(row * unit_xstep)
            if halfw >= xstep and halfh >= ystep:
                ret[row, height - 1 + j] = data[halfh + ystep, halfw - xstep]
                ret[row, height + width - 2 -
                    j] = data[halfh + ystep, halfw + xstep]
                ret[row, height + width + height - 3 + j] = data[
                    halfh - ystep, halfw + xstep
                ]
                ret[row, perimeter - j] = data[halfh - ystep, halfw - xstep]
            else:
                break
    return ret


def get_gauss(n: int) -> List[float]:
    """Return the Gaussian 1D kernel for a diameter of <n>
    Referenced from: https://stackoverflow.com/questions/11209115/
    """
    sigma = 0.3 * (n / 2 - 1) + 0.8
    r = range(-int(n / 2), int(n / 2) + 1)
    new_sum = sum(
        [
            1
            / (sigma * math.sqrt(2 * math.pi))
            * math.exp(-float(x) ** 2 / (2 * sigma**2))
            for x in r
        ]
    )
    # Ensure that the gaussian array adds up to one
    return [
        (
            1
            / (sigma * math.sqrt(2 * math.pi))
            * math.exp(-float(x) ** 2 / (2 * sigma**2))
        )
        / new_sum
        for x in r
    ]


def vertical_gaussian(data: np.ndarray, n: int) -> np.ndarray:
    """Peforms a Gaussian blur in the vertical direction on <data>. Returns
    the resulting numpy array.

    <n> is the radius, where 1 pixel radius indicates no blur
    """
    padding = n - 1
    width = data.shape[1]
    height = data.shape[0]
    padded_data = np.zeros((height + padding * 2, width))
    padded_data[padding:-padding, :] = data
    ret = np.zeros((height, width))
    kernel = None
    old_radius = -1
    for i in range(height):
        radius = round(i * padding / (height - 1)) + 1
        # Recreate new kernel only if we have to
        if radius != old_radius:
            old_radius = radius
            kernel = np.tile(
                get_gauss(1 + 2 * (radius - 1)),
                (width, 1)
            ).transpose()
        ret[i, :] = np.sum(
            np.multiply(
                padded_data[
                    padding + i - radius +
                    1: padding + i + radius, :
                ],
                kernel
            ),
            axis=0,
        )
    return ret


def polar_to_cartesian(data: np.ndarray, width: int, height: int) -> np.ndarray:
    """Returns the cartesian form of <data>.

    <width> is the original width of the cartesian image
    <height> is the original height of the cartesian image
    """
    assert width > 2
    assert height > 2
    assert width % 2 == 1
    assert height % 2 == 1
    perimeter = 2 * (width + height - 2)
    halfdiag = math.ceil(((width**2 + height**2) ** 0.5) / 2)
    halfw = width // 2
    halfh = height // 2
    ret = np.zeros((height, width, 3))

    def div0():
        # Don't want to deal with divide by zero errors...
        ret[halfh, halfw::-1] = data[0: (halfw + 1), halfh]
        ret[halfh, halfw: (halfw * 2 + 1)] = data[
            0: (halfw + 1), height + width - 2 + halfh
        ]
        ret[halfh: (halfh * 2 + 1), halfw] = data[
            0: (halfh + 1),
            height - 1 + halfw
        ]
        ret[halfh::-1, halfw] = data[0: (halfh + 1), perimeter - halfw]

    div0()

    # Same code as above, except the order of the assignments are switched
    # Code blocks are split up for easier profiling
    def part1():
        for i in range(0, halfh):
            slope = (halfh - i) / (halfw)
            diagx = ((halfdiag**2) / (slope**2 + 1)) ** 0.5
            unit_xstep = diagx / (halfdiag - 1)
            unit_ystep = diagx * slope / (halfdiag - 1)
            for row in range(halfdiag):
                ystep = round(row * unit_ystep)
                xstep = round(row * unit_xstep)
                if (halfh >= ystep) and halfw >= xstep:
                    ret[halfh - ystep, halfw - xstep] = data[row, i]
                    ret[halfh + ystep, halfw - xstep] = data[row, height - 1 - i]
                    ret[halfh + ystep, halfw + xstep] = data[
                        row, height + width - 2 + i
                    ]
                    ret[halfh - ystep, halfw + xstep] = data[
                        row, height + width + height - 3 - i
                    ]
                else:
                    break

    part1()

    def part2():
        for j in range(1, halfw):
            slope = (halfh) / (halfw - j)
            diagx = ((halfdiag**2) / (slope**2 + 1)) ** 0.5
            unit_xstep = diagx / (halfdiag - 1)
            unit_ystep = diagx * slope / (halfdiag - 1)
            for row in range(halfdiag):
                ystep = round(row * unit_ystep)
                xstep = round(row * unit_xstep)
                if halfw >= xstep and halfh >= ystep:
                    ret[halfh + ystep, halfw - xstep] = data[row, height - 1 + j]
                    ret[halfh + ystep, halfw + xstep] = data[
                        row, height + width - 2 - j
                    ]
                    ret[halfh - ystep, halfw + xstep] = data[
                        row, height + width + height - 3 + j
                    ]
                    ret[halfh - ystep, halfw - xstep] = data[row, perimeter - j]
                else:
                    break

    part2()

    # Repairs black/missing pixels in the transformed image
    def set_zeros():
        zero_mask = ret[1:-1, 1:-1] == 0
        ret[1:-1, 1:-1] = np.where(
            zero_mask, (ret[:-2, 1:-1] + ret[2:, 1:-1]) / 2, ret[1:-1, 1:-1]
        )

    set_zeros()

    return ret


def add_chromatic(im: ImageFile, strength: float = 1, no_blur: bool = False) -> Image:
    """Splits <im> into red, green, and blue channels, then performs a
    1D Vertical Gaussian blur through a polar representation. Finally,
    it expands the green and blue channels slightly.

    <strength> determines the amount of expansion and blurring.
    <no_blur> disables the radial blur
    """
    try:
        r, g, b = im.split()
    except Exception as _:
        r, g, b, _ = im.split()

    rdata = np.asarray(r)
    gdata = np.asarray(g)
    bdata = np.asarray(b)
    if no_blur:
        # channels remain unchanged
        rfinal = r
        gfinal = g
        bfinal = b
    else:
        poles = cartesian_to_polar(np.stack([rdata, gdata, bdata], axis=-1))
        rpolar, gpolar, bpolar = (
            poles[:, :, 0],
            poles[:, :, 1],
            poles[:, :, 2],
        )

        bluramount = (im.size[0] + im.size[1] - 2) / 100 * strength
        if round(bluramount) > 0:
            rpolar = vertical_gaussian(rpolar, round(bluramount))
            gpolar = vertical_gaussian(gpolar, round(bluramount * 1.2))
            bpolar = vertical_gaussian(bpolar, round(bluramount * 1.4))

        rgbpolar = np.stack([rpolar, gpolar, bpolar], axis=-1)
        cartes = polar_to_cartesian(
            rgbpolar, width=rdata.shape[1], height=rdata.shape[0]
        )
        rcartes, gcartes, bcartes = (
            cartes[:, :, 0],
            cartes[:, :, 1],
            cartes[:, :, 2],
        )

        rfinal = Image.fromarray(np.uint8(rcartes), "L")
        gfinal = Image.fromarray(np.uint8(gcartes), "L")
        bfinal = Image.fromarray(np.uint8(bcartes), "L")

    # enlarge the green and blue channels slightly, blue being the most enlarged
    gfinal = gfinal.resize(
        (
            round((1 + 0.018 * strength) * rdata.shape[1]),
            round((1 + 0.018 * strength) * rdata.shape[0]),
        ),
        Image.Resampling.LANCZOS,
    )
    bfinal = bfinal.resize(
        (
            round((1 + 0.044 * strength) * rdata.shape[1]),
            round((1 + 0.044 * strength) * rdata.shape[0]),
        ),
        Image.Resampling.LANCZOS,
    )

    rwidth, rheight = rfinal.size
    gwidth, gheight = gfinal.size
    bwidth, bheight = bfinal.size
    rhdiff = (bheight - rheight) // 2
    rwdiff = (bwidth - rwidth) // 2
    ghdiff = (bheight - gheight) // 2
    gwdiff = (bwidth - gwidth) // 2

    # Centre the channels
    im = Image.merge(
        "RGB",
        (
            rfinal.crop((-rwdiff, -rhdiff, bwidth - rwdiff, bheight - rhdiff)),
            gfinal.crop((-gwdiff, -ghdiff, bwidth - gwdiff, bheight - ghdiff)),
            bfinal,
        ),
    )

    # Crop the image to the original image dimensions
    return im.crop((rwdiff, rhdiff, rwidth + rwdiff, rheight + rhdiff))
