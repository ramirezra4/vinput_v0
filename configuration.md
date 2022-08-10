# VINPUT Configuration Steps
## System Requirements and Dependencies (install via pip)
### Recommend installing Anaconda Distribution
* **Python**
* Flask
* pypyodbc
* requests
* datetime
* dateutils
* pandas

## Checklist
1. Install all dependencies to virtual environment containing VINPUT.
2. Open [cnx.py](Cnx.py) and update DRIVER_NAME, SERVER_NAME, DATABASE_NAME and TABLE attributes to connect to SEAMLESS and the correct table mapping ALGResidualNEWIDs to residuals.
3. Update file ALG_US_CHROMEMAP.csv to most recent version available.

# Usage
1. Set app.run(debug=False)
2. Run [api.py](api.py) on your webserver (update host to reflect your server).
3. Input correctly formatted url -> http://your_server/[path&variable_1&variable_2...&variable_n]

## Calls
### Endpoint 1:
* Takes in VIN #
* Returns ALG Code

https://your_server/algcode/vin=<string:vin>

### Endpoint 2:
* Takes in:
    * Vin, State, Contract Date
* Returns Model Year, Vehicle Descriptions (Make, Model, Style), ALG Codes (Make Model Style), RVs

https://your_server/15kresiduals/vin=<string:vin>&state=<string:state>&date=<string:date>

### Endpoint 3:
* Takes in: VIN, State, Contract Date, Term, Annual Mileage Band, MSRP, Inception Miles
* Returns: Model Year, Vehicle Descriptions (Make, Model, Style), ALG Codes (Make Model Style), RV% for that term and mileage band, RV$ that accounts for MRM and inception miles, MRM, Effective Date Range

https://your_server/singledeal/vin=<string:vin>&state=<string:state>&date=<string:date>&mileage_band=<string:mileage_band>&msrp=<string:msrp>&inception_miles=<string:inception_miles>'