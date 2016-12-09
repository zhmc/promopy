# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import re

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

        except Exception,e:
            print e

    # print ProductDetailDic
    # print ProductDetailDic.get("Samples")
    print "sample_charge"
    print sample_charge

    try:
        Size_Values = ProductDetailDic.get("Size")
        if "Length" in Size_Values or "Width" in Size_Values or "Height" in Size_Values or '"' in Size_Values:
            Size_Group = "Dimension"
        elif "M" in Size_Values or "L" in Size_Values or "S" in Size_Values:
            Size_Group = "Standard & Numbered"
        elif "oz" in Size_Values or "ml" in Size_Values:
            Size_Group = "Volume/Weight"
        print "Size_group,Size_values"
        print Size_Group, Size_Values
    except Exception,e:
            print e


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

"""这个函数是获取商品的基本信息，包括字段Product_Name，Description，Prod_Image"""
def getBasicInfomation(bsObj):
    BasicInfomation ={}
    BasicInfomation['Product_Name'] =""
    BasicInfomation['Description'] =""
    BasicInfomation['Prod_Image'] =""

    Product_Name = bsObj.find("span", {"class": "prodName"}).get_text().strip()
    BasicInfomation['Product_Name'] = Product_Name
    Description = bsObj.find("div", {"class": "prodDescrFull prepend-top"}).get_text().strip()
    BasicInfomation['Description'] = Description
    picsrc = bsObj.find("input", {"type": "image"})['src']
    BasicInfomation['Description'] = picsrc


"""这个函数是获取Pricing大块中的table和Price Includes信息"""
def getPricing(bsObj):
    Pricing = {}
    Pricing['PirceTable'] = {}
    Pricing['Price Includes'] = ''
    PirceTable = {}
    PirceTable['Quantity'] = []
    PirceTable['Price'] = []

    allData = bsObj.findAll("div", class_="attributesContainer")
    PriceingDiv = allData[0]
    # 这里只处理又有一个表格的简单情况
    trs = PriceingDiv.findAll("tr")
    # print "trs", len(trs)
    row_Quantity = trs[0].findAll("th")
    for th in row_Quantity:
        PirceTable['Quantity'].append(th.get_text().strip())

    row_Price = trs[1].findAll("td")
    for td in row_Price:
        PirceTable['Price'].append(td.get_text().strip())

    Pricing['PirceTable'] = PirceTable

    if "Price Includes:" in PriceingDiv.get_text().strip():
        # 这个地方用rfind而不是index，是为了从后往前找，防止有两条Price Includes而出错
        index = PriceingDiv.get_text().strip().rfind("Price Includes:")
        Price_Includes = PriceingDiv.get_text().strip()[index + len("Price Includes:"):].strip()
        # 这地方有一段隐藏文本Add to Shopping Cart
        Price_Includes = Price_Includes.replace("Add to Shopping Cart","").strip()
        Pricing['Price_Includes'] = Price_Includes

    return Pricing

