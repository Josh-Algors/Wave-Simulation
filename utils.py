# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 06:55:24 2019

@author: AHIABA
"""

import os
import time
import numpy as np


def generate_output_name(file_format="png"):
    file_name = "{}.{}".format(int(time.time()), file_format)

    # Replace line below with absolute path to output directory.
    out_dir = r'C:/Users/AHIABA/Desktop'
    return os.path.join(out_dir, file_name), file_name


def rot270(array):
    """
    Rotates a numpy array by 270 degrees.
    :param array:
    :return:
    """
    return np.rot90(np.rot90(np.rot90(array)))
