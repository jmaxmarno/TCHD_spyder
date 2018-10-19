#-------------------------------------------------------------------------------
# Name:        TCHD Facility and Septic Address Geocode
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
'''
WORKSPACE AND ENVIRONMENT SETUP:
'''
#THIS WILL DETERMINE WHERE THE OUTPUT LOG IS WRITTEN
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
file_path = get_script_path()
# REPLACE 'file_path' WITH DESIRED DIRECTORY FOR OUTPUT LOG IF DIFFERENT FROM SCRIPT LOCATION
os.chdir(file_path)
StagingGDB = os.path.join(file_path, "Staging.gdb")
if not arcpy.Exists(StagingGDB):
    arcpy.CreateFileGDB_management(out_folder_path=file_path, out_name="Staging", out_version="CURRENT")
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = StagingGDB
arcpy.env.workspace = StagingGDB
locator = "I:\\IEPH\\Software\\ESRI\\ESRI_StreetMap\\Locators\\USA_StreetAddress.loc"
facility_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY"
septic_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_SEPTIC_ONSITE_SYSTEM"
'''
GEOCODE FACILITY TABLE AND OUTPUT TO STAGING.GDB
'''
# BACKUP EXISTING TABLE:
arcpy.CopyRows_management(facility_table, "FACILITYCOREBACKUP")
# SELECT ROWS WITH NULL LAT OR LON
arcpy.TableSelect_analysis(in_table=facility_table, out_table="nullGeoRows", where_clause="GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL")
arcpy.AddField_management("nullGeoRows", "STREETADDRESS", "TEXT")
arcpy.CalculateField_management(in_table="nullGeoRows", field="STREETADDRESS"
, expression="addrcat( !STREET_NUMBER!, !STREET_DIRECTION!, !STREET_NAME!, !STREET_TYPE!)"
, expression_type="PYTHON_9.3"
, code_block='def addrcat(snum, sdir, sname, stype):\n    snum = str(snum)\n    sdir = str(sdir)\n    sname = str(sname)\n    stype = str(stype)\n    streetaddress = ""\n    if len(snum)>0 and snum != "None":\n        streetaddress = streetaddress+snum\n    if len(sdir)>0 and sdir != "None":\n        streetaddress = streetaddress+" "+sdir\n    if len(sname)>0 and sname != "None":\n        streetaddress = streetaddress + " " + sname\n    if len(stype)>0 and stype != "None":\n        streetaddress = streetaddress + " " + stype\n    return streetaddress')


facility_fields = "STREETADDRESS;CITY;STATE;ZIP"
arcpy.GeocodeAddresses_geocoding("nullGeoRows", locator, facility_fields, "Facility_geocode", 'STATIC')




'''
I:\IEPH\Software\ESRI\ESRI_StreetMap\Locators\USA_StreetAddress.loc





'''
'''
fields to update
Geocode State - text field






'''
'''
SNIPPETS
arcpy.GetCount_management(in_rows="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY")
arcpy.GetCount_management(in_rows="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_SEPTIC_ONSITE_SYSTEM")



C:\Users\cwhite\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\Connection to EnvisionDB.sde


arcpy.TableSelect_analysis(in_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY", out_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/testselect", where_clause="GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL")


arcpy.TableSelect_analysis(in_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY", out_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/testselect2", where_clause="(GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL) AND (STREET_NAME NOT LIKE 'Mobile')")
arcpy.CalculateField_management(in_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/nullGeoRows", field="STREETADDRESS", expression="addrcat( !STREET_NUMBER!, !STREET_DIRECTION!, !STREET_NAME!, !STREET_TYPE!)", expression_type="PYTHON_9.3", code_block='def addrcat(snum, sdir, sname, stype):\n    snum = str(snum)\n    sdir = str(sdir)\n    sname = str(sname)\n    stype = str(stype)\n    streetaddress = ""\n    if len(snum)>0 and snum != 'None':\n        streetaddress = streetaddress+snum\n    if len(sdir)>0 and sdir != 'None':\n        streetaddress = streetaddress+" "+sdir\n    if len(sname)>0 and sname != 'None':\n        streetaddress = streetaddress + " " + sname\n    if len(stype)>0 and stype != 'None':\n        streetaddress = streetaddress + " " + stype\n    return streetaddress')


this one still won't omit the 'do not use'
arcpy.TableSelect_analysis(in_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY", out_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/testselect4", where_clause="(GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL) AND (STREET_NAME NOT LIKE 'Mobile') AND ( FACILITY_NAME NOT LIKE 'not use')")

'''


