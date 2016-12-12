from bs4 import BeautifulSoup
import time
import requests
from ProductParser import Prodouct,parser

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

print "start now "+time.strftime('%Y-%m-%d %H:%M:%S')

file = open('results.csv', 'w')
firstRow = "XID,Product_Name,Product_Number,Product_SKU,Product_Inventory_Link,Product_Inventory_Status,Product_Inventory_Quantity,Description,Summary,Prod_Image,Catalog_Information,Category,Keywords,Product_Color,Material,Size_Group,Size_Values,Shape,Theme,Tradename,Origin,Option_Type,Option_Name,Option_Values,Can_order_only_one,Req_for_order,Option_Additional_Info,Imprint_Method,Linename,Artwork,Imprint_Color,Sold_Unimprinted,Personalization,Imprint_Size,Imprint_Location,Additional_Color,Additional_Location,Product_Sample,Spec_Sample,Production_Time,Rush_Service,Rush_Time,Same_Day_Service,Packaging,Shipping_Items,Shipping_Dimensions,Shipping_Weight,Shipper_Bills_By,Shipping_Info,Ship_Plain_Box,Comp_Cert,Product_Data_Sheet,Safety_Warnings,Additional_Info,Distibutor_Only,Disclaimer,Base_Price_Name,Base_Price_Criteria_1,Base_Price_Criteria_2,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,Product_Number_Price,Price_Includes,QUR_Flag,Currency,Less_Than_Min,Price_Type,Upcharge_Name,Upcharge_Criteria_1,Upcharge_Criteria_2,Upcharge_Type,Upcharge_Level,Service_Charge,UQ1,UQ2,UQ3,UQ4,UQ5,UQ6,UQ7,UQ8,UQ9,UQ10,UP1,UP2,UP3,UP4,UP5,UP6,UP7,UP8,UP9,UP10,UD1,UD2,UD3,UD4,UD5,UD6,UD7,UD8,UD9,UD10,Upcharge_Details,U_QUR_Flag,Confirmed_Thru_Date,Product_Number_Criteria_1,Product_Number_Criteria_2,Product_Number_Other,SKU_Criteria_1,SKU_Criteria_2,SKU_Criteria_3,SKU_Criteria_4,SKU,Inventory_Link,Inventory_Status,Inventory_Quantity,Distributor_View_Only,Operation,Carrier_Information,Item_Weight,Warranty,Battery,Industry_Segment,SEO_FLG,UPC_Code,Additional_Imprint_Information,Item_Assembled,Delivery_Option,Do_Not_Use,Product_Status,Workflow_Status,Last_Updated_Date"
file.write(firstRow)
file.write("\n")

url = "http://promomart.espwebsite.com/ProductResults/?SearchTerms=HAT"
html = requests.get(url, headers=headers).content

bsObj = BeautifulSoup(html, 'html.parser')

ids = bsObj.findAll('div', class_="col4 prodPannel")

for item in ids:
    ProdID = item.find('input',class_="ProdID").get('value')
    print "\n",ProdID,time.strftime('%Y-%m-%d %H:%M:%S')
    url = "http://promomart.espwebsite.com/ProductDetails/?productId=" + ProdID

    rows = parser(Prodouct(url)).to_csv_row
    for row in rows:
        file.write(str(ProdID))
        file.write(row)
        file.write("\n")
    # str = parser(Prodouct(url)).to_csv_row
    # file.write(str)
    # file.write("\n")

print "done"+time.strftime('%Y-%m-%d %H:%M:%S')