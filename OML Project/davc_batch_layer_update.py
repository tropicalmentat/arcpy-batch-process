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
ref_lyr = mp.Layer("D:\LUIGI\OML\GIS Project Files\BASEMAP DAVAO CITY\Sea and Lakes.lyr")
ins_lyr = mp.Layer("D:\LUIGI\OML\GIS Project Files\BASEMAP DAVAO CITY\Bathymetric Contours.lyr")

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
            elif "Basemap" in mapdoc:  # ignore Basemap
                pass                       
            elif "Davao City" in mapdoc:
                mdoc_name = os.path.basename(mapdoc).split('.')[0]               
                print '%d. %s' % (count, mdoc_name)

                mxd = mp.MapDocument(mapdoc)

                # save a backup of the mxd
                backup_mxd = os.path.join(backup_dir, mdoc_name + '.mxd')
                print "Saving as %s" % backup_mxd

                #shutil.copy(mapdoc, backup_mxd)       

                # update and insert layer                                            
                main_df = mp.ListDataFrames(mxd)[1]
                main_lyrs = mp.ListLayers(mxd, "", main_df)
                                  
                for lyr in main_lyrs:
                    lyr_name = lyr.name
                    ins_src = ins_lyr.dataSource
                    
                    if "Sea and Lakes" == lyr_name or "Sea" == lyr_name:
                        """
                        print 'Updating %s' % lyr.name
                        mp.UpdateLayer(main_df, lyr, ref_lyr)
                        print 'Inserting %s before %s' % (ins_lyr, lyr)
                        mp.InsertLayer(main_df, lyr, ins_lyr, "BEFORE")
                        """
                        # update sea layer transparency
                        lyr.transparency = 0
                        
                    # update bathymetric contour layer name in the TOC
                    elif lyr.dataSource == ins_src:
                        lyr.name = "Bathymetric Contours (250m intervals)"
                    else:
                        pass
                        #print 'no'

                #save mapdoc
                mxd.save()

                #export map
                map_name = os.path.join(out_dir, mdoc_name)
                print "Exporting %s" % mapdoc
                mp.ExportToPNG(mxd, map_name, resolution=96)
                                    

                print '\n'
                del mxd, lyr
                count += 1

del ref_lyr, ins_lyr

            
        

