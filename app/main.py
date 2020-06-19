from flask import Flask, render_template, jsonify, request
from shapely.geometry import Point as Shapely_point, mapping
from geojson import Point as Geoj_point, Polygon as Geoj_polygon, Feature, FeatureCollection
		

#create the app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False



# rendering the index or entry using either of the 3 routes
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	return render_template('index.html')


# the buffer-point implementation/
@app.route('/buffer-point')
def buffer_point():

	# using the request function to get the values of lon, lat, and buf-dist
	lon = request.args.get('lon')
	lat = request.args.get('lat')
	buf_dist = request.args.get('buf-dist')

	# error_res dictionary is used to build the JSON response
	# in case there is an error with lon, lat, or buf_dist values
	error_res = {}

	# check if lon argument value is valid as numeric
	# arguments passed from the API are strings
	try:
		lon = float(lon)
	except ValueError:
		error_res['longitude error'] = 'lon argument should be numeric'
		error_res['value given'] = lon
		return jsonify(error_res)
	
	# check if lon is out of range
	if lon < -180.0 or lon > 180.0:
		error_res['longitude error'] = 'lon argument value out of range. It shoud be between -180.0 and 180.0'
		error_res['value given'] = lon
		return jsonify(error_res)


	# check if lat argument value is valid as numeric
	# arguments passed from the API are strings
	try:
		lat = float(lat)
	except ValueError:
		error_res['latitude error'] = 'lat argument should be numeric'
		error_res['value given'] = lat
		return jsonify(error_res)

	# check if lat is out of range
	if lat < -90.0 or lat > 90.0:
		error_res['latitude error'] = 'lat argument value out of range. It shoud be between -90.0 and 90.0'
		error_res['value given'] = lat
		return jsonify(error_res)


	# check if buf_dist argument value is valid as numeric
	# arguments passed from the API are strings
	try:
		buf_dist = float(buf_dist)
	except ValueError:
		error_res['buffer distance error'] = 'buf_dist argument should be numeric'
		error_res['value given'] = buf_dist
		return jsonify(error_res)

	# check if lat is out of range
	if  buf_dist < 0.001 or buf_dist > 100:
		error_res['buffer distance error'] = 'this API expects a buffer distance less than 100km'
		error_res['value given'] = buf_dist
		return jsonify(error_res)

	
	
	# create a Shapely point
	s_point = Shapely_point(lon,lat)
	# use Shapely buffer function on the created Shapely point to create a buffer polygon
	s_point_buf = s_point.buffer(buf_dist/111)
	# use Shapely mapping function to create a dictionary from the polygon object
	# the dictionary has two keys: type and coordinates
	s_point_buf_dict = mapping(s_point_buf)
	# get the coordinates from the dictionary
	s_point_buf_coords = s_point_buf_dict['coordinates']

	# use the geojson library to create two features: the given point and its buffer
	# 1. the given point, colored red
	pnt_feature = Feature(geometry=Geoj_point((lon,lat)))
	pnt_feature['properties']['name'] = 'API point'
	pnt_feature['properties']['marker-color']='#F00'
	# 2. the buffer polygon, colored blue with fill opacity
	poly_feature = Feature(geometry=Geoj_polygon(s_point_buf_coords))
	poly_feature['properties']['name'] = 'API point buffer'
	poly_feature['properties']['stroke']='#0F0'
	poly_feature['properties']['fill']='#0F0'
	poly_feature['properties']['fill-opacity']= 0.3
	
	# now use both the pnt and the poly to create a feature collection
	feature_col_res = FeatureCollection([pnt_feature,poly_feature])
	
	# finally return the feature collect
	return jsonify(feature_col_res)
	


# main to run app
if __name__ == '__main__':
	app.run(debug = True)
