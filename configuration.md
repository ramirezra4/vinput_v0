# VINPUT Configuration Steps
## System Requirements and Dependencies (install via pip)
* **Python**
* Flask
* pypyodbc
* requests
* datetime
* pandas

## Checklist
1. Install all dependencies to virtual environment containing VINPUT.
2. Open [cnx.py](Cnx.py) and update DRIVER_NAME, SERVER_NAME, DATABASE_NAME and TABLE
    attributes to connect to SEAMLESS and the correct table mapping ALGResidualNEWIDs
    to residuals.
3. Update file ALG_US_CHROMEMAP.csv to most recent version available.

# Usage
1. Run [api.py](api.py) on your webserver (update host to reflect your server).

## Paths
