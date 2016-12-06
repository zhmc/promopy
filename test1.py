from bs4 import BeautifulSoup
import requests

url = "http://promomart.espwebsite.com/ProductDetails/?productId=551125026"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
html = requests.get(url, headers=headers).content
bsObj = BeautifulSoup(html, 'html.parser')

allData = bsObj.findAll("div", class_="attributesContainer")
ImprintDiv = allData[2]
ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
BlockMap = {}
ImprintDic = {}
ImprintMethodName = ""
ImprintCharge = {}

for dataFieldBlock in ImprintData:
    BlockName = dataFieldBlock.find("h5").get_text().strip()
    BlockValue = dataFieldBlock
    BlockMap[BlockName] = BlockValue

for key in BlockMap.keys():
        block = BlockMap[key]
        if key =="Imprint Method":
        	#print key, BlockMap[key]
        	ImprintMethodName = block.find("div", class_="setDetail dataFieldBlock").get_text().strip()
        	if "Charge Type" in block.get_text().strip():
        		ImprintCharge['Upcharge_Name'] = ImprintMethodName
        		ImprintCharge['Upcharge_Criteria_1'] = "IMMD:"+ImprintMethodName
        		ImprintCharge['Upcharge_Type'] = "Imprint Method Charge"
        		if "Per Order" in block.get_text().strip():
        			ImprintCharge['Upcharge_Level'] = "Per Order"
        		else:
        			ImprintCharge['Upcharge_Level'] = "Other"

print ImprintMethodName, ImprintCharge