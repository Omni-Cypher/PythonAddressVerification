import json
import os
from re import search
import openpyxl
import pycountry
import pymssql
import requests
from textblob import TextBlob
from openpyxl.styles import Font, Color, colors, fills

def verify_address_US(street, street2, city, state, zipcode):

    street.replace(" ", "+")
    street2.replace(" ", "+")
    street_address = street + ' ' + street2
    city.replace(" ", "+")
    state.replace(" ", "+")
    zipcode.replace(" ", "+")

    codes = {
        '200': 'Everything went okay, and the result has been returned (if any).',
        '301': 'The server is redirecting you to a different endpoint. This can happen when a company switches domain names, or an endpoint name is changed.',
        '400': 'The server thinks you made a bad request. This can happen when you don’t send along the right data, among other things.',
        '401': 'The server thinks you’re not authenticated. Many APIs require login credentials, so this happens when you don’t send the right credentials to access an API.',
        '403': 'The resource you’re trying to access is forbidden: you don’t have the right permissions to see it.',
        '404': 'The resource you tried to access wasn’t found on the server.',
        '503': 'The server is not ready to handle the request.'
    }

    key = ''
    auth_id = ''
    auth_token = ''

    req = f'https://us-street.api.smartystreets.com/street-address?auth-id={auth_id}&auth-token={auth_token}&street=' \
          f'{street_address}&city={city}&state={state}&candidates=10'
    req.replace(" ", '%')
    response = requests.get(req)

    response_code = str(response).split()[1].replace('[', '').replace(']', '').replace('>', '')
    # print(f'{error}- {codes.get(error)}')
    # print(f'Req: {req}')

    # loading json data as text dictionary
    response_data = json.loads(response.text)
    print(response_data[0]['errors'])
    if len(response_data) != 0:

        # jprint(response.json())

        # corrected data parsing
        vstreet = f"{response_data[0]['components']['primary_number']} " \
                  f"{response_data[0]['components']['street_name']}"
        print(vstreet)
        try:
            vstreet_suffix = response_data[0]['components']['street_suffix']
        except KeyError:
            vstreet_suffix = ''

        vstreet = f"{vstreet} {vstreet_suffix}"

        if street2 != '':
            try:
                vstreet2 = f"{response_data[0]['components']['secondary_designator']} " \
                           f"{response_data[0]['components']['secondary_number']}"
            except KeyError:
                vstreet2 = f"{response_data[0]['components']['secondary_designator']}"
        else:
            vstreet2 = ''

        vcity = response_data[0]['components']['city_name']
        vstate = response_data[0]['components']['state_abbreviation']
        vzip = response_data[0]['components']['zipcode']

        if (street.lower() == vstreet.lower()) and (city.lower() == vcity.lower()) \
                and (state.lower() == vstate.lower()) and (zipcode.lower() == vzip.lower()):
            print("--------------\nValid Address\n--------------")
        else:
            print("--------------\nCorrected Address\n--------------")
        print(f"{vstreet} {vstreet2}, {vcity}, {vstate} {vzip}")
        return vstreet, vstreet2, vcity, vstate, vzip

    else:
        pass
        # print("--------------\nNo Response\n--------------")
