"""
   ServiceNow Rest API connector
   
I've created this basic script based on the straightforward documentation 
provided by ServiceNow as code sample in the instance REST API Explorer.

In order for this to work on the New York release you first need to create 
a ClientId and optionally a client secret for your python application in 
the ServiceNow System OAuth --> Application Registry.

You then take the cliendId and client secret values and input them in the
variables included in the below script.

The username required for authentication needs to have the itil role assigned
as well as the snc_platform_rest_api_access

This script can be further developed to query other ServiceNow tables as required

I use it mostly to query the ServiceNow table structures from within PowerBI

"""


import servicenow_rest.api as sn #imports custom snow REST API library --> https://github.com/AMMullan/python-servicenow-rest
import requests


s = sn.Client('instance_name.service-now.com', 'user', 'pass')

#Define start and end date
year = 2019
month = 9
startdate = str(year)+"-"+str(month)+"-1"
enddate = str(year)+"-"+str(month)

#Sets the first POST request to the instance sending our OAuth 2.0 token

url_o = "https://cmno.service-now.com/oauth_token.do"
post_body = {
'content_type':'application/json',
'grant_type':'password', 
'client_id':'cl_id', 
'client_secret':'cl_secret',
'username':'user',
'password':'pass'
}
def send_post(url_o,post_body):
    s_post=requests.post(url=url_o,data=post_body)
    json_data = s_post.json()
    print (json_data['access_token'])
    

#Sets the url for GET incidents table
get_body = {
'Authorization':'Bearer',
'Token':'send_post(url_o,post_body)',
}
url="https://cmno.service-now.com/api/now/table/incident?sysparm_query=100"


#Sets proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

#Set up ClientID& Secret for OAuth 2.0 authentication
ClientID = 'cl_id'
Secret = 'cl_secret'

#Pulling incidents from the GET response to our REST API call:
def response(year,month):
    user = ''
    pwd = ''
    response=requests.get(url,auth=(user,pwd),headers=headers,params=get_body)
    json_response = response.json()
    print(json_response)

# Check for HTTP codes other than 200
# if response.status_code != 200: 
    # print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    # exit()

def main():
    year = [[ 2019 ]]
    month = [[ 9 ]]
    send_post(url_o,post_body)
    print(response(year,month))

if __name__ == "__main__":
    main()
