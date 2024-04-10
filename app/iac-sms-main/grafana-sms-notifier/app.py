import logging
import json
import boto3
import traceback
from pprint import pprint
from dateutil import parser
from datetime import datetime, date, timedelta
import pytz
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

START_DATE = date.today()
END_DATE = date.today() + timedelta(days=1)
# iac/env_prod_tooling/grafana_and_oncall/terraform.tfvars - Oncall hostname
MY_ONCALL_API_BASE_URL = "***/api/v1/schedules"
MY_ONCALL_API_KEY = "***"
headers = {"Authorization": MY_ONCALL_API_KEY}
schedule_ids = [schedule["id"] for schedule in requests.get(MY_ONCALL_API_BASE_URL, headers=headers).json()["results"]]
user_on_call_hours = {}
on_duty_ops_dict = {
    "test@test.com": "+36301234567",
}

def lambda_handler(event, context):
    try:
        sns_client = boto3.client('sns',region_name='eu-central-1')
        event_dict = event['body']
        event_json = json.dumps(event_dict)
        sns_client.publish(
            TargetArn='***',
            Message=event_json
        )
        for schedule_id in schedule_ids:
            response = requests.get(f"{MY_ONCALL_API_BASE_URL}/{schedule_id}/final_shifts?start_date={START_DATE}&end_date={END_DATE}",headers=headers)
            for final_shift in response.json()["results"]:
                user_email = final_shift["user_email"]
                shift_start_stg = final_shift["shift_start"]
                shift_start = datetime.fromisoformat(shift_start_stg[:-1])
                datetime_now = datetime.today().replace(microsecond=0)
                if shift_start < datetime_now:
                    for on_duty_ops in on_duty_ops_dict.keys():
                        if user_email == on_duty_ops:
                            logger.info(f"on_duty op is : {user_email} {on_duty_ops_dict[on_duty_ops]}")
                            print(f"on_duty op is : {user_email} {on_duty_ops_dict[on_duty_ops]}")
                            sns_client.publish(
                                PhoneNumber=on_duty_ops_dict[on_duty_ops],
                                Message=event_json
                            )
                            response_data = {
                                'statusCode': 200,
                                'body': event_json
                            }
                            return response_data
    except Exception as e:
        traceback.print_exc()
        response_data = {
            'statusCode': 500,
            'error': str(e)
        }
        return response_data