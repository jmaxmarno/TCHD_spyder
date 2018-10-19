# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:14:55 2018

@author: Max
"""

#
#-------------------------------------------------------------------------------
# Name:        TCHD Facility Geocode and Violations relate
# Purpose:
#
# Author:      Max Marno
#
# Created:     08/01/2018
# Copyright:   Max Marno
#              North Line GIS LLC

import os
import sys
import arcpy
import calendar, datetime, traceback
#THIS WILL DETERMINE WHERE THE OUTPUT LOG IS WRITTEN AND WHERE THE STAGING.GDB IS PLACED (SAME DIRECTORY/FOLDER AS THE SCRIPT)
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
file_path = get_script_path()
#file_path = "D:\\Projects\\TCHD\\TCHD_spyder"
# REPLACE 'file_path' DEFINTION WITH DESIRED DIRECTORY IF DIFFERENT FROM SCRIPT LOCATION
###############################################################################
#CREATE STAGING FGDB
StagingGDB = os.path.join(file_path, "Staging.gdb")
if not arcpy.Exists(StagingGDB):
    arcpy.CreateFileGDB_management(out_folder_path=file_path, out_name="Staging.gdb", out_version="CURRENT")
arcpy.env.overwriteOutput = True
###############################################################################
#finaloutputgdb = StagingGDB
#finaloutputgdb = "D:\\Projects\\TCHD\\TCHD_spyder\\MockSDE.gdb"
#finaloutputgdb = "Database Connections\\SA_srvarcgis.sde"
finaloutputgdb = "C:\\Users\\cwhite\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\SA_sqlexpress.sde"
#sourcedb = "D:\\Projects\\TCHD\\TCHD_spyder\\MockDB.gdb"
#sourcedb = "Database Connections\\Connection to EnvisionDB.sde"
sourcedb = "C:\\Users\\cwhite\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\Connection to EnvisionDB.sde"
defaultgdb = StagingGDB
arcpy.env.scratchWorkspace = defaultgdb
arcpy.env.workspace = defaultgdb

###############################################################################
# SOURCE DATA
#locator = "D:\\Projects\\TCHD\\TCHD_spyder\\ArapahoeLocator\\ArapahoeLocator.loc"
locator = "I:\\IEPH\\Software\\ESRI\\ESRI_StreetMap\\Locators\\USA_StreetAddress"

#facility_path="FACILITY"
facility_path = "EnvisionConnect_Live.dba.TB_CORE_FACILITY"
#septic_path="SEPTIC"
septic_path = "EnvisionConnect_Live.dba.TB_SEPTIC_ONSITE_SYSTEM"
#tchd_address_path = "TCHD_ADDRESS"
tchd_address_path = "EnvisionConnect_Live.dba.uvw_TCHD_Addresses" 

facility_table = os.path.join(sourcedb, facility_path)
septic_table = os.path.join(sourcedb, septic_path)
TCHD_ADDRESS = os.path.join(sourcedb, tchd_address_path)
facilitiesstaging = os.path.join(StagingGDB, "Facilities_Staging")
violationsstaging = os.path.join(StagingGDB, "Violations_Staging")
facilitiesfinal = os.path.join(finaloutputgdb, "FACILITIES")
violationsfinal = os.path.join(finaloutputgdb, "VIOLATIONS")
facilitiesviolations_relationship = os.path.join(finaloutputgdb, "FACILITIES_VIOLATIONS")
###############################################################################
d = datetime.datetime.now()
log = open("LogTest.txt","a")
log.write("----------------------------" + "\n")
log.write("----------------------------" + "\n")
log.write("Log: " + str(d) + "\n")
log.write("\n")
# Start process...
starttime = datetime.datetime.now()
log.write("Begin process:\n")
log.write("     Process started at "+ str(starttime) + "\n")
log.write("\n")
try:
#    arcpy.Compress_management(finaloutputgdb)
#    arcpy.RebuildIndexes_management(finaloutputgdb, "NO_SYSTEM", [facilitiesfinal, violationsfinal], "ALL" )
#    arcpy.AnalyzeDatasets_management(finaloutputgdb, "NO_SYSTEM", [facilitiesfinal, violationsfinal],"ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE" )
    # LOG START TIME


##############################################################################


        
        
###############################################################################    
        #    LOG COMPLETION TIME

    endtime = datetime.datetime.now()
    # Process Completed
    log.write("     Completed successfully in "+ str(endtime - starttime) + "\n")
    log.write("\n")
    # Close Log
    log.close()
except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Concatenate information together concerning
    # the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    # Return python error messages for use in
    # script tool or Python Window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    # LOG AND CLOSE
    log.write("" + pymsg + "\n")
    log.write("Failed @" +str(d))
    log.close()
###############################################################################
    
    
