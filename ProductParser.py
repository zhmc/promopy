# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import requests

class Prodouct(object):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    Product_Name = ""
    Product_Number = ""
    Description = ""
    Prod_Image = ""
    Category = ""
    Product_Color = ""
    Material = ""

    sample_charge = {}
    Size_Group = ""
    Size_Values = ""
    Price_table = [[], []]
    Price_Includes = ""

    def __init__(self, url):
        self.url = url

    @property
    def to_csv_row(self):
        csv_row = ""

        # xid
        csv_row += ","
        # Product_Name
        csv_row += '"' + self.Product_Name + '"' + ","
        # Product_Number
        csv_row += '"' + self.Product_Number + '"' + ","
        # Product_SKU, Product_Inventory_Link, Product_Inventory_Status, Product_Inventory_Quantity
        csv_row += ",,,,"
        # Description
        csv_row += '"' + self.Description + '"' + ","
        # Summary
        csv_row += ","
        # Prod_Image
        csv_row += self.Prod_Image + ","
        # Catalog_Information
        csv_row += '"' + self.Category + '"' + ","
        # Keywords
        csv_row += ","
        # Product_Color
        csv_row += ","
        # Silicone=Silicone
        csv_row += self.Material + "=" + self.Material + ","
        # Size_Group
        csv_row += self.Size_Group + ","
        # Size_Values
        csv_row += self.Size_Values + ","

        print csv_row
        return csv_row


def parser(productObject):
    html = requests.get(productObject.url, headers=productObject.headers).content

    bsObj = BeautifulSoup(html, 'html.parser')

    # all attributes here
    Product_Name = ""
    Product_Number = ""
    Description = ""
    Prod_Image = ""
    Category = ""
    sample_charge = {}
    Size_Group = ""
    Size_Values = ""
    Price_table = [[], []]
    Price_Includes = ""

    Product_Name = bsObj.find("span", {"class": "prodName"}).get_text().strip()
    print Product_Name
    productObject.Product_Name = Product_Name

    Product_Number = bsObj.find("div", {"class": "prodNum"}).get_text().strip()
    print Product_Number
    productObject.Product_Number = Product_Number

    Description = bsObj.find("div", {"class": "prodDescrFull prepend-top"}).get_text().strip()
    # print Description
    productObject.Description = Description

    picsrcs = bsObj.findAll("input", {"type": "image"})
    for i in range(len(picsrcs)):
        if i == 0:
            Prod_Image += picsrcs[i]['src']
        else:
            Prod_Image += "," + picsrcs[i]['src']

    # print Prod_Image
    productObject.Prod_Image = Prod_Image

    allData = bsObj.findAll("div", class_="attributesContainer")
    # print len(allData)

    PriceingDiv = allData[0]
    trs = PriceingDiv.findAll("tr")
    # print "trs", len(trs)
    row_Quantity = trs[0].findAll("th")
    for th in row_Quantity:
        Price_table[0].append(th.get_text().strip())
    row_Price = trs[1].findAll("td")
    for td in row_Price:
        Price_table[1].append(td.get_text().strip())

    print Price_table
    productObject.Price_table = Price_table

    Product_Detail = allData[1]
    Product_Detail_Data = Product_Detail.findAll("div", class_="dataFieldBlock")
    print len(Product_Detail_Data)
    ProductDetailDic = {}
    for k in range(len(Product_Detail_Data)):
        try:
            raw_attr = Product_Detail_Data[k].find("h5").get_text()
            attr = raw_attr.strip()
            raw_value = Product_Detail_Data[k].get_text().strip()
            value = raw_value.replace(attr, "").strip()
            ProductDetailDic[attr] = value
            if attr == "Samples":
                # value = value.replace("\t","")
                sample_list = value.split("\n")
                sample_list_clean = []
                for si in range(len(sample_list)):
                    if len(sample_list[si].strip()) > 0:
                        sample_list_clean.append(sample_list[si].strip())
                ProductDetailDic[attr] = sample_list_clean
                # 如果存在sample这一项，那么给sample_charge填充数据
                sample_charge['Upcharge_Type'] = "Sample Charge"
                sample_charge['Upcharge_Level'] = "Other"
                sample_charge['Service_Charge'] = "Optional"
                sample_charge['UQ1'] = "1"
                for key in range(len(sample_list_clean)):
                    if sample_list_clean[key] == "Price":
                        sample_charge['UP1'] = sample_list_clean[key + 1]
                sample_charge['Upcharge_Details'] = sample_list_clean[-1].replace("Price Includes:", "").strip()

        except:
            pass
    # print ProductDetailDic
    # print ProductDetailDic.get("Samples")
    print "sample_charge"
    print sample_charge

    try:
        Size_Values = ProductDetailDic.get("Size")
        if "Length" in Size_Values or "Width" in Size_Values or "Height" in Size_Values or "x" in Size_Values:
            Size_Group = "Dimension"
        elif "M" in Size_Values or "L" in Size_Values or "S" in Size_Values:
            Size_Group = "Standard & Numbered"
        elif "oz" in Size_Values or "ml" in Size_Values:
            Size_Group = "Volume/Weight"
        print "Size_group,Size_values"
        print Size_Group, Size_Values
    except:
        pass

    ImprintDiv = Product_Detail = allData[1]


    return productObject

if __name__ == "__main__":
    print parser(Prodouct("http://promomart.espwebsite.com/ProductDetails/?productId=550923254")).to_csv_row
