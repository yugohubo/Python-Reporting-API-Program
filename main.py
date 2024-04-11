import config as cf #Imports Config File for Spreadsheet IDs


import tkinter as tk
import os
import os.path


import pandas as pd
from datetime import datetime
import requests


#Google API Dependencies

from google.auth.transport.requests import Request  
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_csv(spreadsheet_id):            # This is for getting the Spreadsheets as CSV files / You can find the original code at googlesheets doc
 
    
    service = build('sheets', 'v4', credentials=creds)

    gsheets = service.spreadsheets().get(spreadsheetId = spreadsheet_id).execute()
    sheets = gsheets['sheets']
    # print(gsheets)

    try:
        

        sheet_number = len(sheets) - 2
        for sheet in sheets:
            

            range_name = sheets[sheet_number]['properties']['title']
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, 
                range=range_name,
                majorDimension = 'ROWS'
                ).execute()
            df = pd.DataFrame(result['values'])
            print(range_name)

            return df
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def get_csv_event_based(spreadsheet_id):
 
    
    service = build('sheets', 'v4', credentials=creds)

    gsheets = service.spreadsheets().get(spreadsheetId = spreadsheet_id).execute() 
    sheets = gsheets['sheets']

    try:
        
        sheet_number = 1 # Which numerically ordered sheet you want to get / enter int number.
        for sheet in sheets:
            

            range_name = sheets[sheet_number]['properties']['title']
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, 
                range=range_name,
                majorDimension = 'ROWS'
                ).execute()
            df = pd.DataFrame(result['values'])
            print(range_name)

            return df
    
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


main()


def total_video_operation():

    '''This function is for the Total Video Report 
    to be exported as an Excel file and opened automatically.'''

    total_video_weekly_spreadID = cf.import_list[1]
    total_video_weekly = get_csv(total_video_weekly_spreadID)
    total_video_weekly.to_excel('total_video.xlsx', index = False)
    os.startfile('total_video.xlsx')

def weekly_snapshot_operation():
    
    '''This function is for the Weekly Snapshot Report
    to be exported as an Excel file and opened automatically.'''

    weekly_spreadID = cf.import_list[0]
    weekly = get_csv(weekly_spreadID)
    weekly.to_excel('weekly.xlsx', index = False)
    os.startfile('weekly.xlsx')


def run_weekly():

    '''This function is for running the main_weekly.py and active_buyer.py,
    so they update their respective google sheets reports'''

    import active_buyer # This is the main function that runs the active_buyer.py / Updates the Active Buyer Report Sheet
    import main_weekly  # This is the main function that runs the main_weekly.py / Updates the Weekly Report Sheet
    

#This is the main function that runs the GUI

if __name__ == "__main__":
    window = tk.Tk()
    window.title('Reports')
    window.geometry('600x600')

    firstFrame = tk.Frame(window, width=300, height=100)
    firstFrame.rowconfigure(0, weight=1)
    firstFrame.columnconfigure(0, weight=1)
    firstFrame.pack(fill="both", expand=True)

    secondFrame = tk.Frame(window, width=300, height=100)
    secondFrame.rowconfigure(0, weight=1)
    secondFrame.columnconfigure(1, weight=1)
    secondFrame.pack(fill="both", expand=True)

    thirdFrame = tk.Frame(window, width=300, height=100)
    thirdFrame.rowconfigure(0, weight=1)
    thirdFrame.columnconfigure(2, weight=1)
    thirdFrame.pack(fill="both", expand=True)


    Weekly = tk.Button(firstFrame, text="Weekly Report", command = weekly_snapshot_operation)
    Weekly.grid(row=0, column=0)

    TotalVideo = tk.Button(secondFrame, text="Video Report", command = total_video_operation) 
    TotalVideo.grid(row=0, column=1)

    RunWeekly = tk.Button(thirdFrame, text="Run Weekly", command = run_weekly) 
    RunWeekly.grid(row=0, column=2)

    window.mainloop()