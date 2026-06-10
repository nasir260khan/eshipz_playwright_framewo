import os



UAT_URL = "https://uat.eshipz.com:444"
PROD_URL = "https://app.eshipz.com"

BASE_URL = os.getenv("BASE_URL", UAT_URL)

UAT_EMAIL = "madhuraki27@gmail.com"
UAT_PASSWORD = "password"

PROD_EMAIL = "madhuraki27@gmail.com"
PROD_PASSWORD = "password"

# --- Carrier URLs ---
UAT_CARRIER_URL = "https://uat-carriers.eshipz.com"
PROD_CARRIER_URL = "https://trackmile.eshipz.com"

# --- Carrier Credentials ---
UAT_CARRIER_USERNAME = "bd_carrier"
UAT_CARRIER_PASSWORD = "password"

PROD_CARRIER_USERNAME = "t0054502@gmail.com"
PROD_CARRIER_PASSWORD = "password"