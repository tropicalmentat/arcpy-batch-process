__author__ = 'G Torres'

# used shutil instead of saveACopy because it:
# does not like having functions in arguments
# does not like overwriting existing mxd with the same name
# throws AttributeError if any of these two things happen

import os
import shutil
import glob
import arcpy.mapping as mp

# reference layers
ref_lyr = mp.Layer("D:\LUIGI\OML\GIS Project Files\BASEMAP ILOILO CITY\Sea and Lakes.lyr")
cont_lyr = mp.Layer("D:\LUIGI\OML\GIS Project Files\BASEMAP ILOILO CITY\Bathymetric Contours.lyr")
bathy_lyr = mp.Layer("D:\LUIGI\OML\GIS Project Files\BASEMAP ILOILO CITY\Bathymetry.lyr")

# walk through directory and sub-dir
dir_root = "D:\LUIGI\OML\GIS Project Files"
out_dir = "D:\LUIGI\OML\JPEGS WORKING DRAFTS"
backup_dir = "D:\LUIGI\OML\GIS Project Files\BACKUP MXD"

count = 1
for root, dirs, files in os.walk(dir_root):
    # ignore .mxd files with keywords
    if 'GROUND TRUTH' in root:
        pass
    elif 'SCALE' in root:
        pass
    elif 'BACKUP' in root:
        pass
    
    # perform desired operations on .mxd
    else:
        mxd_list = glob.glob(root + '\*mxd')
        
        for mapdoc in mxd_list:
             
            if ", Davao" in mapdoc:
                pass
            elif "Basemap" in mapdoc:  # ignore Basemap
                pass                       
            elif "Iloilo Province" in mapdoc:
                mdoc_name = os.path.basename(mapdoc).split('.')[0]               
                print '%d. %s' % (count, mdoc_name)

                mxd = mp.MapDocument(mapdoc)

                # save a backup of the mxd
                backup_mxd = os.path.join(backup_dir, mdoc_name + '.mxd')
                print "Saving as %s" % backup_mxd

                #shutil.copy(mapdoc, backup_mxd)       

                # update and insert bathymetric and contour layers                                            
                main_df = mp.ListDataFrames(mxd)[1]
                main_lyrs = mp.ListLayers(mxd, "", main_df)
                                  
                for lyr in main_lyrs:
                    lyr_name = lyr.name
                    lyr_src = lyr.dataSource
                    cont_src = cont_lyr.dataSource
                    bathy_src = bathy_lyr.dataSource
                    
                    if "Sea and Lakes" == lyr_name or "Sea" == lyr_name:
                        print 'Updating %s' % lyr.name
                        mp.UpdateLayer(main_df, lyr, ref_lyr)
                        if lyr_src == cont_src:
                            pass
                        elif lyr_src == bathy_src:
                            pass
                        else:
                            print 'Inserting %s before %s' % (cont_lyr, lyr)
                            mp.InsertLayer(main_df, lyr, cont_lyr, "BEFORE")

                            print 'Inserting %s after %s' % (bathy_lyr, lyr)
                            mp.InsertLayer(main_df, lyr, bathy_lyr, "AFTER")

                            # modify transparency of Sea and Lakes layer
                            lyr.transparency = 30

                            # modify contour layer TOC name
                            cont_lyr.name = "Bathymetric Contours (250m)"
                            
                # modify legend                                          
                leg_elm = mp.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]

                # remove layers from legend
                for leg_itm in leg_elm.listLegendItemLayers():
                    if leg_itm.dataSource == bathy_src:
                        leg_elm.removeItem(leg_itm)
                    elif leg_itm.name == "Sea and Lakes":
                        leg_elm.removeItem(leg_itm)
                    

                # update position of legend element   
                leg_elm.elementPositionX = 8.8
                leg_elm.elementPositionY = 5.7 - leg_elm.elementHeight
                
                
                #save mapdoc
                #mxd.save()

                #export map
                map_name = os.path.join(out_dir, mdoc_name)
                print "Exporting %s" % mapdoc
                mp.ExportToPNG(mxd, map_name, resolution=96)
                                    

                print '\n'
                del mxd, lyr
                count += 1

del ref_lyr, cont_lyr, bathy_lyr

            
        

