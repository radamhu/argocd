import requests 

from requests.auth import HTTPBasicAuth 

URL = "https://my/api/call" 
PWD = "mypwd" 
USER = "theUser" 

def test_post_and_get_data(): 
    data= [ 
        { 
        'startDate': '2022-02-12', 
        'endDate': '2022-02-22', 
        } 
    ] 
 
    r = requests.post(URL, json=data, auth=HTTPBasicAuth(USER, PWD)) 
    assert r.status_code == 200 
    r= requests.get(URL, auth=HTTPBasicAuth(USER, PWD)) 
    assert r.status_code == 200 
    reply = r.json() 
    assert reply[0]["startDate"] == '2022-02-12'
    