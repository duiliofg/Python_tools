def chelsa_mask(txt_path,output_path,gpkg_mask_path):
  
    """
    By Duilio Fonseca
    2023-05-12
    This function allows you to download and mask CHELSEA climatological files with a single polygon. 
    It is designed to avoid the collapse of your storage capacities. The function will create
    two folders in your output_path (temp and processed). The results are stored in outputpath/processed.
    Example:
    
    txt_path=r"C:\Users\Administrador\Desktop\climate_permafrost\envidatS3paths.txt"
    output_path=r"D:\CHELSA"
    gpkg_mask_path=r"C://Users//Administrador//Desktop//climate_permafrost//mask//chile_mask_wgs84.gpkg"

    chelsa_mask(txt_path,output_path,gpkg_mask_path)
  
    Requisites:
    wget-subprocess-rasterio-fiona
    
    tested in Windows
    """
    import os
    import subprocess
    
    def mask_tiff(folder_path,tif_name,gpkg_mask_path,out_path):
        # """
        # By Duilio Fonseca
        # 2023-05-01
        # This function mask a tiff file with a single polygon (shapefile and geopackage format).
        # Example:
        # folder_path= r"C:\Users\Administrador\Desktop\climate_permafrost\tas_chelsa"
        # tif_name="CHELSA_tas_01_2019_V.2.1"
        # out_path=r"C:\Users\Administrador\Desktop\climate_permafrost\tas_chelsa\masked_files"
        # gpkg_mask_path=r"C:\Users\Administrador\Desktop\climate_permafrost\mask\chile_mask_wgs84.gpkg"
        # mask_tiff(folder_path,tif_name,gpkg_mask_path,out_path)
        # """
        import fiona
        import rasterio
        import rasterio.mask
        import os
        
        with fiona.open(gpkg_mask_path, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]

        tif_path=os.path.join(folder_path,tif_name)
       
        # Mask the raster
        delivery_path=os.path.join(out_path,tif_name)
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

    def runcmd(cmd, verbose = False, *args, **kwargs):

        process = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            shell = True
        )
        std_out, std_err = process.communicate()
        if verbose:
            print(std_out.strip(), std_err)
        pass
    
    masked_path = os.path.join(output_path,"processed")
    temp_path=os.path.join(output_path,"temp")
    

    if not os.path.exists(masked_path):
        os.makedirs(masked_path)
    if not os.path.exists(temp_path):        
        os.makedirs(temp_path)

    f = open(txt_path, "r")
    for x in f:
        try:
            basename = os.path.basename(x)
            command="wget -P "+ temp_path+" "+x
            tif_name=basename
            tif_name=tif_name[0:-2]
            ## wget
            
            if not os.path.exists(os.path.join(temp_path,tif_name)):
                print('Downloading:'+tif_name)
                runcmd(command, verbose = True)
            else:
                print(tif_name+' already exists a previous version')
            
            ## masking
            
            if not os.path.exists(os.path.join(masked_path,tif_name)):
                print('Masking '+tif_name)
                mask_tiff(temp_path,tif_name,gpkg_mask_path,masked_path)
            else:
                print(tif_name+' already exists a previous masked version')

            ## Delete temporal files
            del_path=os.path.join(temp_path,tif_name)
            os.remove(del_path)
        except:
            print('Sorry the process failed')
            pass

