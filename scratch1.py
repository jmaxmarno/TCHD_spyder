# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 17:39:55 2017

@author: Max
"""

from arcgis.gis import GIS
from arcgis.geocoding import get_geocoders, batch_geocode

gis = GIS("http://www.arcgis.com", "nlgis_max", "Onram@north1")

# use the first of GIS's configured geocoders
geocoder = get_geocoders(gis)[0]

test = batch_geocode(['Denver, CO'])
print(test[0]['location'])
print(type(test[0]['location']))

'test git gui'
