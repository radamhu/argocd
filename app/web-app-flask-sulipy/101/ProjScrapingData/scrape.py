#import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

from time import sleep
from random import randint

#Range of pages #There are total 792 pages to scrape from the URL.
pages = [str(i) for i in range(1,792)]

# Scrape multiple pages
rows=[]

for page in pages:
    print(page)
    url = 'https://toppub.xyz/publications?page='+ str(page)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    p = soup.select('p')
    print(len(p))
    table = soup.find('table', class_='table')
    for row in table.find_all('tr'):
        columns = row.find_all('td') # the first row is returning <th> tags, but since you queried <td> tags, it's returning empty list.
        if len(columns)>0: #In order to skip first row or in general, empty rows, you need to put an if check.
        #Use the indices properly to get different values.
            Name = columns[1].get_text()
            Description =columns[2].get_text()
            Followers = columns[3].get_text()
            rows.append([Name,Description,Followers])
    sleep(randint(2,10))

#print(page.status_code) # The response shouls be 200, to scrape it

df=pd.DataFrame(rows,columns=['Name','Description','Followers'])

print(df)

df.to_csv('blog_medium.csv',header=True,sep=';')