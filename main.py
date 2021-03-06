#!/usr/bin/env python3.6
"""
Carter Frost
For hosting a website for Santa Cruz Map for businesses a virtual downtown shopping experience,
making it easier for locals to support local businesses.
"""

import requests
import requests_cache
from flask import Flask
import json
import csv
from flask_cors import CORS

# TODO: Use something like celery.schedules to update data
# TODO: separate in into separate functions with timers to update fields instead of waiting for a request

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CACHE_TYPE'] = 'simple'

#  run on import
requests_cache.install_cache("/tmp/sczmapCache", expire_after=6000, backend='sqlite', )
global retail_data, business_id_group, businesses, ride_out_the_wave_dict, dining_data, groups_dict


def init():
    print("init function called")
    global retail_data, business_id_group, businesses, ride_out_the_wave_dict, dining_data, groups_dict
    retail_data = dict()
    business_id_group = dict()
    businesses = dict()
    ride_out_the_wave_dict = dict()
    dining_data = dict()
    groups_dict = dict()


@app.route('/', methods=['GET'])
def main():
    return json.dumps(businesses)


@app.route('/googleformupdate', methods=['GET'])
def fupdate():
    print("fupdate function called")
    global businesses
    content = {'header': "", 'header_link': "",
               'subheader1': "", '': "",
               'subheader2': "", 'subheader2_link': "",
               'subheader3': "", 'subheader3_link': ""}
    pictures = ["", "", "", ""]

    gift_card_link = ""
    online_order_link = ""

    csv_url = 'https://docs.google.com/spreadsheets/d/1aCrPNN8GxowAwFjAo56SPBPmR24-iV9GLjnnGAu66O4/export?format=csv' \
              '&id=1aCrPNN8GxowAwFjAo56SPBPmR24-iV9GLjnnGAu66O4&gid=1716473960 '
    with requests.Session() as s:
        download = s.get(csv_url)
        decoded_content = download.content.decode('utf-8')
        form_data = list(csv.reader(decoded_content.splitlines(), delimiter=','))[1:]
        for business in dining_data:
            for business_row in form_data:
                if business['properties']['point_name'] == business_row[1]:
                    businesses[business['properties']['point_id']] = ({'DTA_data': business,
                                                                       'group': groups_dict[business_id_group[
                                                                           str(business['properties']['point_id'])]] if
                                                                       business['properties'][
                                                                           'point_id'] in business_id_group else
                                                                       groups_dict['1'],
                                                                       'type': 'dining',
                                                                       'images': [business_row[6], business_row[7],
                                                                                  business_row[8], business_row[9],
                                                                                  business_row[10]],
                                                                       'online_order_link': business_row[3],
                                                                       'gift_card_link': ride_out_the_wave_dict[
                                                                           business_row[1]] if business_row[1] in
                                                                                               ride_out_the_wave_dict
                                                                       else gift_card_link,
                                                                       'content': {'header': business_row[2],
                                                                                   'header_link': business_row[3],
                                                                                   'subheader1': business_row[4],
                                                                                   'subheader1_link': business_row[5],
                                                                                   }})

            if business['properties']['point_id'] not in businesses:
                businesses[business['properties']['point_id']] = ({'DTA_data': business,
                                                                   'group': groups_dict[business_id_group[
                                                                       str(business['properties']['point_id'])]] if
                                                                   business['properties'][
                                                                       'point_id'] in business_id_group else
                                                                   groups_dict['1'],
                                                                   'type': 'dining',
                                                                   'images': pictures,
                                                                   'online_order_link': online_order_link,
                                                                   'gift_card_link': ride_out_the_wave_dict[
                                                                       business_row[1]] if business_row[1] in
                                                                                           ride_out_the_wave_dict else
                                                                   gift_card_link,
                                                                   'content': content})
        for business in retail_data:
            for business_row in form_data:
                if business['properties']['point_name'] == business_row[1]:
                    businesses[business['properties']['point_id']] = ({'DTA_data': business,
                                                                       'group': groups_dict[business_id_group[
                                                                           str(business['properties']['point_id'])]] if
                                                                       business['properties'][
                                                                           'point_id'] in business_id_group else
                                                                       groups_dict['4'],
                                                                       'type': 'retail',
                                                                       'images': [business_row[6], business_row[7],
                                                                                  business_row[8], business_row[9],
                                                                                  business_row[10]],
                                                                       'online_order_link': business_row[3],
                                                                       'gift_card_link': ride_out_the_wave_dict[
                                                                           business_row[1]] if business_row[1] in
                                                                                               ride_out_the_wave_dict
                                                                       else gift_card_link,
                                                                       'content': {'header': business_row[2],
                                                                                   'header_link': business_row[3],
                                                                                   'subheader1': business_row[4],
                                                                                   'subheader1_link': business_row[5],
                                                                                   }})
            if business['properties']['point_id'] not in businesses:
                businesses[business['properties']['point_id']] = ({'DTA_data': business,
                                                                   'group': groups_dict[business_id_group[
                                                                       str(business['properties']['point_id'])]] if
                                                                   business['properties']['point_id'] in
                                                                   business_id_group else groups_dict['4'],
                                                                   'type': 'retail',
                                                                   'images': pictures,
                                                                   'online_order_link': online_order_link,
                                                                   'gift_card_link': ride_out_the_wave_dict[
                                                                       business_row[1]] if business_row[1] in
                                                                                           ride_out_the_wave_dict
                                                                   else gift_card_link,
                                                                   'content': content})
    return "Got it"


