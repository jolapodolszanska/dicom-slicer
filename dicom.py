# -*- coding: utf-8 -*-
"""
Improved DICOM visualization with key metadata extraction
"""

import pydicom
import os
import numpy as np
import matplotlib.pyplot as plt

PathDicom = "./MyHead dataset/"
lastFilesDCM = []

for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():
            lastFilesDCM.append(os.path.join(dirName, filename))

print(f"Found {len(lastFilesDCM)} DICOM files.")

if len(lastFilesDCM) == 0:
    print("No DICOM files found in the specified directory.")
    exit()

dicomLbl = pydicom.dcmread(lastFilesDCM[0])

print(f"Rows: {dicomLbl.Rows}, Columns: {dicomLbl.Columns}")
print(f"Pixel Spacing: {dicomLbl.PixelSpacing}")
print(f"Slice Thickness: {dicomLbl.SliceThickness}")

ConstPixelDims = (int(dicomLbl.Rows), int(dicomLbl.Columns), len(lastFilesDCM))
ConstPixelSpacing = (
    float(dicomLbl.PixelSpacing[0]),
    float(dicomLbl.PixelSpacing[1]),
    float(dicomLbl.SliceThickness),
)

x = np.arange(0.0, (ConstPixelDims[1]) * ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[0]) * ConstPixelSpacing[1], ConstPixelSpacing[1])

DicomArray = np.zeros(ConstPixelDims, dtype=dicomLbl.pixel_array.dtype)

print("Generating image, please wait...")

for idx, filenameDCM in enumerate(lastFilesDCM):
    ds = pydicom.dcmread(filenameDCM)
    DicomArray[:, :, idx] = ds.pixel_array

print("Done!")

# Wybranie środkowej warstwy do wizualizacji
slice_index = len(lastFilesDCM) // 2
plt.figure(dpi=256)
plt.axes().set_aspect('equal', 'datalim')
plt.pcolormesh(x, y, np.flipud(DicomArray[:, :, slice_index]), cmap="gray")
plt.colorbar(label="Intensity")
plt.title(f"Slice {slice_index}")
plt.show()

print("\nKey DICOM Metadata:")
key_tags = [
    "PatientName", "PatientID", "PatientSex", "PatientAge",
    "StudyDate", "StudyTime", "Modality", "StudyDescription",
    "Manufacturer", "KVP", "XRayTubeCurrent", 
    "PixelSpacing", "SliceThickness", "Rows", "Columns"
]

for tag in key_tags:
    try:
        value = getattr(dicomLbl, tag, "[Not Found]")
        print(f"{tag}: {value}")
    except AttributeError:
        print(f"{tag}: [Attribute not found]")
