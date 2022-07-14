# import necessary libraries
from abc import abstractmethod
import pandas as pd
import numpy as np
import pypyodbc as dbc
import requests as api

class Platter:
    """
    Platter takes in VIN numbers and serves up a piping hot
    set of residual values.

    In implementing this app I made a couple of important assumptions
    about the peripheral systems involved, namely:

    1. Company server and authentication therein is static.
    2. MMR API authentication key is static.
    3. All information handled is unsecured.

    With those two assumptions I have decided that the configuration for connecting
    to these outside components should be hardcoded. OOP features will abstract logic
    encapsulating authentication so as to allow for future security augmentations to
    be made relatively painlessly.

    Below will be an abstract implementation of the app in general to guide development
    and view at a high level the chain of logic connecting each of the many dependent sources
    to each other to achieve the desired output.
    """

    @abstractmethod
    def get_vin():
        """
        Get a vin or batch of vins. Dresses up batch into useable internal data structure.
        """
        return
    
    @abstractmethod
    def hit_cula():
        """
        Check if there is an existing mapping (VIN -> RV) in CULA database.
        Returns BOOL (True/False).
        """
        return
    
    @abstractmethod
    def hit_mmr():
        """
        Attempts to map VIN to NADA ID via MMR api request in the event there
        is no existing mapping through CULA.
        Returns string = NADA ID#.
        """
        return
    
    @abstractmethod
    def map_nada():
        """
        Attempts to map NADA ID# to RV table in CULA DB. Could augment HIT_CULA().
        Returns RV dataframe.
        """
        return

    @abstractmethod
    def is_used():
        """Returns BOOL indicating whether car (or car in batch) is used."""
        return

    @abstractmethod
    def hit_carfax():
        """
        Hits carfax api to retrieve history on cars that are mapped to RV's.
        Implements logic to adjust RV's depending on factors contained in title.
        """
        return

    @abstractmethod
    def rv_out():
        """Converts mapped RV(s) into desired output format."""
        return
    
    @abstractmethod
    def platter():
        """Outputs raw RV's."""