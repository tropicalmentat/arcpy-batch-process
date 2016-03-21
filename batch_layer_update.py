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
ins_lyr = mp.Layer("

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
    
    # perform desired operation on .mxd
    else:
        mxd_list = glob.glob(root + '\*mxd')
        
        for mapdoc in mxd_list:
             
            if ", Davao" in mapdoc:
                pass
                       
            elif "Davao City" in mapdoc:
                map_name = os.path.basename(mapdoc).split('.')[0]               
                print '%d. %s' % (count, map_name)

                mxd = mp.MapDocument(mapdoc)

                # save a backup of the mxd
                backup_mxd = os.path.join(backup_dir, map_name + '.mxd')
                print "Saving as %s" % backup_mxd

                shutil.copy(mapdoc, backup_mxd)       

                # update layer                                            
                main_df = mp.ListDataFrames(mxd)[1]
                main_lyrs = mp.ListLayers(mxd, "", main_df)
                src_lyr = None
                   
                for lyr in main_lyrs:
                    lyr_name = lyr.name
                    if "Sea and Lakes" == lyr_name or "Sea" == lyr_name:
                        #print 'yes'
                        #mp.UpdateLayer(main_df, lyr, ref_lyr)
                    else:
                        #print 'no'
                                    

                print '\n'
                del mxd
                count += 1
                

            
        

