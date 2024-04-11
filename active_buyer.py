import pandas as pd
import requests
import io
import time

import requests
import os.path

import datetime
from datetime import timedelta

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Scope for the google api to work with googlesheets


# Google API Dependencies

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



### GOOGLE SHEETS API CALLS Function Setups ###

def get_values(spreadsheet_id, range_name):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    # pylint: disable=maybe-no-member
    
    try:
        
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        return result
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def update_values(spreadsheet_id, range_name, value_input_option,
                  values):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    
    try:

        service = build('sheets', 'v4', credentials=creds)
        
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error



def main():
      
      ### Google Sheets Credentials Setup ###

      global creds
      creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
      if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'...\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
      
      
      # Use your own spreadsheet id and range name

      checker = get_values(spreadsheet_id='spread_id', range_name='range')  # Ex range: Sheetname!A1:A1
      number_of_rows_list = checker['values']
      number_of_rows = int(number_of_rows_list[0][0])     # This is the number of rows in the spreadsheet
      print(number_of_rows)                               
      number_of_rows += 1
      number_of_rows = str(number_of_rows)
      print(number_of_rows)
      
      

     ### METABASE ###

     # First URL after http is your metabase server, you can check this from settings in the metabase. Also, VPN should be open.

      ### LOGIN ###

      response = requests.post('http://metabase.com/api/session', # Use your own metabase url
                              json={'username': 'your_username',
                                    'password': 'your_password'})
      print(response)
      session_id = response.json()['id']
      headers = {'X-Metabase-Session': session_id}   # This is the session id for the user so you can access the data without relogging in


      ### API CALLS ###

      on_public = requests.post('http://metabase.com/api/card/card_id_1/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel = pd.read_csv(io.BytesIO(response))
      
      #############################################################
      
      on_public = requests.post('http://metabase.com/api/card/card_id_2/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel2 = pd.read_csv(io.BytesIO(response))

      ###############################################################
      
      on_public = requests.post('http://metabase.com/api/card/card_id_3/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel3 = pd.read_csv(io.BytesIO(response))

      #################################################################

      on_public = requests.post('http://metabase.com/api/card/card_id_4/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel4 = pd.read_csv(io.BytesIO(response))
      
      #############################################################
     
      # For checking if any of the dataframes are empty if any empty wait 5 seconds and try again
      
      excel_list = [excel, excel2, excel3, excel4]
      for i in excel_list:
            if i.empty:
                  time.sleep(5)
                  main()
      

     ### Column Renaming for Data Merging ### (Change column names to your needs)

      excel2.rename(columns={'column_x':'column_rename'},inplace=True)
      extract = excel2['column_rename']
      excel = excel.join(extract)
      
      excel3.rename(columns={'column_y':'column_rename'}, inplace=True)
      extract = excel3['column_rename']
      excel = excel.join(extract)

      excel4.rename(columns={'column_z':'column_rename'},inplace=True)
      extract = excel4['column_rename']
      excel = excel.join(extract)


       ### Deleting Public Links ### 

      off_public = requests.delete('http://metabase.com/api/card/card_id_1/public_link',
                              headers=headers) 
      off_public = requests.delete('http://metabase.com/api/card/card_id_2/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id_3/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id_4/public_link',
                              headers=headers)

      response = requests.get('http://metabase.com/api/card',
                              headers=headers).json()
      

        # For checking if any public links are remaining.
        # Since they were all private links.

      questions = [q for q in response if q['public_uuid']]
      print(f'{len(questions)} public of {len(response)} questions')
      print(excel)
      excel_list = excel.values.tolist()
      print(excel_list)         
      

      columns = ['B','C','D','E'] # Columns to get updated in the spreadsheet
      for l in excel_list:

        for k in range(0,len(columns)):    # Updates the values to the spreadsheet

            update_values('Sheet_id',  
            f"'sheet_name'!{str(columns[k])+str(number_of_rows)}","USER_ENTERED",[[excel_list[0][k]]]
            )

main()
