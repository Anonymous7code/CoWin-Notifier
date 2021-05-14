# Importing Libraries

import requests
import time
from datetime import datetime, timedelta


# Define your requirments
age = 50
# Pass your pincode You may pass multiple pincode in for of list
pincode = ['']
number_days = 5       # Max of 7 days supported
p_flag = 'Y'

actual = datetime.today()
list_format = [actual + timedelta(days=x) for x in range(number_days)]

actual_dates = [x.strftime('%d%m%y') for x in list_format]
print(actual_dates)

print('Starting search for Vaccine Slots...')

while True:
    count = 0
    for pinCode in pincode:
        for dates in actual_dates:

            url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(
                pinCode, dates)

            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            results = requests.get(url, headers=header)
            # print(results.text)
            if results.ok:
                json_response = results.json()

                flag = False
                if json_response['centers']:
                    if(p_flag.lower() == 'y'):
                        for center in json_response['centers']:
                            # print(center)
                            for session in center['sessions']:
                                if (session['min_age_limit'] <= age and session['available_capacity'] >= 1):
                                    print('Pincode: ' + pinCode)
                                    print("Available on: {}".format(dates))
                                    print("\t", center["name"])
                                    print("\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ",
                                          session["available_capacity"])
                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine type: ",
                                              session["vaccine"])
                                    print("\n")

                                    count = count + 1

                                else:
                                    pass
                else:
                    pass

            else:
                print("No Response!")

    if(count == 0):
        print("No Vaccination slot avaliable!")
    else:
        print("Search Completed!")

        dt = datetime.now() + timedelta(minutes=3)

        while datetime.now() < dt:
            time.sleep(1)
