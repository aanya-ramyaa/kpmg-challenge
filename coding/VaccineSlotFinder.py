#This tool fetches planned vaccination sessions for a given pincode / area.

import json
import requests

#define url & headers 
cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}"
agent_header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36'}

#define return strings
missing_input = "Missing Date and/or Pincode. Please verify & try again!"
no_slots = "No slots found! Try another date (format: dd-mm-yyyy) or change pincode!"

def check_slots_availability(pincode, date):

    #construct CoWIN API URL using query parameters
    cowin_api  = cowin_url.format(pincode,date)

    #post request to fetch response from CoWIN server
    slot_response = requests.get(cowin_api,headers=agent_header)

    #get response in JSON to check number of slots available
    slot_list = requests.get(cowin_api,headers=agent_header).json()

    #check whether slots are available for given pincode & date
    if (slot_response.ok):

        if (len(slot_list['sessions']) > 0):

            return True

    else:

        return False

def get_slots(pincode, date):

    #construct CoWIN API URL using query parameters
    cowin_api  = cowin_url.format(pincode,date)

    #get response in JSON
    slot_list = requests.get(cowin_api,headers=agent_header).json()

    #initialize slot-details string & add column headers
    slot_details = ''
    slot_details = "{:<30} {:<30} {:<30} {:<30}".format('Centre', 'From Time', 'To Time', 'Vaccine')
    slot_details += '\n'

    #iterate through json slot details & append to slot-details string
    for slots in range(0,len(slot_list['sessions'])) :

        row = ''
        centre = slot_list['sessions'][slots]['name']
        timeFrom = slot_list['sessions'][slots]['from']
        timeTo = slot_list['sessions'][slots]['to']
        vaccine = slot_list['sessions'][slots]['vaccine']
        row = "{:<30} {:<30} {:<30} {:<30}".format(centre,timeFrom,timeTo,vaccine)
        slot_details += '\n'
        slot_details += row

    #return slot details string to user
    return(slot_details) 

def lambda_handler(event, context):

    try:

        #load query strings for pincode & date from event data
        pincode = event['queryStringParameters']['pincode']
        date = event['queryStringParameters']['date']

    except Exception as e:

        print("pincode and/or date missing")
        return missing_input

    else:

        print("checking slots availability..")

        #get vaccination slot details if available
        if (check_slots_availability(pincode, date)):

            print("slots available, getting details..")
            return get_slots(pincode, date)

        else:

            return no_slots                
