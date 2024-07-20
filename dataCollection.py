import requests

def get_strava_data(access_token, activity_id):
    url = f"https://www.strava.com/activities/{activity_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Example usage
access_token = '2a40545729615984b05904a0733894414f687f7d'
activity_id = '2292639868'  # Replace with your actual activity ID
activity_data = get_strava_data(access_token, activity_id)

if activity_data:
    print(activity_data)

# -------------------------------------------------------------------------

# import requests

# def get_access_token(client_id, client_secret, refresh_token):
#     url = 'https://www.strava.com/oauth/token'
#     payload = {
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token
#     }
#     response = requests.post(url, data=payload)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to refresh token. Status code: {response.status_code}")
#         return None

# def get_strava_data(access_token, activity_id):
#     url = f"https://www.strava.com/api/v3/activities/{activity_id}"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     elif response.status_code == 404:
#         print(f"Activity not found. Status code: {response.status_code}")
#     elif response.status_code == 401:
#         print(f"Unauthorized. Status code: {response.status_code}")
#     else:
#         print(f"Failed to fetch data. Status code: {response.status_code}")
#     return None

# # Example usage
# client_id = '130721'
# client_secret = 'caafd3966bf5e5df54287f26b7efd361d2f1d1de'
# refresh_token = '2da7dc55655bfa048c3c19d0583a7bdd7dbb8da8'
# activity_id = '2292639868'  # Replace with your actual activity ID

# # Refresh the access token
# token_data = get_access_token(client_id, client_secret, refresh_token)
# if token_data:
#     access_token = token_data['access_token']
#     # Fetch the activity data
#     activity_data = get_strava_data(access_token, activity_id)
#     if activity_data:
#         print(activity_data)

# -------------------------------------------------------------------------

# from __future__ import print_function
# import time
# import swagger_client
# from swagger_client.rest import ApiException
# from pprint import pprint

# # Configure OAuth2 access token for authorization: strava_oauth
# swagger_client.configuration.access_token = '2a40545729615984b05904a0733894414f687f7d'  # Replace with your actual access token

# # Create an instance of the API class
# api_instance = swagger_client.ActivitiesApi()
# id = 2292639868  # Replace with your actual activity ID
# includeAllEfforts = True  # To include all segment efforts. (optional)

# try: 
#     # Get Activity
#     api_response = api_instance.getActivityById(id, includeAllEfforts=includeAllEfforts)
#     pprint(api_response)
# except ApiException as e:
#     print("Exception when calling ActivitiesApi->getActivityById: %s\n" % e)
