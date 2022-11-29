# -*- coding: utf-8 -*-
"""
Created on Sat Jul  19 2019
@title: TAN Cutouts PSW
@author: Casey Carlile
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
from astropy import units as u
from astropy.coordinates import SkyCoord

#Create Arrays of RA, Dec and Galaxy Number
#Text with coordinates and numbers was opened in excel and saved to separate CSV files.
#Opens csv files and reads contents to a list of strings
with open('RA.csv', 'r') as f:
    reader = csv.reader(f)
    RA_string = list(reader)

with open('DEC.csv', 'r') as g:
    reader = csv.reader(g)
    DEC_string = list(reader)

with open('GalaxyNum.csv', 'r') as h:
    reader = csv.reader(h)
    NUM_string = list(reader)

#Converts list of strings to numpy array of floats or ints
RAdata = np.array(RA_string, dtype = np.float)
DECdata = np.array(DEC_string, dtype = np.float)
NUM = np.array(NUM_string, dtype = np.int)

#opening PSW fits file and using WCS
image = 'PSW_TAN.fits'
print(image)
hdu = fits.open(image)[1]
wcs = WCS(hdu.header)
data = hdu.data
tbh = hdu.header
#print(tbh)

#plotting using WCS
fig = plt.figure()
fig.add_subplot(111, projection=wcs)
plt.imshow(data, origin='lower')
plt.title('Stripe 82x Survey Sky Map')
plt.xlabel('RA')
plt.ylabel('Dec')
plt.show()

#For loop to create cutouts for galaxies 412 and greater.
#Galaxies 1, 2 and 3 are out of the picture so a cutout cannot be created.
#Change range to less than 20 to avoid Runtime Warnings.
for i in range(3, 122):    
    #print(NUM[i])
    #Sets position using RA and Dec coordinates
    sky_position = SkyCoord(RAdata[i]*u.degree, DECdata[i]*u.degree, frame='icrs')
    #Sets size in arcminutes
    size = u.Quantity((5, 5), u.arcmin)
    #Creates cutout
    cutout = Cutout2D(data, position=sky_position, size=size, wcs=wcs, mode='partial')
    #Labels the cutout with the galaxy number
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=cutout.wcs)
    ax.set_title('Galaxy ' + str(NUM[i])[1:-1] + '\n250μm')
    #Labels axes with RA and Dec
    ax.set_xlabel('RA')
    ax.set_ylabel('Dec')
    #Changes axes units to coordinates instead of pixels
    lon = ax.coords[0]
    lat = ax.coords[1]
    lon.set_major_formatter('hh:mm:ss')
    lat.set_major_formatter('dd:mm:ss')
    #Plot marker
    ax.plot_coord(sky_position, "+", color="black")
    #Displays plots
    plt.imshow(cutout.data, origin='lower')
    plt.savefig('Galaxy ' + str(NUM[i])[1:-1] + ' (PSW_TAN).png')
