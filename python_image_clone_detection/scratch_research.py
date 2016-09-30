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
    IMAGE_BLOCKS = 15

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
                if outer_block == inner_block:
                    duplicate_blocks.append(outer_block)

        return duplicate_blocks
     #
     #
     #
     #    l = len(imagparts[0])-1
     #
     # for i in range(len(imagparts)-1):
     #  difs = sum(abs(x-y) for x,y in zip(imagparts[i][:l],imagparts[i+1][:l]))
     #  mean = float(sum(imagparts[i][:l])) / l
     #  dev = float(sum(abs(mean-val) for val in imagparts[i][:l])) / l
     #  if dev/mean >= float(opt.blcoldev):
     #   if difs <= int(opt.blsim):
     #    if imagparts[i] not in dupl:
     #     dupl.append(imagparts[i])
     #    if imagparts[i+1] not in dupl:
     #     dupl.append(imagparts[i+1])
     #
     # return dupl

    def _split_up_image_into_blocks(self):
        blocks = list()
        image_width, image_height = self._grey_image.size
        # image = self._grey_image.load()

        for x in range(0, image_width - ImageCloneDetector.IMAGE_BLOCKS, ImageCloneDetector.IMAGE_BLOCKS):
            for y in range(0, image_height - ImageCloneDetector.IMAGE_BLOCKS, ImageCloneDetector.IMAGE_BLOCKS):

                block_top = x * ImageCloneDetector.IMAGE_BLOCKS
                block_left = y * ImageCloneDetector.IMAGE_BLOCKS
                block_right = x + ImageCloneDetector.IMAGE_BLOCKS
                block_bottom = y + ImageCloneDetector.IMAGE_BLOCKS
                block = (block_top, block_left, block_right, block_bottom)
                blocks.append(self._grey_image.crop(block))
                # parts.append(image[x:x+ImageCloneDetector.IMAGE_BLOCKS, y:y+ImageCloneDetector.IMAGE_BLOCKS])

        # parts = sorted(parts)
        return blocks

    def execute(self):
        self._grey_image = Image.open(self._file_path).convert('L')
        self._blurred_image = self._grey_image.filter(ImageFilter.SMOOTH_MORE)
        self._blocks = self._split_up_image_into_blocks()
        duplicates = self._compare_blocks()


if __name__ == "__main__":
    detector = ImageCloneDetector('../Resources/cloned.jpg')
    detector.execute()
    print(detector.json)




