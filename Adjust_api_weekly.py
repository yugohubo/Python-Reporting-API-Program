from ast import dump
from cmath import nan,isnan
from pickle import FALSE, TRUE
import requests
import pandas as pd
import io
import numpy as np
import datetime
from datetime import timedelta
import json


#Global and Time Variables

today = datetime.datetime.today()   
noww = today - timedelta(days = 1)

noww = noww.strftime("%Y-%m-%d")
imp_all=0
clicks = 0
installs = 0



### ADJUST API CALLS ###

# You can get your auth token from the adjust dashboard. It is a unique token for your account.
# Your app-token is different for each app you have in adjust. You can get it from the dashboard.

def main():

    all = requests.get(f'http://api.adjust.com/kpis/v1/app-token?start_date={noww}&end_date={noww}&attribute_type=all&grouping=os_names', headers={'Authorization': 'Token token=auth_token','Accept':'text/csv'}).content
    product = requests.get(f'http://api.adjust.com/kpis/v1/app-token/events?start_date={noww}&end_date={noww}', headers={'Authorization': 'Token token=auth_token','Accept':'text/csv'}).content
    
    impressions = requests.get(f'https://dash.adjust.com/control-center/reports-service/report?&cost_mode=network&app_token__in=your_app_token&date_period={noww}:{noww}&dimensions=os_name&metrics=impressions,clicks,network_installs',headers={'Authorization': 'Token token=your_auth_token', 'Accept':'json'}).content
    # impressions not just impressions but also network installs(store) and clicks
    
    imp_pd = pd.read_csv(io.StringIO(impressions.decode('utf-8')))
    imp_df = pd.DataFrame(imp_pd,columns=['impressions'])
    imp = imp_df.values.tolist()

    print(all)
    all_pd = pd.read_csv(io.StringIO(all.decode('utf-8')))
    all_df = pd.DataFrame(all_pd,columns=['clicks','installs','network_in'])
    all = all_df.values.tolist()


    product_pd = pd.read_csv(io.StringIO(product.decode('utf-8')))
    print(product_pd)
    product_df = pd.DataFrame(product_pd,columns=['event_name','events'])
    print(product_df)
    products = product_df.values.tolist()
    
    
    View_product = 0
    add_basket = 0
    purchase = 0
    for i in products:      
        if i[0]=='View Product':        
             View_product+=i[1]         
    for i in products:
        if i[0]=='AddToBasket':
             add_basket+=i[1]
    for i in products:
        if i[0]=='Purchase':
             purchase+=i[1]

    
    # Define them as global variables so they can be used in the next function
    
    global clicks_all
    global ios_down
    global andr_down
    global imp_all


    imp_all = 0
    for i in imp:
         imp_all += i[0]
    
    cl=[x[0] for x in all]
    clicks_all = np.nansum(cl)
    
    ios_down = all[1][1]
    andr_down = all[0][1]
    imp_all=int(imp_all)
    

    # Parse the data and store it in a dictionary

    decoded_data = impressions.decode('utf-8')
    parsed_data = json.loads(decoded_data)

    numeric_values_by_os = {}
    numeric_values_by_os_clicks = {}
    
    for row in parsed_data['rows']:
        os_name = row['os_name']
        impressionss = int(row['impressions'])
        clicks = int(row['clicks'])

        if os_name in numeric_values_by_os:
            numeric_values_by_os[os_name].append(impressionss)
            numeric_values_by_os_clicks[os_name].append(clicks)
            
        else:
            numeric_values_by_os[os_name] = [impressionss]
            numeric_values_by_os_clicks[os_name] = [clicks]
    
    # Sum all values for all OS
    imp_all = numeric_values_by_os['android'][0]+numeric_values_by_os['ios'][0]
    clicks_all = numeric_values_by_os_clicks['android'][0]+numeric_values_by_os_clicks['ios'][0]
    
    
    # Print all so you can check if any is missing
    
    print(imp_all)
    print(clicks_all)
    print(andr_down)
    print(ios_down)
    print(View_product)
    print(purchase)


    # Returns the data to be imported in this order as a list
    
    return [[imp_all], [int(clicks_all)], [ios_down], [andr_down],[View_product],[purchase]]   

main()