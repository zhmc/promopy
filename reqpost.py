import requests
from bs4 import BeautifulSoup
import re
import time

def getFirstPageContent(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url,headers=headers)
    return response.content


def getNextPageContent(url, startContent):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    bsObj = BeautifulSoup(startContent, 'html.parser')
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

    response = requests.post(url,data=postData,headers=headers)

    return response.content

def printProdID(content):
    bsObj = BeautifulSoup(content, 'html.parser')
    ids = bsObj.findAll('div', class_="col4 prodPannel")
    for item in ids:
        ProdID = item.find('input',class_="ProdID").get('value')
        print ProdID

    print "done"+time.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    print "start"+time.strftime('%Y-%m-%d %H:%M:%S')
    url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=HAT"
    content = getFirstPageContent(url)
    print "page: 1"
    printProdID(content)
    
    for i in range(20):
        content = getNextPageContent(url, content)
        print "page: "+str(i+2)
        printProdID(content)
