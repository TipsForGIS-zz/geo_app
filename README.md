# geo_app

This is a Python Flask application server. The purpose of this app is to illustrate how a geospatial API can be created in Flask. The geospatial API creates a buffer polygon of a given lon and lat values with buffer distance in KM. The response of the API is a GeoJSON file containing both the given point and the created buffer using the buffer distance given.


This is an example of the API endpoint for an area in Malé, Maldives and a buffer distance of 25 KM:

http://127.0.0.1:5000/buffer-point?lon=73.51&lat=4.17&buf-dist=25

