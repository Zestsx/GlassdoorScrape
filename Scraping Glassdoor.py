from google.colab import drive
drive.mount('/content/drive')
import os
import re
from re import search
from datetime import date
import time
import pathlib
from unicodedata import normalize

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen



#Information we want to scrape
MainData = pd.DataFrame(columns = ['Value', 'Pros', 'Cons', 'Recommend', 'CEOApproval','BusinessOutlook','Rating'])

print(MainData)
    
#Define Number of Pages

pagenumbers = range(1, 10)

#Test Page Number
# i= 1
# pagenumbers = range(i)

#Loop through pages
for i in pagenumbers:
    pagenumber = i
    #You need to get the url of the company reviewed and paste it here, with {pagenumber} as a variable (Example below is JLL)
    url = f'https://www.glassdoor.sg/Reviews/Meta-Reviews-E40772_P{pagenumber}.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng'
    print(url)   
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")


     #Get overall rating
    Rating = soup.find_all('span', attrs = {'class':'ratingNumber mr-xsm'})
    RatingClean = []
    for x in Rating:
        RatingClean.append(x.text)
    
    print(RatingClean)

    #Get date - Role 
    ValueTitle = soup.find_all('span', attrs = {'class':'authorInfo'})
    ValueClean = []
    PostDateClean = []
    LocationClean = []
    Role = []
    print(ValueTitle)
    for x in ValueTitle:
        ValueClean.append(x.text)
    print(ValueClean)
#     for x in ValueTitle:
#          PostDateClean.append(x.text.split("- ")[0])
    
#     for x in ValueTitle:
#         Role.append((x.text.replace('\xa0', ' ').split("- ")[1]))

#     for x in ValueTitle:
#         LocationClean.append((x.text.replace('\xa0', ' ').split("- ")[1].split("in")[0]))

# }

    # print(PostDateClean)

    # print(LocationClean)

    #Feedback
    Feedback = soup.find_all('div', attrs = {'class':'v2__EIReviewDetailsV2__fullWidth'})
    for x in Feedback:
        print(x)

    #Get Pros
    ProClean = []
    Pros = soup.find_all('span', attrs = {'data-test':'pros'})
    for x in Pros:
        ProClean.append(x.text)

    print(ProClean)

    #Get Cons
    ConClean = []
    Cons = soup.find_all('span', attrs = {'data-test':'cons'})
    for x in Cons :
        ConClean.append(x.text)

    print(ConClean)

    sentiment_lookup = {
    'css-hcqxoa-svg': 'Approve',
    'css-1kiw93k-svg': 'Disapprove',
    'css-10xv9lv-svg': 'No Comment',
    'css-1h93d4v-svg': 'Neutral'}

    #Recommend
    RecommendClean = []
    Recommend = soup.find_all('div', attrs = {'class':'d-flex align-items-center mr-std'})
    for x in Recommend:
        if re.match('Recommend', x.text):
            y = x.find_all('svg')
            for z in y:
                RecommendClean.append(z.get('class')[1])

    print(RecommendClean)
    
    # print(RecommendClean)

    #CEO Approval
    CEOApprovalClean = []
    CEOApproval= soup.find_all('div', attrs = {'class':'d-flex align-items-center mr-std'})
    for x in CEOApproval:
        if re.match('CEO Approval', x.text):
            y = x.find_all('svg')
            for z in y:
                CEOApprovalClean.append(z.get('class')[1])

    print(CEOApprovalClean)
    

    #BusinessOutlook
    BusinessOutlookClean = []
    BusinessOutlook = soup.find_all('div', attrs = {'class':'d-flex align-items-center mr-std'})
    for x in BusinessOutlook:
        if re.match('Business Outlook', x.text):
            y = x.find_all('svg')
            for z in y:
                BusinessOutlookClean.append(z.get('class')[1])

    print(BusinessOutlookClean)
    
    

    

    df = pd.DataFrame(list(zip(ValueClean, ProClean, ConClean, RecommendClean, CEOApprovalClean, BusinessOutlookClean, RatingClean)), columns = ['Value', 'Pros', 'Cons', 'Recommend', 'CEOApproval','BusinessOutlook','Rating'])

    df['Recommend'] =   df['Recommend'] .apply(lambda x: sentiment_lookup.get(x))
    df['CEOApproval'] =   df['CEOApproval'] .apply(lambda x: sentiment_lookup.get(x))
    df['BusinessOutlook'] =   df['BusinessOutlook'] .apply(lambda x: sentiment_lookup.get(x))

    print(df)


    
    MainData = pd.concat([MainData,df])
   

    #Wait a little
    time.sleep(5)

MainData['Role'] = MainData['Value'].str.split("in ", n = 1, expand = True)[0]
MainData['Role'] = MainData['Role'].str.split(" - ", n = 1, expand = True)[1]
MainData['Location'] = MainData['Value'].str.split("in ", n = 1, expand = True)[1]
MainData['Date'] = MainData['Value'].str.split(" - ", n = 1, expand = True)[0]
print(MainData)

# Save Results
today_str = date.today().strftime('%Y-%m-%d')
print(today_str)
file_name = 'Scrape' + '_'  + today_str + '_Analysis'

save_path = '/content/drive/My Drive/'+'Insert Google Drive Folder'

print('Saving results to ' + save_path) 

MainData.to_csv(f'/content/drive/My Drive/Glassdoor/{file_name}.csv')
