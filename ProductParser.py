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

    Imprint_Method = ""
    Sold_Unimprinted = ""

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

        # print csv_row
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
    # print len(Product_Detail_Data) 这个地方发现长度有点不太对，不能依次按顺序取数据，必须得按照键值对取数据
    ProductDetailDic = {}
    for k in range(len(Product_Detail_Data)):
        try:
            raw_attr = Product_Detail_Data[k].find("h5").get_text()
            attr = raw_attr.strip()
            raw_value = Product_Detail_Data[k].get_text().strip()
            value = raw_value.replace(attr, "").strip()
            ProductDetailDic[attr] = value
            if attr == "Samples":
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


    """
    这个地方ImpritDiv里面分为几个板块（如果有），其中Imprint Information板块是始终出现的，
    当Imprint Method板块出现时，有时候里面会有charge type，这时会有一个table记录upcharge
    当Artwork & Proofs板块出现时，有时候里面会有charge type，这时会有一个table记录upcharge

    当一个商品有几个upcharge（包括Sample Charge，Imprint Method Charge，Artwork Charge，Rush Service Charge）
    出现时，在csv中第一条记录中的upcharge type项暂时定为记录Imprint Method Charge（如果有），别的就接着主记录行，用一行填上upcharge相关信息
    """
    ImprintDiv = allData[2]
    ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    BlockMap = {}
    ImprintDic = {}

    # 获取到ImprintDiv里面的各个板块
    for dataFieldBlock in ImprintData:
        BlockName = dataFieldBlock.find("h5").get_text().strip()
        BlockValue = dataFieldBlock
        BlockMap[BlockName] = BlockValue

    # 遍历这几个板块
    #for k in d.keys()

    for k in range(len(ImprintData)):
        try:
            ImprintKey = ImprintData[k].find("label").get_text().strip()
            ImprintValue = ImprintData[k].get_text().replace(ImprintKey, "").strip()
            ImprintDic[ImprintKey] = ImprintValue

        except Exception, e:
            print e


    return productObject


"""这个函数是获取Pricing大块中的table和Price Includes信息"""
def getPricing(bsObj):
    pass


"""这个函数是获取ProductDetail大块中的除了Samples板块的基本信息"""
def getProductDetail(bsObj):
    pass


"""这个函数是获取ProductDetail大块中的Samples板块（如果有），会生成csv中的sample charge"""
def getSampleCharge(bsObj):
    pass


"""这个函数是获取Imprint大块中的Imprint Information板块（肯定有）"""
def getImprintInformation(bsObj):
    pass


"""这个函数是获取Imprint大块中的Imprint Method板块（如果有）"""
def getImprintMethod(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    ImprintDiv = allData[2]
    ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    BlockMap = {}
    ImprintCharge = {}

    for dataFieldBlock in ImprintData:
        BlockName = dataFieldBlock.find("h5").get_text().strip()
        BlockValue = dataFieldBlock
        BlockMap[BlockName] = BlockValue

    for key in BlockMap.keys():
        block = BlockMap[key]
        if key == "Imprint Method":
            # print key, BlockMap[key]
            ImprintMethodName = block.find("div", class_="setDetail dataFieldBlock").get_text().strip()
            # 如果文中出现charge type，就为ImprintCharge填充数据，如果不出现，那么len(ImprintCharge)=0
            if "Charge Type" in block.get_text().strip():
                ImprintCharge['Upcharge_Name'] = ImprintMethodName
                ImprintCharge['Upcharge_Criteria_1'] = "IMMD:" + ImprintMethodName
                ImprintCharge['Upcharge_Type'] = "Imprint Method Charge"
                if "Per Order" in block.get_text().strip():
                    ImprintCharge['Upcharge_Level'] = "Per Order"
                else:
                    ImprintCharge['Upcharge_Level'] = "Other"
                ImprintCharge['Service_Charge'] = "Required"
                ImprintChargeTable = {}
                ImprintQuantity = block.find("th").get_text().strip()
                ImprintPrice = block.find("td").get_text().strip()
                ImprintChargeTable['UQ1'] = ImprintQuantity
                ImprintChargeTable['UP1'] = ImprintPrice
                ImprintCharge['QuantityPirceTable'] = ImprintChargeTable
                if "Price Includes:" in block.get_text().strip():
                    index = block.get_text().strip().index("Price Includes:")
                    ImprintChargeDetail = block.get_text().strip()[index+len("Price Includes:"):].strip()
                    ImprintCharge['Upcharge_Details'] = ImprintChargeDetail

    return ImprintCharge



"""这个函数是获取Imprint大块中的Artwork & Proofs板块（如果有）"""
def getArtwork_Proofs(bsObj):
    pass


if __name__ == "__main__":
    url = "http://promomart.espwebsite.com/ProductDetails/?productId=551051126"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    html = requests.get(url, headers=headers).content
    bsObj = BeautifulSoup(html, 'html.parser')

    print getImprintMethod(bsObj)
