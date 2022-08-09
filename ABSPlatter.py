# import necessary libraries
from abc import abstractmethod

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
    def platter():
        """Outputs raw RV's."""