##############################################################################################
#  This Script is devloped for Automation of Halton Generation and creating Halton sample circle
# over urban edge
# 

###################################################################################################


import sys, time, os, win32com.client, glob, arcpy, numpy, random
import ghalton, shapefile, matplotlib.pyplot as plt, numpy as np, arcpy, os.path, ntpath, shutil, glob, os, sys, time
import win32com.client, random
import os.path, ntpath, shutil, glob

from shapely.geometry import Point
from shapely.geometry import asShape
from shapely.geometry import Polygon



print "Congrats all modules and library succesfully imported"

########## Part A: copying and renaming files #############

# input raw data directory: output folder of phase I process

raw_data = r"D:\#Python_script_devlopment\#halton_circle_generation\Input"

output_copy_file = r"D:\#Python_script_devlopment\#halton_circle_generation\Final_inputt"

basepath = os.path.basename

print basepath


# copying urban edge file from respective folder and rename
# all data directories #

all_raw_data = [x[0] for x in os.walk(raw_data)][1:]
if "fGDB.gdb" in x:
        x.remove("fGDB.gdb")

# print all_raw_data

print "\n data dirctory %s ...." %all_raw_data

for current_data_dir in all_raw_data:

    print "\n processing %s...." %basepath(current_data_dir)

    dirname = ntpath.basename(current_data_dir)
    print dirname

    for xx in range(1,4):

        urban_edge = glob.glob(r"%s\%s\*urban_edge_t%d.*" %(raw_data,dirname,xx))

        print urban_edge

        folderpath = r"%s\T%d\%s" %(output_copy_file,xx,dirname)

        print folderpath
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
            for ft in urban_edge:
                shutil.copy(ft,folderpath)
                files = os.listdir(folderpath)
                files_xlsx = [f for f in files if f[:10] == 'urban_edge']
                print files_xlsx
                for root, dir, files in os.walk(folderpath):
                    for f in files_xlsx:
                        print f
                        dirname2 = ntpath.basename(root)
                        ori = root +'/'+f
                        dest = root+'/'+dirname2+f[-4:]
                        print dest
                        os.rename(ori,dest)

#### Copying and renaming file done ####




## Halton Generation ##

urban_edge_raw_data = r"%s\T3" % output_copy_file

reproject_files = r"D:\#Python_script_devlopment\#halton_circle_generation\Reproject_files"

tempWS = r"C:\FloorSpaceTemp"

arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')
arcpy.env.scratchWorkspace = tempWS
arcpy.env.workspace = tempWS
cs = 54052

basepath = os.path.basename

urban_edge_all_raw_data = [x[0] for x in os.walk(urban_edge_raw_data)][1:]

print "\n data dirctory %s ...." %urban_edge_all_raw_data

