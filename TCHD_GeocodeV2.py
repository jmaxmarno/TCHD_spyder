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



'''







# -*- coding: utf-8 -*-
"""
Update lat and lon based on street address (ESRI world geocoder)
Created on Mon Dec 18 15:07:28 2017
@author: Max Marno
North Line GIS Inc
"""
import os
import sys
import string
import calendar, datetime, traceback
import pandas as pd
import numpy as np
from arcgis.gis import GIS
from arcgis.geocoding import get_geocoders, batch_geocode
'''
CHANGE TO RELEVANT DIRECTORY
'''
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
file_path = get_script_path()
os.chdir(file_path)
'''
CREATE LOG FILE
'''

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
    '''
    Sign into ArcGIS Online    
    '''
    gis = GIS(url= 'https://www.arcgis.com', username='nlgis_max', password='Onram@north1')
    geocoder = get_geocoders(gis)[0]
    
    '''
    INPUT TABLES
    '''
    facilitiesdf = pd.read_excel(r'D:\Projects\TCHD\TCHD_spyder\Facilities.xlsx')
    septicdf = pd.read_excel(r'D:\Projects\TCHD\TCHD_spyder\Septic.xlsx')
    '''
    DEFINE INPUT FUNCTIONS TO GET X,Y
    '''
    def getxlonfacilites(arow):
        if pd.isnull(arow['GIS_LONGITUDE']) or arow['GIS_LONGITUDE']==-1:        
            addr = "%s %s %s %s %s, %s %s" % (int(arow['STREET_NUMBER'])
            ,arow['STREET_DIRECTION'], arow['STREET_NAME']
            ,arow['STREET_TYPE'],arow['CITY'],arow['STATE'], arow['ZIP'])
            geoaddr = batch_geocode([addr])
            coords = geoaddr[0]['location']
            xlon = coords['x']
            #ylat = coords['y']
            return xlon
        else:
            return arow['GIS_LONGITUDE']
            
    def getylatfacilities(arow):
        if pd.isnull(arow['GIS_LATITUDE']) or arow['GIS_LATITUDE']==-1:        
            addr = "%s %s %s %s %s, %s %s" % (int(arow['STREET_NUMBER'])
            ,arow['STREET_DIRECTION'], arow['STREET_NAME']
            ,arow['STREET_TYPE'],arow['CITY'],arow['STATE'], arow['ZIP'])
            geoaddr = batch_geocode([addr])
            coords = geoaddr[0]['location']
            #xlon = coords['x']
            ylat = coords['y']
            #arow.loc[:,('GIS_LATITUDE')] = ylat
            #arow.loc[:,('GIS_LONGITUDE')] = xlon
            return ylat
        else:
            return arow['GIS_LATITUDE']
    
    def getxlonseptic(arow):
        if pd.isnull(arow['GIS_LONGITUDE']) or arow['GIS_LONGITUDE']==-1:        
            addr = "%s %s %s %s %s, %s %s" % (int(arow['P_STREET_NUMBER'])
            ,arow['P_STREET_DIRECTION'], arow['P_STREET_NAME']
            ,arow['P_STREET_TYPE'],arow['P_CITY'],arow['P_STATE'], arow['P_ZIP'])
            geoaddr = batch_geocode([addr])
            coords = geoaddr[0]['location']
            xlon = coords['x']
            #ylat = coords['y']
            return xlon
        else:
            return arow['GIS_LONGITUDE']
            
    def getylatseptic(arow):
        if pd.isnull(arow['GIS_LATITUDE']) or arow['GIS_LATITUDE']==-1:        
            addr = "%s %s %s %s %s, %s %s" % (int(arow['P_STREET_NUMBER'])
            ,arow['P_STREET_DIRECTION'], arow['P_STREET_NAME']
            ,arow['P_STREET_TYPE'],arow['P_CITY'],arow['P_STATE'], arow['P_ZIP'])
            geoaddr = batch_geocode([addr])
            coords = geoaddr[0]['location']
            xlon = coords['x']
            ylat = coords['y']
            #arow.loc[:,('GIS_LATITUDE')] = ylat
            #arow.loc[:,('GIS_LONGITUDE')] = xlon
            return ylat
        else:
            return arow['GIS_LATITUDE']
            
    '''
    RUN
    '''        
    septicdf['GIS_LATITUDE']= septicdf.apply (lambda row: getylatseptic(row), axis=1)
    septicdf['GIS_LONGITUDE'] = septicdf.apply (lambda row: getxlonseptic(row), axis=1)
    facilitiesdf['GIS_LATITUDE']= facilitiesdf.apply (lambda row: getylatfacilities(row), axis=1)
    facilitiesdf['GIS_LONGITUDE'] = facilitiesdf.apply (lambda row: getxlonfacilites(row), axis=1)
    facilitiesdf.to_csv("Facilities_new.csv")
    septicdf.to_csv("Septic.csv")
    #facilitiesdf.apply (lambda row: list(row), axis=1)
    
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
