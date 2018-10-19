# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:08:50 2017

@author: Max
"""
#test comment

# -*- coding: utf-8 -*-
"""
Update lat and lon based on street address (ESRI world geocoder)
Created on Mon Dec 18 15:07:28 2017
@author: Max Marno
North Line GIS Inc
"""
 
import arcpy
import os
import sys
import string
import calendar, datetime, traceback
import pandas as pd
import numpy as np
#from arcgis.gis import GIS

os.chdir(r'D:\Projects\TCHD\TCHD_spyder')


try:

    '''
    LOG START TIME
    '''
    d = datetime.datetime.now()
    log = open(r"PythonOutputLogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    # Start process...
    starttime = datetime.datetime.now()
    log.write("Begin process:\n")
    log.write("     Process started at "+ str(starttime) + "\n")
    log.write("\n")
    
    # BEGIN PROCESSING    
    
    
    '''
    LOG COMPLETION TIME
    '''
    endtime = datetime.datetime.now()
    # Process Completed
    log.write("     Completed successfully in "+ str(endtime - starttime) + "\n")
    log.write("\n")
    log.close()
except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Concatenate information together concerning 
    # the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    # LOG AND CLOSE 
    log.write("" + pymsg + "\n")
    log.close()
