# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 12:21:51 2021

@author: Jola
"""

import pydicom
import os
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans

PathDicom = "./MyHead dataset/"
lastFilesDCM = []  
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower(): 
            lastFilesDCM.append(os.path.join(dirName,filename))
            
dicomLbl = pydicom.read_file(lastFilesDCM[0])

ConstPixelDims = (int(dicomLbl.Rows), int(dicomLbl.Columns), len(lastFilesDCM))

ConstPixelSpacing = (float(dicomLbl.PixelSpacing[0]), float(dicomLbl.PixelSpacing[1]), float(dicomLbl.SliceThickness))

x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])


DicomArray = np.zeros(ConstPixelDims, dtype=dicomLbl.pixel_array.dtype)

print ("Generating image, please wait...")  

for filenameDCM in lastFilesDCM:
    ds = pydicom.read_file(filenameDCM)
    DicomArray[:, :, lastFilesDCM.index(filenameDCM)] = ds.pixel_array  
    
print ("Done!")  
plt.figure(dpi=256)
plt.axes().set_aspect('equal', 'datalim')
plt.pcolormesh(x, y, np.flipud(DicomArray[:, :, 170]))

"-----------------------------------------------------------------------------"



