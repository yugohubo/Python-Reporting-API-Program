import pandas as pd
import requests
import io
import time

import datetime
from datetime import timedelta


today = datetime.datetime.today()
todayy = today - timedelta(days = 1)

#todayy = input("Please enter the date you wish to update(yyyy-mm-dd):/n") # Alternative way to use the date you wish to update

todayy = todayy.strftime("%Y-%m-%d")

# First URL after http is your metabase server, you can check this from settings in the metabase. Also, VPN should be open.

def main():
      
      ### LOGIN ###

      response = requests.post('http://metabase.com/api/session', # Use your own metabase server
                              json={'username': 'your_username',
                                    'password': 'your_password'})
      print(response)
      session_id = response.json()['id']
      headers = {'X-Metabase-Session': session_id} # Use this session id for the following requests
            

      ### API CALLS ###

      on_public = requests.post('http://metabase.com/api/card/card_id/public_link',
                              headers=headers) # creates the public link so we can get the data
      uuid = on_public.json()['uuid']


      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content

      excel = pd.read_csv(io.BytesIO(response))
      
      #############################################################
      on_public = requests.post('http://metabase.com/api/card/card_id/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel2 = pd.read_csv(io.BytesIO(response))

      #############################################################

      on_public = requests.post('http://metabase.com/api/card/card_id/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel3 = pd.read_csv(io.BytesIO(response))
      print(excel3)

      #############################################################

      on_public = requests.post('http://metabase.com/api/card/card_id/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel4 = pd.read_csv(io.BytesIO(response))
      
      #############################################################
      
      on_public = requests.post('http://metabase.com/api/card/card_id/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel5 = pd.read_csv(io.BytesIO(response))
      print(excel5)
      
      #############################################################
      
      on_public = requests.post('http://metabase.com/api/card/209/public_link',
                              headers=headers) 
      uuid = on_public.json()['uuid']
      response = requests.get(f'http://metabase.com/api/public/card/{uuid}/query/csv',
                              ).content
      excel6 = pd.read_csv(io.BytesIO(response))
      print(excel6)

      #############################################################

      # For checking if any of the dataframes are empty if any empty wait 5 seconds and try again

      excel_list = [excel,excel2,excel3,excel4,excel5,excel6]
      for i in excel_list:
            if i.empty:
                  time.sleep(5)
                  main()


      ### Column Renaming for Data Merging ### (Change column names to your needs)

      excel2.rename(columns = {'column_x ' : 'rename_1' }, inplace = True)
      extract = excel2["rename_1"] # Extracting the column to join the first excel dataframe
      excel = excel.join(extract)
      
      excel3.rename(columns={'column_y':'rename_2'}, inplace = True)
      extract = excel3["rename_2"]
      excel = excel.join(extract)

      excel4.rename(columns={'column_z':'rename_3'}, inplace = True)
      extract = excel4["rename_3"]
      excel = excel.join(extract)

      excel5.rename(columns={'column_k':'rename_4'}, inplace = True)
      extract = excel5["rename_4"]
      excel = excel.join(extract)

      excel6.rename(columns={'column_l':'rename_5'}, inplace = True)
      extract = excel6["rename_5"]
      excel = excel.join(extract)

      excel.rename(columns={'column':'rename'}, inplace = True) # We have merged all with the first excel file
      excel.rename(index ={ 0: f"{todayy}"}, inplace = True) # For changing Row name to the date of today
      excel = excel.values.tolist()
  

      ### Deleting Public Links ### 

      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)
      off_public = requests.delete('http://metabase.com/api/card/card_id/public_link',
                              headers=headers)


      # For checking if any public links are remaining.
      # Since they were all private links.
      
      response = requests.get('http://metabase.com/api/card',
                              headers=headers).json()
      questions = [q for q in response if q['public_uuid']]
      print(f'{len(questions)} public of {len(response)} questions')
      print(questions)


      return excel

main()
