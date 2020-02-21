import requests 
from bs4 import BeautifulSoup

url_to_scrape = 'http://www.pro-football-reference.com/years/2016/'

r = requests.get(url_to_scrape)

soup = BeautifulSoup(r.text,'lxml')

Information = []

for table_row in soup.select(".sortable  stats_table tr"):
    table_cells = table_row.findALL('td')
    
    if len(table_cells) > 0:
        tabledetail1 = table_cells[0].find('td')['align']
        Information.append(tabledetail1)
        
    
print (Information)
        