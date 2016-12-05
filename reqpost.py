import requests
from bs4 import BeautifulSoup
import re
import time


print "start"+time.strftime('%Y-%m-%d %H:%M:%S')

url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=HAT"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

response = requests.get(url,headers=headers)
# print response.content
bsObj = BeautifulSoup(response.content, 'html.parser')
ids = bsObj.findAll('div', class_="col4 prodPannel")
for item in ids:
    ProdID = item.find('input',class_="ProdID").get('value')
    print ProdID

print "Page1_done"+time.strftime('%Y-%m-%d %H:%M:%S')

postData = {}
inputset1 = bsObj.findAll("input", {"type": "hidden"})
inputset2 = bsObj.findAll("input", {"type": "text"})

for inputitem in inputset1:
    key = inputitem.attrs['name']
    try:
        value = inputitem.attrs['value']
    except:
        value = ""
    finally:
        postData[key] = value
for inputitem in inputset2:
    key = inputitem.attrs['name']
    try:
        value = inputitem.attrs['value']
    except:
        value = ""
    finally:
        postData[key] = value

#print postData

nextLink = bsObj.find("a", {"class": "edcPageNext"}).attrs['href']
__EVENTTARGET_value = re.findall(r"doPostBack\('(.*?)'",nextLink)
# print __EVENTTARGET

postData["__EVENTTARGET"] = __EVENTTARGET_value

response2 = requests.post(url,data=postData,headers=headers)
# print response2.content

bsObj = BeautifulSoup(response2.content, 'html.parser')
ids = bsObj.findAll('div', class_="col4 prodPannel")
for item in ids:
    ProdID = item.find('input',class_="ProdID").get('value')
    print ProdID

print "Page1_done"+time.strftime('%Y-%m-%d %H:%M:%S')