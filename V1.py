# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:07:28 2017

@author: Max
"""

def testfun():
    print('sucess')
    
import arcpy
import os
import sys
import pandas as pd
from arcgis.gis import GIS
gis = GIS(url= 'https://www.arcgis.com', username='nlgis_max', password='Onram@north1')

arcpy.env.workspace = r'D:\Projects\TCHD\TCHD_spyder'

facilitiesdf = pd.read_excel(r'D:\Projects\TCHD\TCHD_spyder\Facilities.xlsx')
septicdf = pd.read_excel(r'D:\Projects\TCHD\TCHD_spyder\Septic.xlsx')


#
#def returncoords(inputstring):
#    geocoder = gis.tools.geocoder
#    
#    
#geocode('45 ridge road Centennial, WY 82055')
geocoder = gis.tools.geocoder