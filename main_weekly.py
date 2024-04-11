from __future__ import print_function

import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Imports from other files

import config_weekly as cf
import metabase_api_weekly as meta
import Adjust_api_weekly as adj



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
    # pylint: disable=maybe-no-member
    
    try:

        service = build('sheets', 'v4', credentials=creds)
        
        # values = [
        #     [
        #         # Cell values ...
        #     ],
        #     # Additional rows ...
        # ]
        
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

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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


    ### DATA IMPORT ORDER INPUT FROM USER ###

    print("Order for values: DAU, DAB, Time_spent, DAL, DAL_perc, DAVV, DAVV_perc, DAV ")
    sayfa = input("Input the sheet name:\n")
    cell = input("Input the DAU cell:\n")
    iterated=int(cell[1:])
    cell=cell[:1]

    
    ### Import Data From Metabase API ###

    meta_dict = meta.main() 
    cell_meta = [29,30,31,32,33,35,36,39,26] 
    cell_number = len(cell_meta)
    

    ### UPDATE METABASE DATA ###
    
    i = 0
    for k in range(cell_number):
        print(i)
        if meta_dict[0][i] != meta_dict[0][i] :
            update_values(cf.destination,
            f"'{sayfa}'!{cell[:1]+str(cell_meta[i])}",
            "USER_ENTERED",[[0]]
            )
            i+=1
       
        else:
            update_values(cf.destination,
            f"'{sayfa}'!{cell[:1]+str(cell_meta[i])}",
            "USER_ENTERED",[[meta_dict[0][i]]]
            )
            i+=1
        

    ### Import Data From Adjust API ###

    adjust_dict = adj.main()
    cell_adjust = [14,15,9,10,28]
    cell_number = len(cell_adjust)

    ### UPDATE ADJUST DATA ###

    i = 0
    for k in range(cell_number):

        update_values(cf.destination,
        f"'{sayfa}'!{cell[:1]+str(cell_adjust[i])}","USER_ENTERED",[[adjust_dict[i][0]]]
        )
        i+=1
    
    ### LOOKER based data in the googlesheets as seperate spreadsheets to be updated to the main report ###        
        
        # SpreadSheet ID's are imported from the config file

    for i in cf.import_list:
        
        if i == cf.DAL:

            new = get_values(i,"C2")
        
        elif i == cf.DAV:

            new = get_values(i,"C2")
        
        elif i == cf.son_30_gun:

            new = get_values(i,"A2")

        else:
            new = get_values(i,"B2")


        # TRY EXCEPT BLOCK TO HANDLE THE COMMA IN THE NUMBERS
        try:    
            if "," in str(new['values'][0][0]):
                new['values'][0][0] = int(str(new['values'][0][0]).replace(",",""))
            else:
                new['values'] = new['values']
        except:
            new['values'] = [[0]]
       

        # ITERATE THE CELL NUMBER TO UPDATE THE VALUES
        iterated=str(iterated)
        cell+=iterated
        iterated=int(iterated)

        ## UPDATE LOOKER DATA ##
        
        # Based on the order of your sheet table change it as you wish
        
        if i == cf.son_30_gun:
            cell = cell[:1]
            cell += "40"
            try:    
                update_values(cf.destination,
                    f"'{sayfa}'!{cell}","USER_ENTERED",new['values']
                    ) 

            except:
                new['values'] = [[0]]
                update_values(cf.destination,
                f"'{sayfa}'!{cell}","USER_ENTERED",new['values']
                )

        else:

            try:    
                update_values(cf.destination,
                    f"'{sayfa}'!{cell}","USER_ENTERED",new['values']
                    ) 

            except:
                new['values'] = [[0]]
                update_values(cf.destination,
                f"'{sayfa}'!{cell}","USER_ENTERED",new['values']
                )
            cell=cell[:1]
            iterated+=1


main()