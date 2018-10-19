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
import psutil
#THIS WILL DETERMINE WHERE THE OUTPUT LOG IS WRITTEN AND WHERE THE STAGING.GDB IS PLACED (SAME DIRECTORY/FOLDER AS THE SCRIPT)
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
file_path = get_script_path()
arcpy.env.overwriteOutput = True
file_path = "D:\\Projects\\TCHD\\TCHD_spyder"
# REPLACE 'file_path' DEFINTION WITH DESIRED DIRECTORY IF DIFFERENT FROM SCRIPT LOCATION
###############################################################################
#CREATE STAGING FGDB
StagingGDB = os.path.join(file_path, "Staging.gdb")
if not arcpy.Exists(StagingGDB):
    arcpy.CreateFileGDB_management(out_folder_path=file_path, out_name="Staging.gdb", out_version="CURRENT")
###############################################################################
finaloutputgdb = StagingGDB
finaloutputgdb = "D:\\Projects\\TCHD\\TCHD_spyder\\MockSDE.gdb"
#finaloutputgdb = "Database Connections\\SA_srvarcgis.sde"
#finaloutputgdb = "C:\\Users\\cwhite\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\SA_sqlexpress.sde"
sourcedb = "D:\\Projects\\TCHD\\TCHD_spyder\\MockDB.gdb"
#sourcedb = "Database Connections\\Connection to EnvisionDB.sde"
#sourcedb = "C:\\Users\\cwhite\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\Connection to EnvisionDB.sde"
defaultgdb = StagingGDB
arcpy.env.scratchWorkspace = defaultgdb
arcpy.env.workspace = defaultgdb

###############################################################################
# SOURCE DATA
locator = "D:\\Projects\\TCHD\\TCHD_spyder\\ArapahoeLocator\\ArapahoeLocator.loc"
#locator = "I:\\IEPH\\Software\\ESRI\\ESRI_StreetMap\\Locators\\USA_StreetAddress"

facility_path="FACILITY"
#facility_path = "EnvisionConnect_Live.dba.TB_CORE_FACILITY"
septic_path="SEPTIC"
#septic_path = "EnvisionConnect_Live.dba.TB_SEPTIC_ONSITE_SYSTEM"
tchd_address_path = "TCHD_ADDRESS"
#tchd_address_path = "EnvisionConnect_Live.dba.uvw_TCHD_Addresses" 

facility_table = os.path.join(sourcedb, facility_path)
septic_table = os.path.join(sourcedb, septic_path)
TCHD_ADDRESS = os.path.join(sourcedb, tchd_address_path)
facilitiesstaging = os.path.join(StagingGDB, "Facilities_Staging")
violationsstaging = os.path.join(StagingGDB, "Violations_Staging")
facilitiesfinal = os.path.join(finaloutputgdb, "FACILITIES")
violationsfinal = os.path.join(finaloutputgdb, "VIOLATIONS")
facilitiesviolations_relationship = os.path.join(finaloutputgdb, "FACILITIES_VIOLATIONS")
###############################################################################
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
try:
    #if arcpy.Exists(finaloutputgdb):
        #arcpy.Compress_management(finaloutputgdb)
    #if arcpy.Exists(facilitiesfinal) & arcpy.Exists(violationsfinal):
        #arcpy.RebuildIndexes_management(finaloutputgdb, "NO_SYSTEM", [facilitiesfinal, violationsfinal], "ALL" )
        #arcpy.AnalyzeDatasets_management(finaloutputgdb, "NO_SYSTEM", [facilitiesfinal, violationsfinal],"ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE" )
