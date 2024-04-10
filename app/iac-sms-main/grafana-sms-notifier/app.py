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
MY_ONCALL_API_BASE_URL = "https://oncall.tooling.prod.vbg.aws.de.vodafone.com/api/v1/schedules"
# MY_ONCALL_API_KEY = "c2861db783f9eb7148b80652efc983803db611840a30c5f7b1a55dcec29d59ab"
# test API key 7d54b24081ab7b723ce91292cd7d54487b58fc2edb67c55303f128f0a1b7503b
MY_ONCALL_API_KEY = "7d54b24081ab7b723ce91292cd7d54487b58fc2edb67c55303f128f0a1b7503b"
headers = {"Authorization": MY_ONCALL_API_KEY}
schedule_ids = [schedule["id"] for schedule in requests.get(MY_ONCALL_API_BASE_URL, headers=headers).json()["results"]]
user_on_call_hours = {}
on_duty_ops_dict = {
    "attila.fabrik@vodafone.com": "+4915209770910",
    "rolandcsaba.adam@vodafone.com": "+36304723089",
    "laurikristian.gombos@vodafone.com": "+36706659419",
    "daniel.dudek@vodafone.com": "+491722520156",
    "philipp.clemens@vodafone.com": "+491773291683",
    "duchuan.nguyen@vodafone.com": "+491743149800",
    "marc.zimmermann@vodafone.com": "+4915736510414",
    "soufian.ayadi@vodafone.com": "+36304723089"
}

def lambda_handler(event, context):
    try:
        sns_client = boto3.client('sns',region_name='eu-central-1')
        event_dict = event['body']
        event_json = json.dumps(event_dict)
        sns_client.publish(
            TargetArn='arn:aws:sns:eu-central-1:161646829058:grafana-sms-notifier',
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