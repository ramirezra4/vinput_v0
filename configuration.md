# VINPUT Configuration Steps
## System Requirements and Dependencies (install via pip)
* **Python**
* Flask
* pyodbc
* requests
* datetime
* pandas

## Checklist
1. Install all dependencies.
2. Open [cnx.py](Cnx.py) and change DRIVER_NAME, SERVER_NAME, DATABASE_NAME and TABLE
    attributes to connect to SEAMLESS and the correct table mapping ALGResidualNEWIDs
    to residuals.
3. Update file ALG_US_CHROMEMAP.csv to most recent version.
4. Drop project directory into  