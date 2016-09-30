import sys
from PIL import Image, ImageFilter, ImageDraw
import operator as op
# from optparse import OptionParser
# import cv2
import os
import json
from PIL import Image, ImageStat, ImageChops, ImageEnhance
import numpy as np
from matplotlib import pyplot as plt
from fractions import Fraction
from decimal import Decimal



class ImageCloneDetector:
    IMAGE_BLOCKS = 200
    SAVE_BLOCK_IMAGES_OUTPUT = True

    def __init__(self, file_path):
        self._file_path = file_path
        self._json_data = list()
        self._image = None

    @property
    def json(self):
        return json.dumps(self._json_data)

    def _compare_blocks(self):
        duplicate_blocks = list()
        for outer_block in self._blocks:
            for inner_block in self._blocks:

                pass
                # if outer_block == inner_block:
                #     duplicate_blocks.append(outer_block)

        return duplicate_blocks

    def _split_up_image_into_blocks(self):
        blocks = list()
        image_width, image_height = self._grey_image.size
        image_width += ImageCloneDetector.IMAGE_BLOCKS
        image_height += ImageCloneDetector.IMAGE_BLOCKS

        for x in range(0, image_width, ImageCloneDetector.IMAGE_BLOCKS):
            for y in range(0, image_height, ImageCloneDetector.IMAGE_BLOCKS):
                block_top = y
                block_left = x
                block_bottom = y + ImageCloneDetector.IMAGE_BLOCKS
                block_right = x + ImageCloneDetector.IMAGE_BLOCKS

                block = (block_left, block_top, block_right, block_bottom)
                image_block = self._grey_image.crop(block)

                if ImageCloneDetector.SAVE_BLOCK_IMAGES_OUTPUT:
                    try:
                        image_block.save('../output/{0}.{1}x{2}.{3}.jpg'
                                         .format(block_top, block_left, block_bottom, block_right))
                    except SystemError as e:
                        pass


        # for y in range(0, image_height + ImageCloneDetector.IMAGE_BLOCKS, ImageCloneDetector.IMAGE_BLOCKS):


            # for x in range(0, image_width + ImageCloneDetector.IMAGE_BLOCKS, ImageCloneDetector.IMAGE_BLOCKS):
            #     block_top = x
            #     block_left = y
            #     block_bottom = x + ImageCloneDetector.IMAGE_BLOCKS
            #     block_right = y + ImageCloneDetector.IMAGE_BLOCKS
            #
            #     # left, top, right, bottom
            #     block = (block_left, block_top, block_right, block_bottom)
            #     image_block = self._grey_image.crop(block)
            #     # print(image_block)
            #     try:
            #         image_block.save('../output/{0}.{1}x{2}.{3}.jpg'.format(block_top, block_left, block_bottom, block_right))
            #     except SystemError as e:
            #         pass
            #     blocks.append(image_block)


                # parts.append(image[x:x+ImageCloneDetector.IMAGE_BLOCKS, y:y+ImageCloneDetector.IMAGE_BLOCKS])

        # parts = sorted(parts)
        return blocks

    def execute(self):
        # self._grey_image = Image.open(self._file_path).convert('L')
        self._grey_image = Image.open(self._file_path)
        self._blurred_image = self._grey_image.filter(ImageFilter.SMOOTH_MORE)
        self._blocks = self._split_up_image_into_blocks()
        duplicates = self._compare_blocks()


if __name__ == "__main__":
    detector = ImageCloneDetector('../Resources/cloned.jpg')
    detector.execute()
    print(detector.json)