for current_U_edge in urban_edge_all_raw_data:
    print "\n processing %s...." %basepath(current_U_edge)

    cityname = ntpath.basename(current_U_edge)

    print cityname

    input_file = r"%s\%s.shp" %(current_U_edge,cityname)

    reproject_file = r"%s\%s.shp" %(reproject_files,cityname)
    
    wkt = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
            PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];\
            -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
            0.001;0.001;IsHighPrecision"

    sr = arcpy.SpatialReference(4326)

    #sr.loadFromString(wkt)

    arcpy.Project_management(input_file,reproject_file,sr)

    shp = shapefile.Reader("%s\%s" %(reproject_files,cityname))

    xMin, yMin, xMax, yMax = shp.bbox

    print shp.bbox

    yyMin = yMin  
    yyMax = yMax + 1
    xxMin = xMin 
    xxMax = xMax + 1

    feature_info = [[[xxMin,yyMin],[xxMin,yyMax],[xxMax,yyMax],[xxMax,yyMin]]]

    features = []

    for feature in feature_info:
        features.append(
            arcpy.Polygon(
                arcpy.Array([arcpy.Point(*coords) for coords in feature])))

    
    arcpy.env.overwriteOutput = True
    arcpy.CopyFeatures_management(features, "D:/#Python_script_devlopment/#halton_circle_generation/#reprojection_trial/%s.shp" % cityname )
    
    infc = r"D:/#Python_script_devlopment/#halton_circle_generation/#reprojection_trial/%s.shp" % cityname

    arcpy.DefineProjection_management(infc, sr)

    arcpy.AddField_management(infc,"Area","Double")
    arcpy.CalculateField_management(infc,"Area","!SHAPE.AREA@SQUAREKILOMETERS!","PYTHON_9.3")


    ## Area value extracting from shapefile
    #rows = arcpy.SearchCursor("D:/#Python_script_devlopment/#halton_circle_generation/#reprojection_trial/%s.shp",fields ="Area" % cityname)
    rows = arcpy.SearchCursor(infc,fields ="Area")
    for row in rows:
        bbox_area = row.getValue("Area")

    print " Bounding box area calculated Congrats"

    density_area = bbox_area

    density_points = int(density_area)

   ## if else condition will come here to check
   # urban edge area and decides halton points density
    sequencer = ghalton.Halton(2)
    #npnts = density_points
    npnts = 500  # this is for testing only
    points = sequencer.get(npnts)

    xPoints = [x[1] for x in points]
    yPoints = [y[0] for y in points]

    print "intial xPoints \n %s" % xPoints[0:20]
    print "intial yPoints \n %s" % yPoints[0:20]

    print "last xPoints \n %s" % xPoints[480:]
    print "last yPoints \n %s" % yPoints[480:]

    

    lat = list(np.random.randint(yyMin, yyMax, npnts))
    lon = list(np.random.randint(xxMin, xxMax, npnts))

    print "intial lat %s" % lat[0:20]
    print "intial lon %s" % lon[0:20]

    print "last lat %s" % lat[480:]
    print "last lon %s" % lon[480:]

    

    xHL = [xL + xH for xL, xH in zip(lon, xPoints)]
    yHL = [yL + yH for yL, yH in zip(lat, yPoints)]

    print "intial xHL %s" % xHL[0:20]
    print "intial yHL %s" % yHL[0:20]

    print "last xHL %s" % xHL[480:]
    print "last yHL %s" % yHL[480:]



    
    
    w = shapefile.Writer(shapefile.POINT)

    
    w.autoBalance = 1
    w.field('ID_string', 'N')

    
    #from shapely.geometry import Point
    #from shapely.geometry import asShape

    counter = 0

    for i in range(npnts):
        w.point(xHL[i],yHL[i])
        x_rnd = float(round(xHL[i],1))
        #print "x_rnd %d" %x_rnd
        lon_p = int(round(abs(x_rnd)*100))
        #print lon_p

        if x_rnd >= 0:
            lon_factor = 0
        else:
            lon_factor = 1

        y_rnd = float(round(yHL[i],1))

        lat_p = int(abs(y_rnd)*10000000)

        #print lat_p

        if y_rnd >= 0:
            lat_factor = 0
        else:
            lat_factor = 1

        latt_factor = 100000*lat_factor

        w.record(((i+10001)*1000000000)+ lat_p + latt_factor + lon_p + lon_factor)

        counter +=1

        filename = r"D:\#Python_script_devlopment\#halton_circle_generation\Halton_trial_shp\%s" % cityname
        w.save(filename)
        prj = open("%s.prj" % filename, "w")
        epsg = 'GEOGCS["GCS_WGS_1984",'
        epsg += 'DATUM["D_WGS_1984",'
        epsg += 'SPHEROID["WGS_1984",6378137,298.257223563]]'
        epsg += ',PRIMEM["Greenwich",0.0],'
        epsg += 'UNIT["degree",0.0174532925199433]]'
        prj.write(epsg)
        prj.close()    



    

    

   

   

   

    
    
    

    

    

    

    

    

    

    

    

    
    
    

    
    

    
    



    

    
    

