#By Pablo Iribarren and modified by Duilio Fonseca-Gallardo
#Script to extract dhdt several products.
#This script needs: polygons divides by altitude bands and a raster with data.
import rasterio as rs
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import statistics
from statsmodels import robust
from numpy import nonzero
import scipy

#Data lecture
#Geopackage & Raster
vec= gpd.read_file(r"/home/duilio/Desktop/mocho_50m_bandas/mocho_bandas_50m_porcuenca_32179.gpkg")
data= rs.open(r"/home/duilio/Desktop/mocho_50m_bandas/hugonnet_mocho_32719.tif")
iden= [] # Id list
poly= [] # Numpy matrix list
nmad_bb= [] # Normalized Median Absolute Deviation list
area_pol=[] # Polygon's surface
#Custom Attributes
cod_gla= []#Lista de Codigos glaciar

#Raster Mask
for i in range(vec["geometry"].shape[0]):    
    iout, _ = mask(data, vec.geometry[i], invert=False,crop=True)
    
    #Polygon Surface
    area_pol=vec.geometry[i].area
   
    #pointer
    rs_mask=np.array(iout)
    
    #get non zero data
    values_mask=rs_mask[nonzero(rs_mask)]
    
    #Median Absolute Deviation
    mad=robust.mad(values_mask)
    
    #Normalized Median Absolute Deviation (approximately mad(x)/0.6745)
    nmad=mad/scipy.stats.norm.ppf(3/4.)
    
    #Data Filtering / Statistical treatment
    values_mask[values_mask>mad*3]=np.nan
    values_mask[values_mask<mad*(-3)]=np.nan
    dhdt_pnd=(np.nanmean(values_mask)*area_pol/(vec["AREA_Km2"][i]*(10**6)))
    print(dhdt_pnd)
    
    #Saving Vectors
    poly.append(iout)
    iden.append(vec["fid"][i])
    cod_gla.append(vec["COD_GLA"][i])
    nmad_bb.append(nmad)
