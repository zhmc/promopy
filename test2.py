# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import requests

url = "http://promomart.espwebsite.com/ProductDetails/?productId=551144004"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
html = requests.get(url, headers=headers).content
bsObj = BeautifulSoup(html, 'html.parser')

allData = bsObj.findAll("div", class_="attributesContainer")
ImprintDiv = allData[3]
ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
ImprintDic = {}
ImprintMethodName = ""
ImprintBasicInfo = {}

for dataFieldBlock in ImprintData:
    BlockName = dataFieldBlock.find("h5").get_text().strip()
    if "Packaging" in BlockName:
        packagingInfo = dataFieldBlock.get_text().strip().replace("Packaging","").strip()

