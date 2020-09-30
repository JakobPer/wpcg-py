# import these three numpy packages as pyinstaller fails if not
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import imageio as iio
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image


class ImageUtils:

    @staticmethod
    def make_pretty(src, dest, repeat_background=False, blur_background=False, sigma=10, blend_edges=False,
                    blend_ratio=0.02, width=1920, height=1080, thresh=0.1):
        """
        Creates a new image from the source image. The new image increases the size of the shorter edge of the source
        image to fit the R ratio provided. Then it calculated the median values of both column edges and then the mean
        value of both to get a fitting background color. The new image is filled with this mean color and the image is
        placed in the center and saved in dest. Image format is derived from the dest uri.

        If repeat background is enabled, the image is repeated left and right from the center in the background. If blur
        is also enabled this background is blurred with a gaussian blur with the provided sigma. I blend_edges is
        enabled the adjacent edges of the image in the center are linearly blended with the background depending on the
        blend ratio. The blend ratio defines how many pixels should be blended. It is defined as the percentage of the
        total size of the new image. In example, if the image is in portrait and has a width of 1000 pixels, the new
        width would be 2000 pixels and the ratio is 0.02, then 0.02*2000=40 pixels left and right of the 1000 pixels
        would be blended.

        :param src: uri to the source image.
        :param dest: uri to the destination image. Will be overwritten if exists.
        :param repeat_background: True if the image should be repeated in the background.
        :param blur_background: True if a gaussian blur should be applied to the background.
        :param sigma: The sigma value of the gaussian blur (how much it should be blurred, higher=more blurry).
        :param blend_edges: True if the edges of the central image should be blended with the background.
        :param blend_ratio: The ratio of how many pixels should be blended.
        :param width: The resulting width of the wallpaper.
        :param height: The resulting height of the wallpaper.
        :param thresh: The threshold of how much the aspect ratio need to deviate from the defined width/height ratio for the image to
        be prettified.
        :return: True is successful. May raise exceptions on error.
        """
        source_image = Image.open(src)
        source_ratio = source_image.width / source_image.height

        # set new size
        new_size = np.zeros(3, dtype=int)
        new_size[0] = height
        new_size[1] = width
        new_size[2] = 3

        image_ratio = float(width) / float(height)
        narrow = source_ratio < image_ratio

        if abs(image_ratio - source_ratio) <= thresh:
            return False

        # calculate resize dimensions to fit width/height
        if narrow:
            resize_dimension = (int(source_image.width * (height / source_image.height)), height)
        else:
            resize_dimension = (width, int(source_image.height * (width / source_image.width)))

        # resize the image and get numpy array
        source_image = source_image.resize(resize_dimension, resample=Image.BICUBIC)
        image = np.array(source_image)[:, :, 0:3]

        # calc mean of left/right or top/bottom depending on ratio
        means = None
        if narrow:
            means = np.median(image[:, (0, image.shape[1] - 1)], axis=0).astype(int)
        else:
            means = np.median(image[(0, image.shape[0] - 1), :], axis=0).astype(int)
        mean_color = np.mean(means, axis=0).astype(int)

        # create final image with mean color
        final = np.zeros(new_size, dtype=int)
        final[:, :] = mean_color

        # calc offset of center image
        offset = int((new_size[1] - image.shape[1]) / 2) if narrow else int((new_size[0] - image.shape[0]) / 2)

        if repeat_background:
            # repeat image in background
            if narrow:
                left = -int(image.shape[1] - offset % image.shape[1])
                repeat = True
                while repeat:
                    if left + image.shape[1] < new_size[1]:
                        right = left + image.shape[1]
                    else:
                        right = new_size[1]
                        repeat = False

                    if left < 0:
                        final[:, 0:right] = image[:, -left:(right - left)]
                    else:
                        final[:, left:right] = image[:, 0:(right - left)]
                    left = left + image.shape[1]
            else:
                top = -int(image.shape[0] - offset % image.shape[0])
                repeat = True
                while repeat:
                    if top + image.shape[0] < new_size[0]:
                        bottom = top + image.shape[0]
                    else:
                        bottom = new_size[0]
                        repeat = False

                    if top < 0:
                        final[0:bottom, :] = image[-top:(bottom - top), :]
                    else:
                        final[top:bottom, :] = image[0:(bottom - top), :]
                    top = top + image.shape[0]

        if blur_background:
            # blur the background
            final[:, :, 0] = gaussian_filter(final[:, :, 0], sigma=sigma)
            final[:, :, 1] = gaussian_filter(final[:, :, 1], sigma=sigma)
            final[:, :, 2] = gaussian_filter(final[:, :, 2], sigma=sigma)

        blend_radius = 0  # set to zero for final image composition to work if blur is disabled
        if blend_edges:
            # blend edges
            blend_radius = int(new_size[1] * blend_ratio) if narrow else int(new_size * blend_ratio)
            for i in range(0, blend_radius):
                f = i / blend_radius
                if narrow:
                    final[:, offset + i] = (1 - f) * final[:, offset + i] + f * image[:, i]
                    final[:, offset + image.shape[1] - (i + 1)] = (1 - f) * final[:,
                                                                            offset + image.shape[1] - (i + 1)] + \
                                                                  f * image[:, image.shape[1] - (i + 1)]
                else:
                    final[offset + i, :] = (1 - f) * final[offset + i, :] + f * image[i, :]
                    final[offset + image.shape[0] - (i + 1), :] = (1 - f) * final[offset + image.shape[0] - (i + 1),
                                                                            :] + \
                                                                  f * image[image.shape[1] - (i + 1), :]

        # finally composite the image into the center
        if narrow:
            final[:, offset + blend_radius:offset + image.shape[1] - blend_radius] = \
                image[:, blend_radius:image.shape[1] - blend_radius]
        else:
            final[offset + blend_radius:offset + image.shape[0] - blend_radius, :] = \
                image[blend_radius:image.shape[0] - blend_radius, :]

        # write image
        iio.imwrite(dest, np.uint8(final))
        return True
