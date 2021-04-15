# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:08:29 2019

@author: AHIABA
"""

import gdal
import math
import numpy as np
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import os
import time

__version__ = '0.1.0'

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


def generate_conditions(input_tiff, initial_angle, wave_period,init_wave_height):
    """
    Accepts Bathymetry data and initial wave conditions, and returns an image of the water region with quiver plots of refraction.
    :param wave_period: Period of the wave in Seconds
    :param input_tiff: Location of the bathymetry data in TIFF format, on disk.
    :param initial_angle: Initial Wave Angle
    :return:
    """
    
    g = 9.81  # Gravity
    initial_angle = np.deg2rad(initial_angle)
    wave_length = g * (wave_period ** 2) / (2 * np.pi)
    initial_celerity = wave_length / wave_period

    gdal_ds = gdal.Open(input_tiff)
    gdal_band = gdal_ds.GetRasterBand(1)
    nodataval = gdal_band.GetNoDataValue()

    grid_size = 50
    data_array = rot270(gdal_ds.ReadAsArray().astype(np.float))
    rows, cols = data_array.shape
    data_array = data_array[
        0 : (rows // grid_size * grid_size), 0 : (rows // grid_size * grid_size)
    ]

    if np.any(data_array == nodataval):
        data_array[data_array == nodataval] = np.nan

    out_full_path, file_name = generate_output_name("png")

    fig = plt.figure(figsize=(25, 20))
    plt.show()
    # Plot contour using matplotlib
    plt.contour(data_array, cmap="viridis", levels=list(range(-1200, 0, 50)))
    plt.colorbar()

    rows, cols = data_array.shape

    # Create a grid representation of depths where each grid is a square of length 'grid_size'
    depths = np.average(
        np.split(
            np.average(
                np.split(data_array, math.ceil(cols / grid_size), axis=1), axis=-1
            ),
            math.ceil(rows / grid_size),
            axis=1,
        ),
        axis=-1,
    )

    # Data is negative to indicate depths, but we need the value of the depths, so convert to positive.
#    depths = np.where(depths < 0, -depths, 0)

    # From formula
    celerity = np.sqrt(g * depths)

    # From formula
    wave_directions = np.arcsin((celerity * np.sin(initial_angle)) / initial_celerity)

    # Replace 'nan' with initial angle.
    wave_directions = np.where(
        np.isnan(wave_directions), initial_angle, wave_directions
    )
    plt.show()
    # Quiver arrows
    U = np.sin(wave_directions)
    V = np.cos(wave_directions)
    
    X, Y = np.meshgrid(np.arange(0, rows, grid_size), np.arange(0, cols, grid_size))
#    fig = plt.figure()
#    plt.subplot
#    plt.show()
    # Plot Quiver diagrams over the contour using matplotlib
    q = plt.quiver(X, Y, U, V)
    plt.quiverkey(q, X=0.3, Y=1.1, U=10, label="Quiver key, length = 10", labelpos="E")
    
    
    # Plot configurations
    plt.gca().set_aspect("equal", adjustable="box")
    plt.savefig(out_full_path, bbox_inches="tight")
    plt.show()                                                                       
    depth_val = "Respective Grid Points for the Wave Heights: "
    return file_name,depth_val,depths
g = 9.81
enter_file_name = input("Enter the directory where the .tif/.netCDF file is saved: ")
g = 9.81
T = float(input('Input Period: '))
Ho = float (input('Input wave height: '))
d = float(input ('Input Depth of water: '))
A= int(input ('Input initial angle: '))
for i in range(int(T),0,-1):
    Lo = float((g * pow(i,2))/(2* math.pi))

    Co = Lo/i
    
    Steepness = Ho/Lo
    U = float((math.pi * Ho)/i)

    
    C = float(math.sqrt(g * d))

    L = float (C * i)

    
    B = math.sin(A * (math.pi/180))
    D = Co/C
    E = B * D
    Alpha = Co*math.sin(A)/C
    
    Kr = round(math.sqrt(math.cos(A * math.pi/180)/math.cos(Alpha * math.pi/180)),2)

    Ks = round(math.sqrt(Co/(2*C)),2)

    H = Ho * round(Kr,2) * round(Ks,2)
        
    print("Wave Period\t\tWave Height\t\tCoeff of Shaoling\t\tWL(Deep-Water)\t\tWL(Shallow-Water)\t\tAngle between Crests")
    print(i,"\t\t\t",H,"\t\t\t",round(Ks,3),"\t\t\t",round(Lo,3),"\t\t\t",round(L,3),"\t\t\t",math.degrees(Alpha))
print("Coefficient of Refraction= ",round(Kr,3))
print ('Final Wave Height = ',H)
result = generate_conditions(enter_file_name,A,T,Ho)
print(result)
print("The Final Wave Height: ",H)