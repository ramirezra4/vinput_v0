from cgi import print_arguments
from datetime import date, datetime
from email import header
from bitarray import test
import requests
import pandas as pd

class MMRapi:
    """
    **SECURE: contains hardcoded API key access.**

    Interface with the MMR API (using CULA Key ACCESS).
    Input: VIN #
    Output: MMR ID #

    API Call follows the format below: [Base_URL][DateTime_String][...][VIN].
    As such a large portion of this module is dedicated to formatting that URL.

    Outputs a dictionary of body: vid pairings.
    """

    def __init__(self, vin):
        self.vin = vin

    # public url
    base_url = f"http://cloud.jdpower.ai/data-api/valuationservices/valuation/vehiclesByVin"
    
    # private key: security measures needed for production FIXME
    api_key = 'ee9b1fc6-f3fc-4f14-ae88-2fcb02d2e3ab'

    # datetime object
    dt = datetime.now()

    # year-month
    dt_string_partial = dt.strftime("%y-%m")

    # datetime string passed into url
    dt_string = f'{dt_string_partial}-01'

    # final url
    url = ''
    
    def __init__(self, vin):
        self.vin = vin
        self.url

    # Request MMRAPI, output JSON
    def match(self):
        """
        1. Assemble URL
        2. Define Request params
        3. Make request
        4. Retrieve JSON of matches (dict)
        5. Return dict mapping body -> MID's
        """
        try:
            self.url = f'{self.base_url}?period=0&vin={self.vin}'
            print(self.url)
            r = requests.get(self.url, headers={"api-key": f'{self.api_key}', "accept": "application.json"})
            return r.json()['result'][0]
        except:
            return "MMR API Call Failed."

    def model_year(self):
        """Retrieve Model Year."""
        return self.match()['modelyear']

    def make(self):
        """Retrieve make."""
        return self.match()['make']

    def model(self):
        """Retrieve car model."""
        return self.match()['model']

    def body(self):
        """Retrieve body style."""
        return self.match()['body']
    
    def ugc_vid(self):
        """
        Retrieve UGC Vehicle ID 
        for some reason not readily apparent.
        """
        return self.match()['ucgvehicleid']

    def vid(self):
        """You want the VID? Take it!"""
        return self.match()['vid']

ilx = MMRapi('5UXCR6C09N9M97942')

print(ilx.match())