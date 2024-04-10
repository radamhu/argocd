import logging
import json
import boto3
import traceback
from pprint import pprint
import csv
import requests
import pprint
pp = pprint.PrettyPrinter(depth=4)

from dateutil import parser
from datetime import datetime, date, timedelta
import pytz

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#session = boto3.Session(profile_name='saml')
#sns_client = session.client('sns',region_name='eu-central-1')
#sns_client = boto3.client('sns',region_name='eu-central-1')
#response = sns_client.list_topics()
#response1 = sns_client.list_subscriptions_by_topic(TopicArn='')
#print(response)
#logger.info(response)
#print(response1)
#logger.info(response1)
#pp.pprint(response1)

ssm = boto3.client('ssm')
myParameter = ssm.get_parameter(Name='common-ops-contacts', WithDecryption=True)
print(myParameter['Parameter']['Value'])

# CUSTOMIZE THE FOLLOWING VARIABLES
START_DATE = date.today()
END_DATE = date.today() + timedelta(days=1)
MY_ONCALL_API_BASE_URL = "https://***/api/v1/schedules"
MY_ONCALL_API_KEY = "***"
headers = {"Authorization": MY_ONCALL_API_KEY}
schedule_ids = [schedule["id"] for schedule in requests.get(MY_ONCALL_API_BASE_URL, headers=headers).json()["results"]]
user_on_call_hours = {}
on_duty_ops_dict = {
    "rolandcsaba.adam@test.com": "+36301234567",
}

print(f'schedule_ids: {type(schedule_ids)}')
print(f'schedule_ids: {schedule_ids}')
logger.info(schedule_ids)

for schedule_id in schedule_ids:
    response = requests.get(f"{MY_ONCALL_API_BASE_URL}/{schedule_id}/final_shifts?start_date={START_DATE}&end_date={END_DATE}", headers=headers)
    #print(f'{MY_ONCALL_API_BASE_URL}/{schedule_id}/final_shifts?start_date={START_DATE}&end_date={END_DATE}')
    # print response 
    #print(response) 
    # print json content 
    #print(response.json()) 
    for final_shift in response.json()["results"]:
        user_email = final_shift["user_email"]
        print(f'user_email: {user_email}')
        shift_start_stg = final_shift["shift_start"]
        shift_start = datetime.fromisoformat(shift_start_stg[:-1])
        datetime_now = datetime.today().replace(microsecond=0)
        print(f"\n")
        print(shift_start < datetime_now)  # 👉️ True or False
        if shift_start < datetime_now:
            print(f'user_email: {type(user_email)}')
            print(f'user_email: {user_email}')
            print(f'shift_start: {type(shift_start)}')
            print(f'shift_start: {shift_start}')
            print(f'datetime_now: {type(datetime_now)}')
            print(f'datetime_now: {datetime_now}')
            for on_duty_ops in on_duty_ops_dict.keys():
                if user_email == on_duty_ops:
                    logger.info(on_duty_ops_dict[on_duty_ops])
                    logger.info(f"on_duty op is : {user_email} {on_duty_ops_dict[on_duty_ops]}")
                    print(f"on_duty op is : {user_email} {on_duty_ops_dict[on_duty_ops]}")