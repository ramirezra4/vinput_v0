from datetime import date, datetime
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
    """

    # public url
    base_url = f"http://cloud.jdpower.ai/data-api/valuationservices/valuation/vehiclesByVin"
    
    # private key: security measures needed for production
    api_key = 'ee9b1fc6-f3fc-4f14-ae88-2fcb02d2e3ab'

    # datetime object
    dt = datetime.now()

    # year-month
    dt_string_partial = dt.strftime("%y-%m")

    # datetime string passed into url
    dt_string = f'{dt_string_partial}-01'

    _match = ""

    _my = ""
    """Car Model Year"""
    
    _make = ""
    """Car make"""

    _model = ""
    """Car model"""

    _body = ""
    """Body style"""

    _ugcID = ""
    """UGC VID"""

    _vid = ""
    """Vehicle ID"""

    def __init__(self, vin):
        """Initialize MMR API Call."""
        self.vin = vin

    def full_call(self):
        """Return unaltered MMR Call"""
        try:
            self.url = f'{self.base_url}?period=0&vin={self.vin}'  
            r = requests.get(self.url, headers={"api-key": f'{self.api_key}', "accept": "application.json"})
            out = r.json()
            print(out)
            return out
        except:
            print("MMR Call Failed")

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
            # print(self.url)
            r = requests.get(self.url, headers={"api-key": f'{self.api_key}', "accept": "application.json"})
            self._match = r.json()['result'][0]
            self._my = self._match['modelyear']
            self._make = self._match['make']
            self._model = self._match['model']
            self._body = self._match['body']
            self._ugc_vid = self._match['ucgvehicleid']
            self._vid = self._match['vid']
        except:
            print("MMR API Call Failed.")

    def model_year(self):
        """Retrieve Model Year."""
        return self._my

    def make(self):
        """Retrieve make."""
        return self._make

    def model(self):
        """Retrieve car model."""
        return self._model 

    def body(self):
        """Retrieve body style."""
        return self._body 
    
    def ugc_vid(self):
        """
        Retrieve UGC Vehicle ID 
        for some reason not readily apparent.
        """
        return self._ugcID

    def vid(self):
        """You want the VID? Take it!"""
        return self._vid

ilx = MMRapi('5UXCR6C09N9M97942')

ilx.full_call()