@app.route('/rupdate', methods=['GET'])
def rupdate():
    print("rupdate function called")
    global ride_out_the_wave_dict
    ride_out_the_wave_data = requests.get(url="https://rotwsc.s3-us-west-1.amazonaws.com/data/latest.json").json()[
        'results']
    # @Note: change rotw_business['gift_card_link'] to rotw_business if we want to use ride the wave's data
    ride_out_the_wave_dict = {rotw_business['name']: rotw_business['gift_card_link'] for rotw_business in
                              ride_out_the_wave_data if 'Santa Cruz'
                              in rotw_business['town']}
    return "Done"


@app.route('/update', methods=['GET'])
def update():
    print("update function called")
    global dining_data, retail_data, groups_dict
    dining_data = requests.get(url="https://downtownsantacruz.com/_api/v2/covid-dining.json").json()
    retail_data = requests.get(url="https://downtownsantacruz.com/_api/v2/covid-retail.json").json()
    group_data = requests.get("https://downtownsantacruz.com/_api/v2/groups.json").json()
    # Remap the list as a dictionary as the keys in the provided API have no meaning, discarding those keys and the
    # group type. Group dict's keys will be the group id and the value will be the properties
    groups_dict = {group['properties']['group_id']: group['properties'] for group in group_data}

    points_base_group_url = "https://downtownsantacruz.com/_api/v2/points.json?m=10&group="
    for group in groups_dict.keys():
        group_businesses = requests.get(points_base_group_url + str(group)).json()
        for business in group_businesses:
            if business['properties']['point_id'] not in business_id_group:  # \
                # or ( int(groups_dict[str(group)]['group_depth']) >
                # int(business_id_group[business['properties']['point_id']]['group_depth'])):
                business_id_group[business['properties']['point_id']] = group
    return "Done"


@app.route('/groups', methods=['GET'])
def groups():
    global business_id_group
    return json.dumps(business_id_group)


@app.route('/static/<name>')
def resource(name):
    """Load a file from the static directory and return it to the browser."""
    with open('static/' + name, 'rb') as f:
        return f.read()


@app.errorhandler(500)
def server_error(e):
    """ Just that it is an error handler"""
    print("I've Done Borked Up", e)
    return "I've Done Borked Up", 500


#  also run on import
init()
rupdate()
update()
fupdate()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
