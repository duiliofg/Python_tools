def mask_tiff(folder_path,tif_name,gpkg_mask_path,out_path,suffix):
    """
    By Duilio Fonseca
    2023-05-01
    This function mask a tiff file with a single polygon (shapefile and geopackage format).
    Example:
    folder_path= r"C:\Users\Administrador\Desktop\climate_permafrost\tas_chelsa"
    tif_name="CHELSA_tas_01_2019_V.2.1"
    out_path=r"C:\Users\Administrador\Desktop\climate_permafrost\tas_chelsa\masked_files"
    suffix='_masked'
    gpkg_mask_path=r"C:\Users\Administrador\Desktop\climate_permafrost\mask\chile_mask_wgs84.gpkg"
    -> mask_tiff(folder_path,tif_name,gpkg_mask_path,out_path,suffix)
    """
    import fiona
    import rasterio
    import rasterio.mask
    
    with fiona.open(gpkg_mask_path, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    tif_path=os.path.join(folder_path,tif_name+".tif")
    delivery_path=os.path.join(out_path,tif_name+suffix+".tif")
    with rasterio.open(tif_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})    

    with rasterio.open(delivery_path, "w", **out_meta) as dest:
        dest.write(out_image)
    
    print(tif_name+" is masked")
   # return out_meta
