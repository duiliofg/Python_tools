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
vec= gpd.read_file(r"your_path/file_glacier_boundaries.gpkg")
vec2=vec.copy() #Copy of original shapefile
vec2=vec2.to_crs({'init':'epsg:32719'}) #Change CRS of shapefile copy - its mandatory a CRS with metric units
data= rs.open(r"your_path/geodetic_balance.tif") #loading Raster with geodetic mass balance 
iden= [] # Id list
poly= [] # Numpy matrix list
nmad_bb= [] # Normalized Median Absolute Deviation list
area_pol=[] # Polygon's surface
#Custom Attributes
cod_gla= []#Lista de Codigos glaciar
dhdt=[]
dhdt_mean_ac=[]
#Raster Mask
print("BLOCK 1: START")
for i in range(vec["geometry"].shape[0]): 
    iout, _ = mask(data, vec.geometry[i], invert=False,crop=True)
    
    #Polygon Surface
    area_pol=vec2.geometry[i].area
   
    #pointer
    rs_mask=np.array(iout)
    
    #get non zero data
    values_mask=rs_mask[nonzero(rs_mask)]
    
    #Median Absolute Deviation
    mad=robust.mad(values_mask)
    
    #Normalized Median Absolute Deviation (approximately mad(x)/0.6745)
    nmad=mad/scipy.stats.norm.ppf(3/4.)
    
    #Data Filtering
    values_mask = values_mask[(values_mask <= nmad*3) & (values_mask >= nmad*(-3))]
    #print(values_mask)   s_32719_fix.tif
    #Clear 
    dhdt_pnd=(np.nanmean(values_mask)*area_pol/(vec["<field_with_area_data_in_km2>"][i]*(10**6)))
    dhdt_mean=(np.nanmean(values_mask))
    #print(dhdt_pnd)
    #Saving Vectors
    poly.append(iout)
    iden.append(vec["fid"][i])
    cod_gla.append(vec["<your_id_Glacier_field>"][i])
    nmad_bb.append(nmad)
    dhdt.append(dhdt_pnd)
    dhdt_mean_ac.append(dhdt_mean)
    clear_output(wait=True)
    print(str(i)+" de "+str(range(vec["geometry"].shape[0])))          
# Add vector to geopackage field
vec["dhdt_pnd_bnd"]=dhdt
vec["dhdt_mean_bnd"]=dhdt_mean_ac
vec.to_file("your_results.gpkg", driver="GPKG")
print("BLOCK 1: DONE")
#Results
result_multicode=pd.DataFrame(data=cod_gla,index=iden,columns=['<your_id_Glacier_field>'])
result_multicode.insert(1, "dhdt", dhdt, allow_duplicates=True)
#List of glacier codes
cod_gla_clean=np.unique(cod_gla)
dhdt_per_glacod=[] #output

# Mass balance per glacier
for code in cod_gla_clean:
    dhdt_gl=result_multicode.loc[result_multicode['<your_id_Glacier_field>'] == code]
    dhdt_per_glacod.append(np.nansum(dhdt_gl['dhdt']))
    
print("BLOCK 2: DONE")    
# Output
output=pd.DataFrame(data=cod_gla_clean,index=cod_gla_clean,columns=['<your_id_Glacier_field>'])   
output.insert(1, "dhdt", dhdt_per_glacod, allow_duplicates=True)
output.to_csv('dhdt_output_by_glacier.csv', index=False, encoding='utf-8')
