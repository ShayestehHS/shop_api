setting_env = 'LOCAL'  # Choices are: LOCAL, PRODUCTION, TEST
# Colors
ENDC = '\033[0m'
WARNING = '\033[93m'
OKGREEN = '\033[92m'
OKCYAN = '\033[96m'
FAIL = '\033[91m'

if setting_env == 'LOCAL':
    from shop_api.settings.local import *
    print(OKCYAN + "-- Local setting imported --" + ENDC)

elif setting_env == 'PRODUCTION':
    from shop_api.settings.production import *
    print(OKCYAN + "-- Production setting imported --" + ENDC)

elif setting_env == "TEST":
    from shop_api.settings.test import *
    print(OKCYAN + "-- Test setting imported --" + ENDC)

else:
    raise Exception(OKCYAN + '-- Invalid setting_env --' + ENDC)

if DEBUG is True:
    mode = FAIL + "ON" + ENDC
else:
    mode = OKCYAN + "OFF" + ENDC

print(OKCYAN + "-- Debug mode is: " + mode + OKCYAN + " --" + ENDC)
