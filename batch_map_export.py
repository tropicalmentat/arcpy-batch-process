import os
import glob
import arcpy.mapping as mp

#walk through directory and sub-dir
dir_root = "D:\LUIGI\OML\GIS Project Files"
out_dir = "D:\LUIGI\OML\JPEGS WORKING DRAFTS"

count = 1
for root, dirs, files in os.walk(dir_root):
    #ignore .mxd files with keywords
    if 'GROUND TRUTH' in root:
        pass
    elif 'BACKUP' in root:
        pass
    elif 'SCALE' in root:
        pass
    #perform desired operation on .mxd
    else:
        for mapdoc in glob.glob(root+'\*.mxd'):
            if ", Davao" in mapdoc:
                pass
            elif "Davao" in mapdoc or "Iloilo" in mapdoc:
                print '%d. %s' % (count, mapdoc)
                mxd = mp.MapDocument(mapdoc)
                mp.ExportToPNG(mxd, out_dir +
                               '\\' + os.path.basename(mapdoc),resolution=96)               
                del mxd
                count += 1
            
        

