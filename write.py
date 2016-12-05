from bs4 import BeautifulSoup
import time
import requests
from ProductParser import Prodouct,parser

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

print "start now "+time.strftime('%Y-%m-%d %H:%M:%S')

file = open('results.csv', 'w')

url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=HAT"
html = requests.get(url, headers=headers).content

bsObj = BeautifulSoup(html, 'html.parser')

ids = bsObj.findAll('div', class_="col4 prodPannel")

for item in ids:
    ProdID = item.find('input',class_="ProdID").get('value')
    print "\n",ProdID,time.strftime('%Y-%m-%d %H:%M:%S')
    url = "http://promomart.espwebsite.com/ProductDetails/?productId=" + ProdID
    str = parser(Prodouct(url)).to_csv_row
    file.write(str)
    file.write("\n")

print "done"+time.strftime('%Y-%m-%d %H:%M:%S')