"""这个函数是获取ProductDetail大块中的除了Samples板块的基本信息
字段包括Category，Material,Color,Size_Group, Size_Values, Shape,	Shipping Dimensions, Shipping Estimate
"""
def getProductDetail(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    ProductDetailDiv = allData[1]
    ProductDetailData = ProductDetailDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    ProductDetailData2 = ProductDetailDiv.findAll("div", class_="dataFieldBlock")

    ProductDetail = {}
    ProductDetail['Shape'] = ""

    for dataFieldBlock in ProductDetailData2:
        if "h5" in dataFieldBlock.prettify():
            BlockName = dataFieldBlock.find("h5").get_text().strip()
            if "Category" in BlockName:
                category = ""
                CateList = dataFieldBlock.get_text().strip().replace("Category","").split(";")
                for cate in CateList:
                    cate_clean = cate.strip()
                    if len(cate_clean) > 0:
                        category += cate_clean +","
                if len(category) > 0:
                    category = category[0:len(category)-1]
                ProductDetail['Category'] = category
            elif "Material" in BlockName:
                category = ""
                CateList = dataFieldBlock.get_text().strip().replace("Material", "").split(",")
                for cate in CateList:
                    cate_clean = cate.strip()
                    if len(cate_clean) > 0:
                        category += cate_clean + ","
                if len(category) > 0:
                    category = category[0:len(category) - 1]

                ProductDetail['Material'] = category
            elif "Color" in BlockName:
                category = ""
                CateList = dataFieldBlock.get_text().strip().replace("Color", "").split(",")
                for cate in CateList:
                    cate_clean = cate.strip()
                    if len(cate_clean) > 0:
                        category += cate_clean + ","
                if len(category) > 0:
                    category = category[0:len(category) - 1]
                ProductDetail['Color'] = category
            elif "Size" in BlockName:
                Size_Group = ""
                rawSize_Values = dataFieldBlock.get_text().strip().replace("Size", "").strip()
                Size_Values = ""

                if "Length" in rawSize_Values or "Width" in rawSize_Values or "Height" in rawSize_Values or '"' in rawSize_Values:
                    Size_Group = "Dimension"
                    splitSize_Values = rawSize_Values.split("x")
                    if len(splitSize_Values) == 3:
                        length = splitSize_Values[0].replace('"','').strip()
                        width = splitSize_Values[1].replace('"','').strip()
                        height = splitSize_Values[2].replace('"','').strip()
                        Size_Values = "Length:" + length + ":in;Width:" +width + ":in;Height:" + height + ":in"
                    elif len(splitSize_Values) == 2:
                        length = splitSize_Values[0].replace('"', '').strip()
                        width = splitSize_Values[1].replace('"', '').strip()
                        Size_Values = "Length:" + length + ":in;Width:" + width + ":in"
                    elif len(splitSize_Values) == 1:
                        length = splitSize_Values[0].replace('"', '').strip()
                        Size_Values = "Length:" + length + ":in"
                elif "M" in rawSize_Values or "L" in rawSize_Values or "S" in rawSize_Values:
                    Size_Group = "Standard & Numbered"
                    Size_Values = rawSize_Values.replace(" ","")
                elif "oz" in rawSize_Values or "ml" in rawSize_Values or "kg" in rawSize_Values:
                    Size_Group = "Volume/Weight"
                    if "oz" in rawSize_Values:
                        splitSize_Values = rawSize_Values.split("oz")
                        if len(splitSize_Values) > 1:
                            for i in range(len(splitSize_Values)):
                                num = splitSize_Values[i].replace(",","").strip()
                                if len(num) > 0:
                                        Size_Values = Size_Values + num +":oz,"
                            if len(Size_Values) > 0:
                                Size_Values = Size_Values[0:len(Size_Values) - 1]
                        else:
                            num = rawSize_Values.replace("oz","").strip()
                            Size_Values = Size_Values + num + ":oz"
                    elif "ml" in rawSize_Values:
                        splitSize_Values = rawSize_Values.split("ml")
                        if len(splitSize_Values) > 1:
                            for i in range(len(splitSize_Values)):
                                num = splitSize_Values[i].replace(",","").strip()
                                if len(num) > 0:
                                    Size_Values = Size_Values + num + ":ml;"
                            if len(Size_Values) > 0:
                                Size_Values = Size_Values[0:len(Size_Values) - 1]
                        else:
                            num = rawSize_Values.replace("ml","").strip()
                            Size_Values = Size_Values + num + ":ml"
                    elif "kg" in rawSize_Values:
                        splitSize_Values = rawSize_Values.split("kg")
                        if len(splitSize_Values) > 1:
                            for i in range(len(splitSize_Values)):
                                num = splitSize_Values[i].replace(",","").strip()
                                if len(num) > 0:
                                    Size_Values = Size_Values + num +":kg,"
                            if len(Size_Values) > 0:
                                Size_Values = Size_Values[0:len(Size_Values) - 1]
                        else:
                            num = rawSize_Values.replace("kg","").strip()
                            Size_Values = Size_Values + num + ":kg"
                ProductDetail['Size_Group'] = Size_Group
                ProductDetail['Size_Values'] = Size_Values
            elif "Shipping Dimensions" in BlockName:
                Size_Values = ""
                rawSize_Values = dataFieldBlock.get_text().strip().replace("Shipping Dimensions","").strip()
                if "x" in rawSize_Values:
                    splitSize_Values = rawSize_Values.split("x")
                    if len(splitSize_Values) == 3:
                        length = splitSize_Values[0].replace('"', '').strip()
                        width = splitSize_Values[1].replace('"', '').strip()
                        height = splitSize_Values[2].replace('"', '').strip()
                        Size_Values = length + ":in;" + width + ":in;" + height + ":in"
                    elif len(splitSize_Values) == 2:
                        length = splitSize_Values[0].replace('"', '').strip()
                        width = splitSize_Values[1].replace('"', '').strip()
                        Size_Values = length + ":in;" + width + ":in"
                    elif len(splitSize_Values) == 1:
                        length = splitSize_Values[0].replace('"', '').strip()
                        Size_Values = length + ":in"
                ProductDetail['Shipping_Dimensions'] = Size_Values
            elif "Shipping Estimate" in BlockName:
                rawEstimate = dataFieldBlock.get_text().strip().replace("Shipping Estimate","").strip()
                num = rawEstimate[0:rawEstimate.index("per")].strip()
                other = rawEstimate.replace(num,"").strip()
                Estimate = num +":"+other
                ProductDetail['Shipping_Items'] = Estimate
            elif "Shape" in BlockName:
                shapeindex = dataFieldBlock.get_text().strip().index("Shape")
                shape = ""
                rawShape = dataFieldBlock.get_text().strip()[shapeindex+len("Shape"):].strip()
                CateList = rawShape.split(",")
                for cate in CateList:
                    cate_clean = cate.strip()
                    if len(cate_clean) > 0:
                        shape += cate_clean + ","
                if len(shape) > 0:
                    shape = shape[0:len(shape) - 1]
                ProductDetail['Shape'] = shape

    return ProductDetail

"""这个函数是获取ProductDetail大块中的Samples板块（如果有），会生成csv中的sample charge"""
def getSampleCharge(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    ProductDetailDiv = allData[1]
    ProductDetailData = ProductDetailDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")

    SampleCharge = {}

    for dataFieldBlock in ProductDetailData:
        if "h5" in dataFieldBlock.prettify():
            BlockName = dataFieldBlock.find("h5").get_text().strip()
            if "amples" in BlockName:
                if "Charge Type" in dataFieldBlock.prettify():
                    SampleCharge['Upcharge_Name'] = 'Product Sample'
                    SampleCharge['Upcharge_Criteria_1'] = 'SMPL:Product Sample'
                    SampleCharge['Upcharge_Type'] = 'Sample Charge'
                    SampleCharge['Upcharge_Level'] = 'Other'
                    SampleCharge['Service_Charge'] = 'Optional'

                    SampleChargeTable = {}
                    SampleQuantity = dataFieldBlock.findAll("tr")[0].findAll("th")[1].get_text().strip()
                    SamplePrice = dataFieldBlock.find("td").get_text().strip()
                    SampleChargeTable['UQ1'] = SampleQuantity
                    SampleChargeTable['UP1'] = SamplePrice
                    SampleChargeTable['UD1'] = "Z"
                    SampleCharge['QuantityPirceTable'] = SampleChargeTable
                    if "Price Includes:" in dataFieldBlock.get_text().strip():
                        index = dataFieldBlock.get_text().strip().rfind("Price Includes:")
                        ArtworkChargeDetail = dataFieldBlock.get_text().strip()[index + len("Price Includes:"):].strip()
                        # 如果Detail中有N/A,那么设为空
                        if "N/A" in ArtworkChargeDetail:
                            ArtworkChargeDetail = ""
                        SampleCharge['Upcharge_Details'] = ArtworkChargeDetail


    return SampleCharge

"""这个函数是获取Imprint大块中的Imprint Information板块（肯定有）, 同时获取可能存在的Imprint Location板块"""
def getImprintInformation(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    ImprintDiv = allData[2]
    ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    BlockMap = {}
    ImprintDic = {}
    ImprintMethodName = ""
    ImprintBasicInfo = {}
    # 赋值 默认为空。返回的字段
    ImprintBasicInfo["Sold_Unimprinted"] = ""
    ImprintBasicInfo["Personalization"] = ""
    ImprintBasicInfo["Imprint_Size"] = ""
    ImprintBasicInfo["Imprint Method"] = ""
    ImprintBasicInfo["Imprint Color"] = ""
    ImprintBasicInfo["Imprint Location"] = ""

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

    return ImprintBasicInfo


"""这个函数是获取Imprint大块中的Imprint Method板块（如果有，会产生ImprintCharge）"""
def getImprintMethodCharge(bsObj):
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
        if key == "Imprint Method":
            block = BlockMap[key]
            # print key, BlockMap[key]
            ImprintMethodName = block.find("div", class_="setDetail dataFieldBlock").get_text().strip()
            # 只要有Imprint Method板块，len(ImprintCharge) > 0
            ImprintCharge['Upcharge_Name'] = ImprintMethodName
            
            # 如果文中出现charge type，就为ImprintCharge填充数据，如果不出现，那么len(ImprintCharge)=1
            if "Charge Type" in block.get_text().strip():
                
                ImprintCharge['Upcharge_Criteria_1'] = "IMMD:" + ImprintMethodName
                ImprintCharge['Upcharge_Type'] = "Imprint Method Charge"
                if "Per Order" in block.get_text().strip():
                    ImprintCharge['Upcharge_Level'] = "Per Order"
                else:
                    ImprintCharge['Upcharge_Level'] = "Other"
                ImprintCharge['Service_Charge'] = "Required"
                # 加价table
                ImprintChargeTable = {}
                ImprintQuantity = block.findAll("tr")[0].findAll("th")[1].get_text().strip()
                ImprintPrice = block.find("td").get_text().strip()
                ImprintChargeTable['UQ1'] = ImprintQuantity
                ImprintChargeTable['UP1'] = ImprintPrice
                ImprintChargeTable['UD1'] = "Z"
                ImprintCharge['QuantityPirceTable'] = ImprintChargeTable
                if "Price Includes:" in block.get_text().strip():
                    index = block.get_text().strip().index("Price Includes:")
                    ImprintChargeDetail = block.get_text().strip()[index+len("Price Includes:"):].strip()
                    ImprintCharge['Upcharge_Details'] = ImprintChargeDetail

    return ImprintCharge



"""这个函数是获取Imprint大块中的Artwork & Proofs板块（如果有，会产生ArtworkCharge）"""
def getArtwork_Proofs(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    ImprintDiv = allData[2]
    ImprintData = ImprintDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    BlockMap = {}
    ArtworkCharge = {}
    # 初始化字典里面的变量
    ArtworkCharge['Upcharge_Name'] = ""
    ArtworkCharge['Upcharge_Criteria_1'] = ""
    ArtworkCharge['Upcharge_Type'] = ""
    ArtworkCharge['Upcharge_Level'] = ""
    ArtworkCharge['Service_Charge'] = ""
    ArtworkCharge['QuantityPirceTable'] = ""
    ArtworkCharge['QuantityPirceTable'] = {}
    ArtworkCharge['Upcharge_Details'] = ""


    for dataFieldBlock in ImprintData:
        BlockName = dataFieldBlock.find("h5").get_text().strip()
        BlockValue = dataFieldBlock
        BlockMap[BlockName] = BlockValue

    for key in BlockMap.keys():
        if key == "Artwork & Proofs":
            block = BlockMap[key]
            ArtworkName = block.find("div", class_="setDetail dataFieldBlock").get_text().strip()
            # 只要有Artwork & Proofs板块，len(ArtworkCharge) > 0
            ArtworkCharge['Upcharge_Name'] = ArtworkName

            # 如果有Artwork & Proofs板块但是内容很简单，没有charge type, 那么前面找ArtworkName会找不到
            if len(ArtworkCharge['Upcharge_Name']) == 0 and "Charge Type" not in block.get_text().strip():
                ArtworkCharge['Upcharge_Name'] = block.get_text().strip().replace("Artwork & Proofs","").strip()

            # 如果文中出现charge type，就为ArtworkCharge填充数据，如果不出现，那么ArtworkCharge['Upcharge_Type'] = ""
            if "Charge Type" in block.get_text().strip():
                ArtworkCharge['Upcharge_Criteria_1'] = "ARTW:" + ArtworkName
                ArtworkCharge['Upcharge_Type'] = "Artwork Charge"
                ArtworkCharge['Upcharge_Level'] = "Other"
                ArtworkCharge['Service_Charge'] = "Optional"
                # 加价table
                ArtworkChargeTable = {}
                ArtworkQuantity = block.findAll("tr")[0].findAll("th")[1].get_text().strip()
                ArtworkPrice = block.find("td").get_text().strip()
                ArtworkChargeTable['UQ1'] = ArtworkQuantity
                ArtworkChargeTable['UP1'] = ArtworkPrice
                ArtworkChargeTable['UD1'] = "Z"
                ArtworkCharge['QuantityPirceTable'] = ArtworkChargeTable
                if "Price Includes:" in block.get_text().strip():
                    index = block.get_text().strip().rfind("Price Includes:")
                    ArtworkChargeDetail = block.get_text().strip()[index+len("Price Includes:"):].strip()
                    # 如果Detail中有N/A,那么设为空
                    if "N/A" in ArtworkChargeDetail:
                        ArtworkChargeDetail = ""
                    ArtworkCharge['Upcharge_Details'] = ArtworkChargeDetail

    return ArtworkCharge


"""这个函数是获取Production and Shipping大块中Production Information小版块的信息,再加上Packaging小版块
获取Production Time，Rush Service，Rush Time，Shipping Weight，Shipping_Info等字段"""
def getProductionInformation(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    Production_ShippingDiv = allData[3]
    Production_ShippingData = Production_ShippingDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    ProductionInformation = {}

    # 产地全部统一为中国
    ProductionInformation["Origin"] = "CHINA"
    ProductionInformation["Shipper_Bills_By"] = ""
    ProductionInformation["Ship_Plain_Box"] = "N"
    ProductionInformation["Production_Time"] = ""
    ProductionInformation["Rush_Service"] = ""
    ProductionInformation["Rush_Time"] = ""
    ProductionInformation["Shipping_Weight"] = ""
    ProductionInformation["Shipping_Info"] = ""
    ProductionInformation["Packaging"] = ""

    for dataFieldBlock in Production_ShippingData:
        # 这个地方有个坑，别的标题都是<h5>，这个Production Information的标题是<h6>
        if "h6" in dataFieldBlock.prettify():
            BlockName = dataFieldBlock.find("h6").get_text().strip()
            if BlockName == "Production Information":
                ProductionInfoList = dataFieldBlock.findAll("div", class_="dataFieldBlock")
                for ProdInfo in ProductionInfoList:
                    ProdInfoClean = ProdInfo.get_text().strip()
                    if "Production Time" in ProdInfoClean:
                        rawtext = ProdInfoClean.replace("Production Time","").strip()
                        if "-" in rawtext:
                            begin = re.match(r'(\d+?)\D*?(\d+?) business days',rawtext).group(1)
                            end = re.match(r'(\d+?)\D*?(\d+?) business days',rawtext).group(2)
                            # print begin,end
                            ProductionInformation["Production_Time"] = str(begin)+","+str(end)
                        else:
                            begin = re.match(r'(\d+?) business days',rawtext).group(1)
                            ProductionInformation["Production_Time"] = str(begin)
                    elif "Rush Service" in ProdInfoClean:
                        if "Yes" in ProdInfoClean:
                            ProductionInformation["Rush_Service"] = "Y"
                        else:
                            ProductionInformation["Rush_Service"] = ""
                    elif "Rush Time" in ProdInfoClean:
                        rawtext = ProdInfoClean.replace("Rush Time", "").strip()
                        if "-" in rawtext:
                            match = re.match(r'(\d+?)\D*?(\d+?) business days',rawtext)
                            if match:
                                begin = match.group(1)
                                end = match.group(2)
                            # print begin,end
                            ProductionInformation["Rush_Time"] = str(begin)+":"+","+str(end)+":"
                        else:
                            begin = re.match(r'(\d+?) business days',rawtext).group(1)
                            ProductionInformation["Rush_Time"] = str(begin)+":"
                    elif "Shipping Weight" in ProdInfoClean:
                        rawtext = ProdInfoClean.replace("Shipping Weight", "").strip()
                        rawweight = ""
                        weight = ""
                        ShippingInfo = ""
                        if "kg" in rawtext :
                            index = rawtext.index("kg")
                            rawweight = rawtext[0:index + len("kg")].strip()
                            weight = rawweight.replace("kg", "").strip() + ":" + "kg"
                        elif "oz" in rawtext:
                            index = rawtext.index("oz")
                            rawweight = rawtext[0:index + len("oz")].strip()
                            weight = rawweight.replace("oz", "").strip() + ":" + "oz"
                        elif "lbs" in rawtext:
                            index = rawtext.index("lbs")
                            rawweight = rawtext[0:index+len("lbs")].strip()
                            weight = rawweight.replace("lbs","").strip() + ":" + "lbs"
                        elif "grams" in rawtext:
                            index = rawtext.index("grams")
                            rawweight = rawtext[0:index + len("grams")].strip()
                            weight = rawweight.replace("grams", "").strip() + ":" + "grams"
                        else:
                            pass
                        ProductionInformation["Shipping_Weight"] = weight
                        ShippingInfo = rawtext.replace(rawweight,"").strip()
                        ProductionInformation["Shipping_Info"] = ShippingInfo

        #  顺便把packaging字段获取
        elif "h5" in dataFieldBlock.prettify():
            BlockName = dataFieldBlock.find("h5").get_text().strip()
            if "Packaging" in BlockName:
                packagingInfo = dataFieldBlock.get_text().strip().replace("Packaging", "").strip()
                ProductionInformation['Packaging'] = packagingInfo

    return ProductionInformation



"""这个函数是获取Production and Shipping大块中Rush Time小版块的信息,如果有这个版块，那么产生一个Rush Service Charge的UPcharge
获取Upcharge_Name，Upcharge_Criteria_1，QuantityPirceTable等字段"""
# 麻烦在于Rush Time小版块中可能会有两张表，记录不同的rush time服务时间，价格只能一个，表里面只能放一种价格
# 经过观察，rushtime服务时间和之前获取的时间一样，只要获取价格
def getRushServiceCharge(bsObj):
    RushServiceCharge = {}
    RushServiceCharge['Upcharge_Name'] = ""
    RushServiceCharge['Upcharge_Criteria_1'] = ""
    basicInfo = getProductionInformation(bsObj)
    # if len(basicInfo.get('Rush_Time')) > 0:
    allData = bsObj.findAll("div", class_="attributesContainer")
    Production_ShippingDiv = allData[3]
    Production_ShippingData = Production_ShippingDiv.findAll("div", class_="criteriaSetBox dataFieldBlock")
    for dataFieldBlock in Production_ShippingData:
        if "h5" in dataFieldBlock.prettify():
            BlockName = dataFieldBlock.find("h5").get_text().strip()
            if "Rush Time" in BlockName:
                #判断是否存在Rush Service Charge
                if "Charge Type" in dataFieldBlock.prettify():

                    RushServiceCharge['Upcharge_Type'] = "Rush Service Charge"
                    RushServiceCharge['Upcharge_Level'] = "Other"
                    RushServiceCharge['Service_Charge'] = "Required"

                    rushtimestr = basicInfo.get('Rush_Time')
                    # print rushtimestr
                    # 判读rushtime有几个值，1个还是2个
                    if "," in rushtimestr:
                        match1 = re.match(r'(\d*?):,(\d*?):', rushtimestr)
                        if match1:
                            begin = match1.group(1)
                            end = match1.group(2)
                            RushServiceCharge['Upcharge_Name'] = begin + " business days,"+end+" business days"
                            RushServiceCharge['Upcharge_Criteria_1'] = "RUSH:" + begin +"," + end
                    # 如果rushtime只有1个值
                    elif len(rushtimestr) > 0:
                        rushtime = rushtimestr.replace(":","").strip()
                        RushServiceCharge['Upcharge_Name'] = rushtime + " business days"
                        RushServiceCharge['Upcharge_Criteria_1'] = "RUSH:" + rushtime

                    #获取Charge Price
                    RushChargeTable = {}
                    RushQuantity = dataFieldBlock.findAll("tr")[0].findAll("th")[1].get_text().strip()
                    RushPrice = dataFieldBlock.find("td").get_text().strip()
                    RushChargeTable['UQ1'] = RushQuantity
                    RushChargeTable['UP1'] = RushPrice
                    RushChargeTable['UD1'] = "Z"
                    RushServiceCharge['QuantityPirceTable'] = RushChargeTable
                    if "Price Includes:" in dataFieldBlock.get_text().strip():
                        index = dataFieldBlock.get_text().strip().rfind("Price Includes:")
                        ArtworkChargeDetail = dataFieldBlock.get_text().strip()[index + len("Price Includes:"):].strip()
                        # 如果Detail中有N/A,那么设为空
                        if "N/A" in ArtworkChargeDetail:
                            ArtworkChargeDetail = ""
                        RushServiceCharge['Upcharge_Details'] = ArtworkChargeDetail

    return RushServiceCharge


"""最终写入csv文件中的时候，每个字段都要两边加上两个双引号，第二个双引号后面加上逗号，来保证不被逗号分隔错"""
def addQuot(rawstr):
    str1 = str(rawstr)
    str2 = '"'+str1+'"'+','
    return str2

if __name__ == "__main__":
    url = "http://promomart.espwebsite.com/ProductDetails/?productId=551052073"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    html = requests.get(url, headers=headers).content
    bsObj = BeautifulSoup(html, 'html.parser')

    print getProductDetail(bsObj)
    print getPricing(bsObj)


