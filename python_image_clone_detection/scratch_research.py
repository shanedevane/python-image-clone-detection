import sys
from PIL import Image, ImageFilter, ImageDraw
import operator as op
# from optparse import OptionParser
# import cv2
import os
import json
from PIL import Image, ImageStat, ImageEnhance
import PIL.ImageChops as IC
import numpy as np
import uuid
from matplotlib import pyplot as plt
from fractions import Fraction
from decimal import Decimal
from random import randint
import math

# ideally should use a design pattern (strategy?) instead of "enable" variabless

class ImageCloneDetector:
    IMAGE_BLOCK_SIZE = 20
    DUPLICATE_DISTANCE_MINIMUM = 0.02
    SAVE_BLOCK_IMAGES_OUTPUT = False
    SAVE_DUPLICATE_IMAGES_OUTPUT = True
    DEBUG_CONSOLE_OUTPUT = False
    ENABLE_IC_DIFF_COMPARISION = False   # slow
    ENABLE_EXACT_PIXEL_COMPARISION = False

    def __init__(self, file_path):
        self._file_path = file_path
        self._json_data = list()
        self._image = None
        self._grey_image = None
        self._blocks = list()
        self._duplicate_blocks = list()

    @property
    def json(self):
        return json.dumps(self._json_data)

    @staticmethod
    def _block_comparison_difference(image_a, image_b):
        try:
            if IC.difference(image_a, image_b).getbbox() is None:
                return True
        except:
            print('exception {0}'.format(sys.exc_info()[0]))
        return False

    @staticmethod
    def _block_comparision_random_exact_pixel(image_a, image_b):
        TEST_PIXELS_AMOUNT = 3      # later make this % of the block
        for x in range(TEST_PIXELS_AMOUNT):
            test_x = randint(0, ImageCloneDetector.IMAGE_BLOCK_SIZE-1)
            test_y = randint(0, ImageCloneDetector.IMAGE_BLOCK_SIZE-1)
            if not image_a.getpixel((test_x, test_y)) == image_b.getpixel((test_x, test_y)):
                return False

    def _compare_blocks(self):
        blocks = list(self._blocks)

        # BUG need to outpout and duplicates folder if not exist

        while len(blocks) > 0:
            image_block = blocks.pop()
            if ImageCloneDetector.DEBUG_CONSOLE_OUTPUT:
                print('processing left {0}'.format(len(blocks)))

            for num, block in enumerate(blocks):

                if ImageCloneDetector.ENABLE_IC_DIFF_COMPARISION:
                    if self._block_comparison_difference(image_block, block):
                        self._duplicate_blocks.append(image_block)

                        if ImageCloneDetector.DEBUG_CONSOLE_OUTPUT:
                            print('processing {0} of {1}'.format(num, len(blocks)))
                            print('found duplicate block {0}'.format(len(self._duplicate_blocks)))

                        if ImageCloneDetector.SAVE_DUPLICATE_IMAGES_OUTPUT:
                            self._save_image_block_for_debug(image_block,
                                                             'output/duplicates/',
                                                             '{0}.jpg'
                                                             .format(uuid.uuid4()))
                        break

                if ImageCloneDetector.ENABLE_EXACT_PIXEL_COMPARISION:
                    if self._block_comparision_random_exact_pixel(image_block, block):
                        self._duplicate_blocks.append(image_block)

        return self._duplicate_blocks

    def _save_image_block_for_debug(self, image_block, folder, file_name):
        try:
            image_block.save('../{0}/{1}'.format(folder, file_name))
        except SystemError as e:
            pass

    def _split_up_image_into_blocks(self):
        image_width, image_height = self._grey_image.size
        image_width += ImageCloneDetector.IMAGE_BLOCK_SIZE
        image_height += ImageCloneDetector.IMAGE_BLOCK_SIZE

        for x in range(0, image_width, ImageCloneDetector.IMAGE_BLOCK_SIZE):
            for y in range(0, image_height, ImageCloneDetector.IMAGE_BLOCK_SIZE):
                block_top = y
                block_left = x
                block_bottom = y + ImageCloneDetector.IMAGE_BLOCK_SIZE
                block_right = x + ImageCloneDetector.IMAGE_BLOCK_SIZE

                block = (block_left, block_top, block_right, block_bottom)
                image_block = self._grey_image.crop(block)

                self._blocks.append(image_block)

                debug_file_name = '{0}.{1}x{2}.{3}.jpg'.format(block_top, block_left,
                                                               block_bottom, block_right)

                if ImageCloneDetector.DEBUG_CONSOLE_OUTPUT:
                    print('appending block {0}'.format(debug_file_name))

                if ImageCloneDetector.SAVE_BLOCK_IMAGES_OUTPUT:
                    self._save_image_block_for_debug(image_block, 'output/blocks/', debug_file_name)

        return self._blocks

    def _image_avg_hash(self, image):
        image = image.convert("L")  # convert to greyscale (not sure about doing this)
        pixels = list(image.getdata())
        block_size_normalizer = ImageCloneDetector.IMAGE_BLOCK_SIZE * ImageCloneDetector.IMAGE_BLOCK_SIZE   # overhead?
        # avg = sum(pixels) / block_size_normalizer
        avg = sum(pixels)
        return avg

    #OPTIONS
    # avg full block and if averages are similar then go further into detection


    # normalise SUM of rgb (and store true value in hash)
    # SUM = RGB 71039, 47264, 54734

    def _round_up(self, rgb_num):
        NORMALISE_AMOUNT = 100        # this should be some ratio vs block size
        rounded_up = int(math.ceil(rgb_num / NORMALISE_AMOUNT) * NORMALISE_AMOUNT)
        return rounded_up

    def _image_avg_rgb_hash(self, image):
        rgb_data = list(image.getdata())
        red_sum = sum([r for r, g, b in rgb_data])
        blue_sum = sum([b for r, g, b in rgb_data])
        green_sum = sum([g for r, g, b in rgb_data])
        round_up_red_sum = self._round_up(red_sum)
        round_up_blue_sum = self._round_up(blue_sum)
        round_up_green_sum = self._round_up(green_sum)
        return round_up_red_sum, round_up_blue_sum, round_up_green_sum

    # for performance we could always add in both numbers (ie. the rounded up and rounded down version)
    # and have a pure lookup instead?

    def _is_potential_duplicate(self, num_a, num_b):
        if abs(num_a-num_b) < ImageCloneDetector.DUPLICATE_DISTANCE_MINIMUM:
            print('potential duplicate {0} {1} abs {2}'.format(num_a, num_b, abs(num_a-num_b)))
            return True
        return False

    def _is_rgb_potential_duplicate(self, rgb_a, rgb_b):
        min = ImageCloneDetector.DUPLICATE_DISTANCE_MINIMUM
        if abs(rgb_a[0]-rgb_b[0]) < min and \
            abs(rgb_a[1]-rgb_b[1]) < min and \
            abs(rgb_a[2]-rgb_b[2]) < min:
            # print('potential duplicate')
            return True
        return False

    # use OPEN CV histogram comparision

    def _walk_through_image_and_hash_block_compare(self):
        image_width, image_height = self._grey_image.size
        image_width += ImageCloneDetector.IMAGE_BLOCK_SIZE
        image_height += ImageCloneDetector.IMAGE_BLOCK_SIZE

        potential_duplicates = list()
        all_hashes = dict()

        for num, x in enumerate(range(0, image_width, ImageCloneDetector.IMAGE_BLOCK_SIZE)):
            # print('{0} of {1}'.format(num, (image_width/ImageCloneDetector.IMAGE_BLOCKS)))
            for y in range(0, image_height, ImageCloneDetector.IMAGE_BLOCK_SIZE):
                block_top = y
                block_left = x
                block_bottom = y + ImageCloneDetector.IMAGE_BLOCK_SIZE
                block_right = x + ImageCloneDetector.IMAGE_BLOCK_SIZE

                block = (block_left, block_top, block_right, block_bottom)
                # image_block = self._blurred_image.crop(block)
                image_block = self._image.crop(block)
                image_hash = self._image_avg_rgb_hash(image_block)

                # print(image_hash)

                # hash_key = str(list(image_hash))
                hash_key = ''.join(str(x) for x in list(image_hash))
                if hash_key in all_hashes:
                    potential_duplicates.append(image_block)
                    break
                else:
                    all_hashes[hash_key] = None

                # too slow obviously
                # duplicate_found = False
                # for img_hash in all_hashes:
                #     if self._is_rgb_potential_duplicate(image_hash, img_hash):
                #         potential_duplicates.append(image_block)
                #         duplicate_found = True
                #         break
                #
                # if not duplicate_found:
                #     all_hashes.append(image_hash)

        return potential_duplicates

    def execute(self):
        self._image = Image.open(self._file_path)
        self._grey_image = self._image.convert('L')

        self._image.save('../output/image.jpg')

        # SHOULD RESIZE THE IMAGE IN CASE IT'S 12MB or something
        # BLOCK SIZE SHOULD BE RELEVANT TO THE IMAGE SIZE???

        # self._blurred_image = self._grey_image.filter(ImageFilter.SMOOTH_MORE)
        # self._blurred_image = self._image.filter(ImageFilter.GaussianBlur(50))

        # self._blurred_image.save('bllurred.jpg')


        # self._grey_image = Image.open(self._file_path)  # this is colour image!
        # self._grey_image = Image.open(self._file_path).convert('RGB')  # this is colour image!
        # self._blocks = self._split_up_image_into_blocks()
        print(len(self._blocks))
        # duplicates = self._compare_blocks()

        dups = self._walk_through_image_and_hash_block_compare()

        for x, dup in enumerate(dups):
            dup.save('../output/dups/{0}.jpg'.format(x))
        print(len(dups))

if __name__ == "__main__":
    detector = ImageCloneDetector('../Resources/cloned.jpg')
    detector.execute()
    print(detector.json)

