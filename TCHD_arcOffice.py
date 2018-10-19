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
import calendar, datetime, traceback
#THIS WILL DETERMINE WHERE THE OUTPUT LOG IS WRITTEN
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
file_path = get_script_path()
print(file_path)
# REPLACE 'file_path' WITH DESIRED DIRECTORY FOR OUTPUT LOG IF DIFFERENT FROM SCRIPT LOCATION
try:
    # LOG START TIME
    d = datetime.datetime.now()
    log = open("PythonOutputLogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    # Start process...
    starttime = datetime.datetime.now()
    log.write("Begin process:\n")
    log.write("     Process started at "+ str(starttime) + "\n")
    log.write("\n")

    # WORKSPACE AND ENVIRONMENT SETUP:'''
    StagingGDB = os.path.join(file_path, "Staging.gdb")
    if not arcpy.Exists(StagingGDB):
        arcpy.CreateFileGDB_management(out_folder_path=file_path, out_name="Staging", out_version="CURRENT")
    arcpy.env.overwriteOutput = True
    arcpy.env.scratchWorkspace = StagingGDB
    arcpy.env.workspace = StagingGDB
    locator = "D:/Projects/TCHD/TCHD_spyder/ArapahoeLocator/ArapahoeLocator.loc"
    facility_table="D:/Projects/TCHD/TCHD_spyder/MockDB.gdb/FACILITY"
    septic_table="D:/Projects/TCHD/TCHD_spyder/MockDB.gdb/SEPTIC"
    
    # DUMMY SOME NULL LAT AND LON ROWS
    ffields = ['OBJECTID', 'GIS_LATITUDE', 'GIS_LONGITUDE']
    with arcpy.da.UpdateCursor(facility_table, ffields) as fcursor:
        for row in fcursor:
            if (row[0]<11):
                row[1] = None
                row[2] = None
            fcursor.updateRow(row)
    
    
    
    
    
    #    GEOCODE FACILITY TABLE AND OUTPUT TO STAGING.GDB
    
    # BACKUP EXISTING TABLE:
    arcpy.CopyRows_management(facility_table, "FACILITYCOREBACKUP")
    # SELECT ROWS WITH NULL LAT OR LON
    arcpy.AddField_management(facility_table, "STREETADDRESS", "TEXT")
    arcpy.TableSelect_analysis(in_table=facility_table
    , out_table="nullGeoRows"
    , where_clause="( GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL ) AND (Upper(FACILITY_NAME) NOT LIKE '%DO NOT USE%') AND (Upper(STREET_NAME) NOT LIKE '%Mobile%')")
    #arcpy.TableSelect_analysis(in_table="D:/Projects/TCHD/TCHD_spyder/MockDB.gdb/FACILITY", out_table="D:/Projects/TCHD/TCHD_spyder/MockDB.gdb/FACILITY_TableSelect", where_clause="( GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL ) AND (Upper(FACILITY_NAME) NOT LIKE '%DO NOT USE%') AND ( STREET_NAME NOT LIKE 'Mobile')")
    def addrcat(snum, sdir, sname, stype):
        snum = str(snum)
        sdir = str(sdir)
        sname = str(sname)
        stype = str(stype)
        streetaddress = ""
        if len(snum)>0 and snum != 'None':
            snum = str(int(float(snum)))
            streetaddress = streetaddress+snum
        if len(sdir)>0 and sdir != 'None':
            streetaddress = streetaddress+" "+sdir
        if len(sname)>0 and sname != 'None':
            streetaddress = streetaddress + " " + sname
        if len(stype)>0 and stype != 'None':
            streetaddress = streetaddress + " " + stype
        return streetaddress
    with arcpy.da.UpdateCursor(facility_table
    , field_names=['OBJECTID', 'GIS_LATITUDE', 'GIS_LONGITUDE', 'STREET_NUMBER'
    , 'STREET_DIRECTION', 'STREET_NAME', 'STREET_TYPE', 'ZIP', 'STREETADDRESS']) as cursor:
        for row in cursor:
            row[-1] = addrcat(row[3], row[4], row[5], row[6])
            cursor.updateRow(row)
    # GEOCODE - PAY CLOSE ATTENTION TO ADDRESS FIELDS SYNTAX
    
    facility_fields = "Street STREETADDRESS;ZIP ZIP"
    arcpy.GeocodeAddresses_geocoding(in_table="nullGeoRows"
    , address_locator=locator, in_address_fields=facility_fields
    , out_feature_class="GeocodedAddresses", out_relationship_type="STATIC")
    
    #    RECLASS '0' LAT AND LON TO NONE
    
    with arcpy.da.UpdateCursor("GeocodedAddresses", field_names = ["Y", "X"]) as gcursor:
        for arow in gcursor:
            if arow[0]==0:
                arow[0]=None
                arow[1]=None
                gcursor.updateRow(arow)
    
    #    NESTED CURSORS TO UPDATE THE ORIGINAL FACILITY TABLE
     
    with arcpy.da.SearchCursor("GeocodedAddresses",["USER_FACILITY_ID","Status", "Score", "X", "Y"]) as search_cur:
        for search_row in search_cur:
            with arcpy.da.UpdateCursor(facility_table,["FACILITY_ID","GEOCODESTATE", "UDF_MATCHCODE", "GIS_LONGITUDE", "GIS_LATITUDE"]) as upd_cur:
                for upd_row in upd_cur:
                    if upd_row[0] == search_cur[0]:
                        upd_row[1] = search_row[1]
                        upd_row[2] = search_row[2]
                        upd_row[3] = search_row[3]
                        upd_row[4] = search_row[4]
                        upd_cur.updateRow(upd_row)
    
    
        #    LOG COMPLETION TIME

    endtime = datetime.datetime.now()
    # Process Completed
    log.write("     Completed successfully in "+ str(endtime - starttime) + "\n")
    log.write("\n")
    ##################################################################################
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

    
    #
    #for i in arcpy.ListFields(facility_table):
    #    print(i.name)
    
    
    
    
    
    
    
    #'''
    #I:\\IEPH\\Software\\ESRI\\ESRI_StreetMap\\Locators\\USA_StreetAddress.loc
    #
    #'''
    #
    #'''
    #fields to update
    #Geocode State - text field
    #
    #
    #
    #
    #
    #
    #'''
    #'''
    #SNIPPETS
    #arcpy.GetCount_management(in_rows="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY")
    #arcpy.GetCount_management(in_rows="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_SEPTIC_ONSITE_SYSTEM")
    #
    #
    #
    #C:\Users\cwhite\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\Connection to EnvisionDB.sde
    #
    #
    #arcpy.TableSelect_analysis(in_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY", out_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/testselect", where_clause="GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL")
    #
    #
    #arcpy.TableSelect_analysis(in_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY", out_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/testselect2", where_clause="(GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL) AND (STREET_NAME NOT LIKE 'Mobile')")
    #arcpy.CalculateField_management(in_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/nullGeoRows", field="STREETADDRESS", expression="addrcat( !STREET_NUMBER!, !STREET_DIRECTION!, !STREET_NAME!, !STREET_TYPE!)", expression_type="PYTHON_9.3", code_block='def addrcat(snum, sdir, sname, stype):\n    snum = str(snum)\n    sdir = str(sdir)\n    sname = str(sname)\n    stype = str(stype)\n    streetaddress = ""\n    if len(snum)>0 and snum != 'None':\n        streetaddress = streetaddress+snum\n    if len(sdir)>0 and sdir != 'None':\n        streetaddress = streetaddress+" "+sdir\n    if len(sname)>0 and sname != 'None':\n        streetaddress = streetaddress + " " + sname\n    if len(stype)>0 and stype != 'None':\n        streetaddress = streetaddress + " " + stype\n    return streetaddress')
    #
    #
    #this one still won't omit the 'do not use'
    #arcpy.TableSelect_analysis(in_table="Database Connections/Connection to EnvisionDB.sde/EnvisionConnect_Live.dba.TB_CORE_FACILITY", out_table="E:/Projects/TCHD/TCHD_spyder/Staging.gdb/testselect4", where_clause="(GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL) AND (STREET_NAME NOT LIKE 'Mobile') AND ( FACILITY_NAME NOT LIKE 'not use')")
    #
    #'''
    