##############################################################################
    # NEW TABLE(TO DELETE DUPLICATE RECORDS)
    if arcpy.Exists("FACILITIES_TABLE"):
        arcpy.Delete_management("FACILITIES_TABLE")
    arcpy.TableToTable_conversion(in_rows=TCHD_ADDRESS, out_name="FACILITIES_TABLE", out_path=defaultgdb) 
    arcpy.management.DeleteIdentical(in_dataset="FACILITIES_TABLE", fields="FACILITY_ID")
    if arcpy.Exists("TCHD_ADDRESS"):
        arcpy.Delete_management("TCHD_ADDRESS")
    arcpy.TableToTable_conversion(in_rows=TCHD_ADDRESS, out_name="TCHD_ADDRESS", out_path=defaultgdb)
    
    ###############################################################################
    # SELECT ROWS WITH NULL LAT OR LON and vice versa
    # CREATE TARGET FACILITIES FC IF DOESN'T EXIST ALREADY IN OUTPUT GDB AND (ONLY ROWS WITH LAT AND LON)
    arcpy.TableSelect_analysis(in_table="FACILITIES_TABLE"
    , out_table="nullGeoRows"
    , where_clause="(GIS_LATITUDE IS NULL OR GIS_LONGITUDE IS NULL ) AND (Upper(NAME) NOT LIKE '%DO NOT USE%') AND (Upper(STREET_NAME) NOT LIKE '%Mobile%')")
    arcpy.TableSelect_analysis(in_table="FACILITIES_TABLE"
    , out_table="FACILITIESw_GEOM"
    , where_clause="(GIS_LATITUDE IS NOT NULL) AND (GIS_LONGITUDE IS NOT NULL ) AND (Upper(NAME) NOT LIKE '%DO NOT USE%')")
    
        
    ###############################################################################    
    # GEOCODE NECESSARY ROWS
    address_fields = "Street ConcatAddress;ZIP ZIP"
    #address_fields="'Street or Intersection' ConcatAddress VISIBLE NONE;'City or Placename' CITY VISIBLE NONE;State STATE VISIBLE NONE;'ZIP Code' ZIP VISIBLE NONE"
    if arcpy.Exists("GeocodedAddresses"):
        arcpy.Delete_management("GeocodedAddresses")
    arcpy.GeocodeAddresses_geocoding(in_table="nullGeoRows"
    , address_locator=locator, in_address_fields=address_fields
    , out_feature_class="GeocodedAddresses")
    #    RECLASS '0' LAT AND LON TO NONE
    def GEO0(inputfc):
        with arcpy.da.UpdateCursor(inputfc, field_names = ["Y", "X"]) as gcursor:
            for arow in gcursor:
                if arow[0]==0:
                    arow[0]=None
                    arow[1]=None
                    gcursor.updateRow(arow)
        del gcursor
        del arow
        
    GEO0("GeocodedAddresses")
    
    ###############################################################################
    #    NESTED CURSORS TO UPDATE FACILITY TABLE
    with arcpy.da.SearchCursor("GeocodedAddresses",["FACILITY_ID","Status", "Score", "X", "Y"]) as search_cur:
        for search_row in search_cur:
            with arcpy.da.UpdateCursor("FACILITIES_TABLE",["FACILITY_ID","UDF_RESULTCODE", "UDF_MATCHCODE", "GIS_LONGITUDE", "GIS_LATITUDE"]) as upd_cur:
                for upd_row in upd_cur:
                    if upd_row[0] == search_cur[0]:
                        upd_row[1] = search_row[1]
                        upd_row[2] = search_row[2]
                        upd_row[3] = search_row[3]
                        upd_row[4] = search_row[4]
                        upd_cur.updateRow(upd_row)
    del search_cur
    del search_row
    del upd_cur
    
    # CREATE FINAL FACILITIES FEATURE CLASS FROM UPDATED FACILITIES TABLE AND VIOLATIONS TABLE
    if arcpy.Exists(facilitiesstaging):
        arcpy.Delete_management(facilitiesstaging)
    arcpy.MakeXYEventLayer_management(table="FACILITIES_TABLE", in_x_field="GIS_LONGITUDE", in_y_field="GIS_LATITUDE", out_layer="FACILITIESw_GEOM_Layer", spatial_reference=arcpy.SpatialReference(4326))
    arcpy.CopyFeatures_management(in_features="FACILITIESw_GEOM_Layer", out_feature_class=facilitiesstaging)
    if arcpy.Exists(violationsstaging):
        arcpy.Delete_management(violationsstaging)    
    arcpy.TableSelect_analysis(in_table=TCHD_ADDRESS, out_table=violationsstaging, where_clause="Total_Critical IS NOT NULL")
    arcpy.management.DeleteIdentical(in_dataset=violationsstaging, fields="RECORD_ID")
    # REMOVE UNNECESSARY FIELDS FROM VIOLATIONS TABLE
    vfields = ['OBJECTID', 'FACILITY_ID', 'RECORD_ID', 'ACCOUNT_ID', 'NAME', 'EMPLOYEE', 'JURISDICTION', 'PE', 'PE_DESC', 'LastRoutineDate', 'SERIAL_NUMBER', 'Total_Critical']
    for i in arcpy.ListFields(violationsstaging):
        if i.name not in vfields:
            arcpy.DeleteField_management(violationsstaging, i.name)
    # DELETE ALL FIELDS THAT CONTAIN THE TEXT 'Edit'
    def deleteeditfields(inputfc):
        for i in arcpy.ListFields(inputfc):
            if 'Edit' in i.name:
                arcpy.DeleteField_management(facilitiesfinal, i.name)
    deleteeditfields(facilitiesstaging)
    deleteeditfields(violationsstaging)
    if not arcpy.Exists(facilitiesfinal):
        arcpy.Copy_management(facilitiesstaging, facilitiesfinal)
    if not arcpy.Exists(violationsfinal):
        arcpy.Copy_management(violationsstaging, violationsfinal)
    arcpy.DeleteRows_management(facilitiesfinal)
    arcpy.DeleteRows_management(violationsfinal)
    ffieldmappings = arcpy.FieldMappings()
    ffieldmappings.addTable(facilitiesfinal)
    arcpy.Append_management(facilitiesstaging, facilitiesfinal, schema_type="NO_TEST", field_mapping= ffieldmappings)
    vfieldmappings = arcpy.FieldMappings()
    vfieldmappings.addTable(violationsfinal)
    arcpy.Append_management(violationsstaging, violationsfinal, schema_type="NO_TEST", field_mapping= vfieldmappings)        
        
    ###############################################################################  
    # CREATE RELATIONSHIP CLASS IF NOT EXISTS
    if not arcpy.Exists(facilitiesviolations_relationship):
        arcpy.CreateRelationshipClass_management(origin_table=facilitiesfinal
        , destination_table=violationsfinal
        , out_relationship_class=facilitiesviolations_relationship, relationship_type="SIMPLE"
        , forward_label="VIOLATIONS", backward_label="FACILITIES", message_direction="NONE"
        , cardinality="ONE_TO_MANY", attributed="NONE", origin_primary_key="FACILITY_ID"
        , origin_foreign_key="FACILITY_ID", destination_primary_key="", destination_foreign_key="")
        
        
        
        
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
    
    
