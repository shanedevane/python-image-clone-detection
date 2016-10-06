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



class ImageCloneDetector:
    IMAGE_BLOCKS = 15
    SAVE_BLOCK_IMAGES_OUTPUT = False
    DEBUG_CONSOLE_OUTPUT = True

    def __init__(self, file_path):
        self._file_path = file_path
        self._json_data = list()
        self._image = None
        self._blocks = list()
        self._duplicate_blocks = list()

    @property
    def json(self):
        return json.dumps(self._json_data)

    def _compare_blocks(self):
        blocks = list(self._blocks)

        # BUG need to outpout and duplicates folder if not exist

        while len(blocks) > 0:
            image_block = blocks.pop()
            if ImageCloneDetector.DEBUG_CONSOLE_OUTPUT:
                print('processing left {0}'.format(len(blocks)))

            for num, block in enumerate(blocks):
                try:
                    if IC.difference(image_block, block).getbbox() is None:
                        self._duplicate_blocks.append(block)
                        if ImageCloneDetector.DEBUG_CONSOLE_OUTPUT:
                            print('processing {0} of {1}'.format(num, len(blocks)))
                            print('found duplicate block {0}'.format(len(self._duplicate_blocks)))

                        if ImageCloneDetector.SAVE_BLOCK_IMAGES_OUTPUT:
                            self._save_image_block_for_debug(image_block,
                                                             'output/duplicates/',
                                                             '{0}.jpg'
                                                             .format(uuid.uuid4()))
                        break
                except:
                    print('exception {0}'.format(sys.exc_info()[0]))
        return self._duplicate_blocks

    def _save_image_block_for_debug(self, image_block, folder, file_name):
        try:
            image_block.save('../{0}/{1}'.format(folder, file_name))
        except SystemError as e:
            pass

    def _split_up_image_into_blocks(self):
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

                self._blocks.append(image_block)

                debug_file_name = '{0}.{1}x{2}.{3}.jpg'.format(block_top, block_left,
                                                               block_bottom, block_right)

                if ImageCloneDetector.DEBUG_CONSOLE_OUTPUT:
                    print('appending block {0}'.format(debug_file_name))

                if ImageCloneDetector.SAVE_BLOCK_IMAGES_OUTPUT:
                    self._save_image_block_for_debug(image_block, 'output/blocks/', debug_file_name)

        return self._blocks

    def execute(self):
        # self._grey_image = Image.open(self._file_path).convert('L')
        self._grey_image = Image.open(self._file_path)  # this is colour image!
        # self._blurred_image = self._grey_image.filter(ImageFilter.SMOOTH_MORE)
        self._blocks = self._split_up_image_into_blocks()
        duplicates = self._compare_blocks()


if __name__ == "__main__":
    detector = ImageCloneDetector('../Resources/cloned.jpg')
    detector.execute()
    print(detector.json)




