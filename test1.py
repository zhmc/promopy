# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import requests

url = "http://promomart.espwebsite.com/ProductDetails/?productId=551144004"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
html = requests.get(url, headers=headers).content
bsObj = BeautifulSoup(html, 'html.parser')

allData = bsObj.findAll("div", class_="attributesContainer")
ImprintDiv = allData[2]
ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
BlockMap = {}
ImprintDic = {}
ImprintMethodName = ""
ImprintBasicInfo = {}

for dataFieldBlock in ImprintData:
    BlockName = dataFieldBlock.find("h5").get_text().strip()
    BlockValue = dataFieldBlock
    BlockMap[BlockName] = BlockValue

for key in BlockMap.keys():

    # 提取Imprint Information板块的信息
    if key == "Imprint Information":
        block = BlockMap[key]
        InfoList = block.findAll("div", class_="dataFieldBlock")

        # 默认Sold_Unimprinted是No，也就是不填
        ImprintBasicInfo["Sold_Unimprinted"] = ""
        # 默认Personalization是No，也就是不填
        ImprintBasicInfo["Personalization"] = ""
        # 默认Imprint_Size是No，也就是不填
        ImprintBasicInfo["Imprint_Size"] = ""
        for i in range(len(InfoList)):
            text = InfoList[i].get_text().strip()
            # print text
            if "Imprint Method" in text:
                ImprintBasicInfo["Imprint Method"] = text.replace("Imprint Method","").strip()
            elif "Imprint Color" in text:
                ImprintBasicInfo["Imprint Color"] = text.replace("Imprint Color","").strip()
            elif "Sold Unimprinted" in text:
                if "Yes" in text.replace("Sold_Unimprinted","").strip():
                    ImprintBasicInfo["Sold_Unimprinted"] = "Y"
            elif "Personalization" in text:
                if "Yes" in text.replace("Personalization:","").strip():
                    ImprintBasicInfo["Personalization"] = "Y"
            elif "Imprint Size" in text:
                ImprintBasicInfo["Imprint_Size"] = text.replace("Imprint Size","").strip()

    # 提取Imprint Location板块的信息（如果有）  这里之考虑了简单的情况（只有一行）
    if key == "Imprint Location":
        text = BlockMap[key].get_text().strip()
        ImprintBasicInfo["Imprint Location"] = text.replace("Imprint Location","").strip()




print ImprintBasicInfo