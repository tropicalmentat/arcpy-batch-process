__author__ = 'G Torres'

# used shutil instead of saveACopy because it:
# does not like having functions in arguments
# does not like overwriting existing mxd with the same name
# throws AttributeError if any of these two things happen

import os
import shutil
import glob
import arcpy.mapping as mp

# reference layer
ref_lyr = mp.Layer("D:\LUIGI\OML\GIS Project Files\BASEMAP DAVAO CITY\Sea and Lakes.lyr")

# walk through directory and sub-dir
dir_root = "D:\LUIGI\OML\GIS Project Files"
out_dir = "D:\LUIGI\OML\JPEGS WORKING DRAFTS"
backup_dir = "D:\LUIGI\OML\GIS Project Files\BACKUP MXD"

count = 1
for root, dirs, files in os.walk(dir_root):
    # work only on the large scale maps 
    if "200000 SCALE" in root:
        mxd_list = glob.glob(root + '\*.mxd')
        lyr_list = glob.glob(root + '\*.lyr')
        
        for mapdoc in mxd_list:
            mdoc_name = os.path.basename(mapdoc).split('.')[0]               
            print '%d. %s' % (count, mdoc_name)

            mxd = mp.MapDocument(mapdoc)

            # save a backup of the mxd
            backup_mxd = os.path.join(backup_dir, mdoc_name + '.mxd')
            print "Saving as %s" % backup_mxd

            shutil.copy(mapdoc, backup_mxd)       

            # update layer                                            
            main_df = mp.ListDataFrames(mxd)[1]
            main_lyrs = mp.ListLayers(mxd, "", main_df)
            src_lyr = None
            ref_lyr = main_lyrs[0]
            
            for lyr in main_lyrs[1:]:
                lyr_name = lyr.name  # get layer name

                # remove layers
                mp.RemoveLayer(main_df, lyr)

            # insert layers from the template map document
            for in_lyr in lyr_list:
                ins_lyr = mp.Layer(in_lyr)
                mp.InsertLayer(main_df, ref_lyr, ins_lyr)

            # save mapdoc
            mxd.save()
            
            # export map
            map_name = os.path.join(out_dir, mdoc_name)
            mp.ExportToPNG(mxd, map_name, resolution=96)
            
            print '\n'
            del mxd
            count += 1
            

        
        

