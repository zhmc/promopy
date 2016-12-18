# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import traceback
import browser
import requests
from requests import ConnectionError
from threading import Thread
from random import choice
from ProductParser import Prodouct,parser
from nextPage import get80PerPage, getNextPageContent, getProdIDList, getFirstPageContent, get80NextPageContent

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers_list = [{'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                ,{'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0"}
                ]

class MyThread(Thread):
    prodID = ""
    url = ""
    rowList = []
    productInfo = Prodouct("")

    def __init__(self, prodID):
        Thread.__init__(self)
        self.prodID = str(prodID)
        self.url = "http://promomart.espwebsite.com/ProductDetails/?productId=" + self.prodID

    def run(self):
        try:
            self.productInfo = parser(Prodouct(self.url))
            self.rowList = self.productInfo.to_csv_row
        except ConnectionError, e:
            print self.prodID + "连接错误"
        # except IndexError:
        # #     print self.prodID + "数组越界"
        # except TypeError,e:
        #     print self.prodID + "类型错误"
        except:
            print self.prodID
            traceback.print_exc()

    def getRowList(self):
        return self.rowList

# threadPool = []

def getThreadPoolFromProdIDList(ProdIDList):
    threadPool = []
    # productList = []
    for ProdID in ProdIDList:
        mythread = MyThread(ProdID)
        threadPool.append(mythread)
    for singlethread in threadPool:
        singlethread.start()
    for singlethread in threadPool:
        singlethread.join()

    # for singlethread in threadPool:
    #     productList.append(singlethread.productInfo)

    return threadPool

def getThreadPoolAndStartContentByKeyword80(keyword):
    url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=" + keyword
    content = getFirstPageContent(url)
    content80 = get80PerPage(url, content)
    idList = getProdIDList(content80)
    threadPool = getThreadPoolFromProdIDList(idList)
    package = {}
    package['threadPool'] = threadPool
    package['startContent'] = content80
    return threadPool

def getFirstThreadPoolAndEndContentByKeyword(keyword):
    url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=" + keyword
    content = getFirstPageContent(url)
    content80 = get80PerPage(url, content)
    idList = getProdIDList(content80)
    threadPool = getThreadPoolFromProdIDList(idList)
    package = {}
    package['threadPool'] = threadPool
    package['endContent'] = content80

    return package

def getThreadPoolAndEndContentByStartContent(keyword, startContent):
    url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=" + keyword
    endContent = get80NextPageContent(url, startContent)
    idList = getProdIDList(endContent)
    threadPool = getThreadPoolFromProdIDList(idList)

    package = {}
    package['threadPool'] = threadPool
    package['endContent'] = endContent

    return package

def getCsvRowsFromThreadPool(threadPool):
    rows4write = []
    for singlethread in threadPool:
        rows = singlethread.getRowList()
        for row in rows:
            newrow = singlethread.prodID + row
            rows4write.append(newrow)
    return rows4write

def write2Csv(filepath, rows4write):
    csvfile = open(filepath, 'w')
    firstRow = "XID,Product_Name,Product_Number,Product_SKU,Product_Inventory_Link,Product_Inventory_Status,Product_Inventory_Quantity,Description,Summary,Prod_Image,Catalog_Information,Category,Keywords,Product_Color,Material,Size_Group,Size_Values,Shape,Theme,Tradename,Origin,Option_Type,Option_Name,Option_Values,Can_order_only_one,Req_for_order,Option_Additional_Info,Imprint_Method,Linename,Artwork,Imprint_Color,Sold_Unimprinted,Personalization,Imprint_Size,Imprint_Location,Additional_Color,Additional_Location,Product_Sample,Spec_Sample,Production_Time,Rush_Service,Rush_Time,Same_Day_Service,Packaging,Shipping_Items,Shipping_Dimensions,Shipping_Weight,Shipper_Bills_By,Shipping_Info,Ship_Plain_Box,Comp_Cert,Product_Data_Sheet,Safety_Warnings,Additional_Info,Distibutor_Only,Disclaimer,Base_Price_Name,Base_Price_Criteria_1,Base_Price_Criteria_2,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,Product_Number_Price,Price_Includes,QUR_Flag,Currency,Less_Than_Min,Price_Type,Upcharge_Name,Upcharge_Criteria_1,Upcharge_Criteria_2,Upcharge_Type,Upcharge_Level,Service_Charge,UQ1,UQ2,UQ3,UQ4,UQ5,UQ6,UQ7,UQ8,UQ9,UQ10,UP1,UP2,UP3,UP4,UP5,UP6,UP7,UP8,UP9,UP10,UD1,UD2,UD3,UD4,UD5,UD6,UD7,UD8,UD9,UD10,Upcharge_Details,U_QUR_Flag,Confirmed_Thru_Date,Product_Number_Criteria_1,Product_Number_Criteria_2,Product_Number_Other,SKU_Criteria_1,SKU_Criteria_2,SKU_Criteria_3,SKU_Criteria_4,SKU,Inventory_Link,Inventory_Status,Inventory_Quantity,Distributor_View_Only,Operation,Carrier_Information,Item_Weight,Warranty,Battery,Industry_Segment,SEO_FLG,UPC_Code,Additional_Imprint_Information,Item_Assembled,Delivery_Option,Do_Not_Use,Product_Status,Workflow_Status,Last_Updated_Date"
    csvfile.write(firstRow)
    csvfile.write("\n")
    for row in rows4write:
        csvfile.write(row)
        csvfile.write("\n")

    csvfile.close()

def writeCsvByThreadPool(threadPool,filepath):
    rows4write = getCsvRowsFromThreadPool(threadPool)
    write2Csv(filepath, rows4write)

if __name__ == "__main__":
    print "start now " + browser.strftime('%Y-%m-%d %H:%M:%S')
    headers = choice(headers_list)
    url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=tshirt"
    html = requests.get(url, headers=headers).content
    first80content = get80PerPage(url,html)

    print "80第一页加载完成 " + browser.strftime('%Y-%m-%d %H:%M:%S')
    # bsObj = BeautifulSoup(first80content, 'html.parser')
    # ids = bsObj.findAll('div', class_="col4 prodPannel")
    idList = getProdIDList(first80content)
    # for item in ids:
    #     ProdID = item.find('input', class_="ProdID").get('value')
    #     idList.append(str(ProdID))


    threadPool = getThreadPoolFromProdIDList(idList)
    print "写文件花多少时间 " + browser.strftime('%Y-%m-%d %H:%M:%S')
    rows4write = getCsvRowsFromThreadPool(threadPool)
    write2Csv('results.csv',rows4write)
    print "done" + browser.strftime('%Y-%m-%d %H:%M:%S')
