# -*- coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import re

class Prodouct(object):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = ""       #  商品页地址
    # bsObj = BeautifulSoup("","html.parser")
    # 第A列XID全空（不预先填值）
    Product_Name = ""   #   第B列
    Product_Number = ""   #   第C列无法得到
    # D, E, F, G列全空
    Description = ""    #   第H列
    # 第I列summary无法得到
    Prod_Image = ""      #   第J列
    # K列全空
    Category = ""     #   第L列
    # 第M列Keywords无法得到
    Product_Color = ""     #   第N列
    Material = ""     #   第O列
    Size_Group = ""   #   第P列
    Size_Values = ""   #   第Q列
    Shape = ""        #   第R列
    # 第S列, T列无法得到
    Origin = "CHINA"   #   第U列
    # V, W, X, Y, Z, AA列全空
    Imprint_Method = ""  # 第AB列
    # 第AC列Linename (EXPORT ONLY)
    Artwork = ""       # 第AD列
    Imprint_Color = ""       # 第AE列
    Sold_Unimprinted = ""       # 第AF列
    Personalization = ""       # 第AG列
    Imprint_Size = ""       # 第AH列
    Imprint_Location = ""       # 第AI列
    # 第AJ列, AK列无法得到
    Product_Sample = "Y"       # 第AL列
    # AM列全空
    Production_Time = ""      # 第AN列
    Rush_Service = ""       # 第AO列
    Rush_Time = ""         # 第AP列
    # AQ列全空
    Packaging= ""       # 第AR列
    Shipping_Items= ""       # 第AS列
    Shipping_Dimensions= ""       # 第AT列
    Shipping_Weight= ""       # 第AU列
    # 第AV列Shipper_Bills_By 无法得到
    Shipping_Info= ""       # 第AW列
    Ship_Plain_Box= "N"       # 第AX列
    Comp_Cert= ""       # 第AY列
    # AZ, BA, BC, BB, BD列全空
    Base_Price_Name= ""      # 第BE列，能够从页面获取
    # 第BF列, BG列无法得到
    Pricing = {}

    # 从第BH列到BQ列是商品的Quantity
    # 从第BR列到CA列是商品的Pricing
    # 从第CB列到CK列，之前的Quantity有几项有值，这里就有几项全是R，后面的为空

    # CL列Product_Number_Price全空

    Price_Includes= ""       # 第CM列
    # 第CN列QUR_Flag 无法得到
    Currency= "USD"       # 第CO列
    # 第CP列Less_Than_Min 无法得到
    Price_Type = "List"  # 第CQ列

    #从CR到EC都是upcharge内容。在写入csv时要分行写。新的一行只填写XID和upcharge内容，其余为空
    ImprintMethodCharge_exist = 0 # 是否存在ImprintMethodCharge
    ImprintMethodCharge = {}

    SampleCharge_exist = 0  # 是否存在SampleCharge
    SampleCharge = {}

    ArtworkCharge_exist = 0  # 是否存在ArtworkCharge
    ArtworkCharge = {}

    RushServiceCharge_exist = 0  # 是否存在RushServiceCharge
    RushServiceCharge = {}

    Confirmed_Thru_Date= ""       # 第ED列
    # 从EE到EO全空
    Distributor_View_Only = "N"  # 第EP列
    # EQ, ER全为空
    # ES列Item_Weight无法获取
    # ET, EU全为空
    Industry_Segment = "Promotional"  # 第EV列
    SEO_FLG = "N"  # 第EW列
    # EX, EY全为空
    Item_Assembled = "Y"  # 第EZ列
    Delivery_Option = "None"  # 第FA列
    # FB, FC, FD, FE都是EXPORT ONLY！


    def __init__(self, url):
        self.url = url

    @property
    def to_csv_row(self):
        csvRowList = []
        csv_row = ""
        csvRowList.append(csv_row)
        # 写入csv文件时，只有那些quantity字段不用加上双引号

        csv_row += ","          # 第A列XID全空（不预先填值）
        csv_row += addQuot(self.Product_Name)     #  第B列
        csv_row += addQuot(self.Product_Number)   #   第C列
        csv_row += ","*4          # D, E, F, G列全空
        csv_row += addQuot(self.Description)     #   第H列
        csv_row += ","              # 第I列summary无法得到
        csv_row += ","               #   第J列Prod_Image要手动填入
        csv_row += ","               # K列全空
        csv_row += addQuot(self.Category)       #   第L列
        csv_row += ","              # 第M列Keywords无法得到
        csv_row +=  addQuot(self.Product_Color)     #   第N列
        csv_row +=  addQuot(self.Material)        #   第O列
        csv_row +=  addQuot(self.Size_Group)        #   第P列
        csv_row +=  addQuot(self.Size_Values)        #   第Q列
        csv_row +=  addQuot(self.Shape)        #   第Q列
        csv_row += ","*2               # 第S列, T列无法得到
        csv_row +=  addQuot(self.Origin)        #   第U列
        csv_row += ","*6             # V, W, X, Y, Z, AA列全空
        csv_row +=  addQuot(self.Imprint_Method)        # 第AB列
        csv_row += ","         # 第AC列Linename (EXPORT ONLY)
        csv_row +=  addQuot(self.Artwork)        #   第AD列
        csv_row +=  addQuot(self.Imprint_Color)        #   第AE列
        csv_row +=  addQuot(self.Sold_Unimprinted)        #   第AF列
        csv_row +=  addQuot(self.Personalization)        #   第AG列
        csv_row +=  addQuot(self.Imprint_Size)        #   第AH列
        csv_row +=  addQuot(self.Imprint_Location)        #   第AI列
        csv_row += "," * 2                # 第AJ列, AK列无法得到
        csv_row +=  addQuot(self.Product_Sample)        #   第AL列
        csv_row += ","                         # AM列全空
        csv_row += addQuot(self.Production_Time)      # 第AN列
        csv_row += addQuot(self.Rush_Service)       # 第AO列
        csv_row += addQuot(self.Rush_Time)         # 第AP列
        csv_row += ","                       # AQ列全空
        csv_row += addQuot(self.Packaging)         # 第AR列
        csv_row += addQuot(self.Shipping_Items)         # 第AS列
        csv_row += addQuot(self.Shipping_Dimensions)         # 第AT列
        csv_row += addQuot(self.Shipping_Weight)         # 第AU列
        csv_row += ","                         # 第AV列Shipper_Bills_By 无法得到
        csv_row += addQuot(self.Shipping_Info)         # 第AW列
        csv_row += addQuot(self.Ship_Plain_Box)         # 第AX列
        csv_row += addQuot(self.Comp_Cert)         # 第AY列
        csv_row += "," * 5                         # AZ, BA, BC, BB, BD列全空
        csv_row += addQuot(self.Base_Price_Name)         # 第BE列Base_Price_Name
        csv_row += "," * 2                   # 第BF列, BG列无法得到

        # 从第BH列到BQ列是商品的Quantity
        # 从第BR列到CA列是商品的Pricing
        # 从第CB列到CK列，之前的Quantity有几项有值，这里就有几项全是R，后面的为空

        quantityList = [","] * 10
        priceList = [","] * 10
        whatDList = [","] * 10

        pp = self.Pricing
        # 这一段已经给price和什么D字段加上了双引号
        if 'PirceTable' in pp:
            if 'Quantity' in pp['PirceTable'].keys():
                if len(pp['PirceTable']['Quantity']) > 1:
                    cutHeadList = pp['PirceTable']['Quantity'][1:]
                    for i in range(len(cutHeadList)):
                        quantityList[i] = addQuot(deleteDollar(cutHeadList[i]).replace(",","").strip())
                        whatDList[i] = addQuot("R")
            if 'Price' in pp['PirceTable'].keys():
                if len(pp['PirceTable']['Price']) > 1:
                    cutHeadList = pp['PirceTable']['Price'][1:]
                    for i in range(len(cutHeadList)):
                        priceList[i] = addQuot(deleteDollar(cutHeadList[i]))

        for item in quantityList:
            csv_row += item
        for item in priceList:
            csv_row += item
        for item in whatDList:
            csv_row += item

        csv_row += ","                             # CL列Product_Number_Price全空
        csv_row += addQuot(self.Price_Includes)          # 第CM列
        csv_row += ","                             # 第CN列QUR_Flag 无法得到
        csv_row += addQuot(self.Currency)          # 第CO列
        csv_row += ","                             # 第CP列Less_Than_Min 无法得到
        csv_row += addQuot(self.Price_Type)          # 第CQ列

        # 从CR到EC都是upcharge内容。在写入csv时要分行写。新的一行只填写XID和upcharge内容，其余为空
        # 此处要判断该商品有几个upcharge。
        upchargeList = []
        upchargeRowList = []


        if self.ImprintMethodCharge_exist:
            upchargeList.append(self.ImprintMethodCharge)
        if self.SampleCharge_exist:
            upchargeList.append(self.SampleCharge)
        if self.ArtworkCharge_exist:
            upchargeList.append(self.ArtworkCharge)
        if self.RushServiceCharge_exist:
            upchargeList.append(self.RushServiceCharge)

        for upcharge in upchargeList:
            upcharge_row = ""
            upcharge_row += addQuot(upcharge['Upcharge_Name'])         # 第CR列
            upcharge_row += addQuot(upcharge['Upcharge_Criteria_1'])   # 第CS列
            upcharge_row += ","                                       # 第CT列Upcharge_Criteria_2全空
            upcharge_row += addQuot(upcharge['Upcharge_Type'])         # 第CU列
            upcharge_row += addQuot(upcharge['Upcharge_Level'])         # 第CV列
            upcharge_row += addQuot(upcharge['Service_Charge'])         # 第CW列
            upcharge_row += addQuot(upcharge['UQ1'])                  # 第CX列
            upcharge_row += ","*9           #从CY到DG是空行
            upcharge_row += addQuot(deleteDollar(upcharge['UP1']))  # 第DH列
            upcharge_row += "," * 9          # 从DI到DQ是空行
            upcharge_row += addQuot("Z")             # 第DR列全是Z
            upcharge_row += "," * 9                # 从DS到EA是空行
            upcharge_row += addQuot(upcharge['Upcharge_Details'])  # 第EB列
            upcharge_row += ","               # 第EC列U_QUR_Flag全空

            upchargeRowList.append(upcharge_row)

        if len(upchargeRowList) > 0:
            csv_row += upchargeRowList[0]
            if len(upchargeRowList) > 1:
                csv_row2 = ","*95 + upchargeRowList[1] + ","*27
                csvRowList.append(csv_row2)
                if len(upchargeRowList) > 2:
                    csv_row3 = ","*95 + upchargeRowList[2] + ","*27
                    csvRowList.append(csv_row3)
                    if len(upchargeRowList) > 3:
                        csv_row4 = "," * 95 + upchargeRowList[3] + "," * 27
                        csvRowList.append(csv_row4)
        else:
            csv_row += "," *38  # 一个upcharge都没有的话，填充空列，从CR到EC

        csv_row += ","           # ED列的Confirmed_Thru_Date项确定不了
        csv_row += "," * 11      # 从EE到EO全空
        csv_row += addQuot(self.Distributor_View_Only)   # 第EP列
        # EQ, ER全为空
        # ES列Item_Weight无法获取
        # ET, EU全为空
        csv_row += "," * 5
        csv_row += addQuot(self.Industry_Segment)            # 第EV列
        csv_row += addQuot(self.SEO_FLG)                    # 第EW列
        csv_row += "," * 2      # EX, EY全为空
        csv_row += addQuot(self.Item_Assembled)                    # 第EZ列
        csv_row += addQuot(self.Delivery_Option)                    # 第FA列
        csv_row += "," * 3                                # FB, FC, FD, FE都是EXPORT ONLY！

        csvRowList[0] = csv_row

        return csvRowList


def parser(productObject):
    # productObject = Prodouct(productObject.url)
    html = requests.get(productObject.url, headers=productObject.headers).content
    bsObj = BeautifulSoup(html, 'html.parser')
    allData = bsObj.findAll("div", class_="attributesContainer")
    # 判断能不能获取信息
    if len(allData) > 0:

        BasicInfomation = getBasicInfomation(bsObj)
        productObject.Product_Name = BasicInfomation['Product_Name']
        productObject.Description = BasicInfomation['Description']
        productObject.Prod_Image = BasicInfomation['Prod_Image']

        Pricing = getPricing(bsObj)
        productObject.Pricing = Pricing
        productObject.Price_Includes = Pricing['Price_Includes']
        productObject.Base_Price_Name = Pricing['Base_Price_Name']

        ProductDetail = getProductDetail(bsObj)
        productObject.Category = ProductDetail['Category']
        productObject.Material = ProductDetail['Material']
        productObject.Product_Color = ProductDetail['Color']
        productObject.Size_Group = ProductDetail['Size_Group']
        productObject.Size_Values = ProductDetail['Size_Values']
        productObject.Shape = ProductDetail['Shape']
        productObject.Shipping_Dimensions = ProductDetail['Shipping_Dimensions']
        productObject.Shipping_Items = ProductDetail['Shipping_Items']

        SampleCharge = getSampleCharge(bsObj)
        if 'Upcharge_Type' in SampleCharge.keys():
            if len(SampleCharge['Upcharge_Type']) > 0:
                productObject.SampleCharge_exist = 1
                productObject.SampleCharge = SampleCharge

        ImprintBasicInfo = getImprintInformation(bsObj)
        productObject.Sold_Unimprinted = ImprintBasicInfo['Sold_Unimprinted']
        productObject.Personalization = ImprintBasicInfo['Personalization']
        productObject.Imprint_Size = ImprintBasicInfo['Imprint_Size']
        productObject.Imprint_Method = ImprintBasicInfo['Imprint_Method']
        productObject.Imprint_Color = ImprintBasicInfo['Imprint_Color']
        productObject.Imprint_Location = ImprintBasicInfo['Imprint_Location']

        ImprintCharge = getImprintMethodCharge(bsObj)
        if 'Upcharge_Type' in ImprintCharge.keys():
            productObject.ImprintMethodCharge_exist = 1
            productObject.ImprintMethodCharge = ImprintCharge

        ArtworkCharge = getArtwork_Proofs(bsObj)
        productObject.Artwork = ArtworkCharge['Upcharge_Name']
        if len(ArtworkCharge['Upcharge_Type']) > 0:
            productObject.ArtworkCharge_exist = 1
            productObject.ArtworkCharge = ArtworkCharge

        ProductionInformation = getProductionInformation(bsObj)
        productObject.Production_Time = ProductionInformation['Production_Time']
        productObject.Rush_Service = ProductionInformation['Rush_Service']
        productObject.Rush_Time = ProductionInformation['Rush_Time']
        productObject.Shipping_Weight = ProductionInformation['Shipping_Weight']
        productObject.Shipping_Info = ProductionInformation['Shipping_Info']
        productObject.Packaging = ProductionInformation['Packaging']

        RushServiceCharge = getRushServiceCharge(bsObj)
        if 'Upcharge_Type' in RushServiceCharge.keys():
            if len(RushServiceCharge['Upcharge_Type']) > 0:
                productObject.RushServiceCharge_exist = 1
                productObject.RushServiceCharge = RushServiceCharge

        Comp_Cert = getComp_Cert(bsObj)
        productObject.Comp_Cert = Comp_Cert


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
    BasicInfomation['Prod_Image'] = picsrc

    return BasicInfomation


"""这个函数是获取Pricing大块中的table和Price Includes， Base_Price_Name信息"""
def getPricing(bsObj):
    Pricing = {}
    Pricing['PirceTable'] = {}
    Pricing['Price_Includes'] = ''
    Pricing['Base_Price_Name'] = ''
    PirceTable = {}
    PirceTable['Quantity'] = []
    PirceTable['Price'] = []

    allData = bsObj.findAll("div", class_="attributesContainer")
    PriceingDiv = allData[0]
    # 这里只处理了有一个表格的简单情况
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

    Base_Price_Name = PriceingDiv.find("span",class_="strong").get_text().strip()
    Pricing['Base_Price_Name'] = Base_Price_Name

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
    ProductDetail['Category'] = ""
    ProductDetail['Material'] = ""
    ProductDetail['Color'] = ""
    ProductDetail['Size_Group'] = ""
    ProductDetail['Size_Values'] = ""
    ProductDetail['Shape'] = ""
    ProductDetail['Shipping_Dimensions'] = ""
    ProductDetail['Shipping_Items'] = ""

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
            elif "Color" == BlockName:
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
                    # 这个地方可能存在多组长宽高
                    if "," in rawSize_Values:
                        #print "存在多组长宽高"
                        firstSplitSize_Values = rawSize_Values.split(",")
                        for item in firstSplitSize_Values:
                            sigleSize_Value = ""
                            splitSize_Values = item.split("x")
                            if len(splitSize_Values) == 3:
                                length = splitSize_Values[0].replace('"', '').strip()
                                width = splitSize_Values[1].replace('"', '').strip()
                                height = splitSize_Values[2].replace('"', '').strip()
                                sigleSize_Value = "Length:" + length + ":in;Width:" + width + ":in;Height:" + height + ":in"
                            elif len(splitSize_Values) == 2:
                                length = splitSize_Values[0].replace('"', '').strip()
                                width = splitSize_Values[1].replace('"', '').strip()
                                sigleSize_Value = "Length:" + length + ":in;Width:" + width + ":in"
                            elif len(splitSize_Values) == 1:
                                length = splitSize_Values[0].replace('"', '').strip()
                                sigleSize_Value = "Length:" + length + ":in"
                            Size_Values += sigleSize_Value + ","
                        if len(Size_Values) > 0:
                            Size_Values = Size_Values[0:len(Size_Values)-1]
                    # 只存在一组长宽高
                    else:
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
                    SampleCharge['Upcharge_Details'] = ""
                    SampleCharge['UQ1'] = ""
                    SampleCharge['UP1'] = ""

                    SampleChargeTable = {}
                    SampleQuantity = dataFieldBlock.findAll("tr")[0].findAll("th")[1].get_text().strip()
                    SamplePrice = dataFieldBlock.find("td").get_text().strip()
                    # 有些表格不写价格，写上QUR
                    if SamplePrice == "QUR":
                        SampleCharge['Upcharge_Type'] = ""
                        continue
                    SampleChargeTable['UQ1'] = SampleQuantity
                    SampleChargeTable['UP1'] = SamplePrice
                    SampleChargeTable['UD1'] = "Z"
                    SampleCharge['QuantityPirceTable'] = SampleChargeTable
                    SampleCharge['UQ1'] = SampleQuantity
                    SampleCharge['UP1'] = SamplePrice
                    if "Price Includes:" in dataFieldBlock.get_text().strip():
                        index = dataFieldBlock.get_text().strip().rfind("Price Includes:")
                        ArtworkChargeDetail = dataFieldBlock.get_text().strip()[index + len("Price Includes:"):].strip()
                        # 如果Detail中有N/A,那么设为空
                        if "N/A" in ArtworkChargeDetail:
                            ArtworkChargeDetail = ""
                        SampleCharge['Upcharge_Details'] = ArtworkChargeDetail


    return SampleCharge


"""
这个地方ImpritDiv里面分为几个板块（如果有），其中Imprint Information板块是始终出现的，
当Imprint Method板块出现时，有时候里面会有charge type，这时会有一个table记录upcharge
当Artwork & Proofs板块出现时，有时候里面会有charge type，这时会有一个table记录upcharge

当一个商品有几个upcharge（包括Sample Charge，Imprint Method Charge，Artwork Charge，Rush Service Charge）
出现时，在csv中第一条记录中的upcharge type项暂时定为记录Imprint Method Charge（如果有），别的就接着主记录行，用一行填上upcharge相关信息
"""


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
    ImprintBasicInfo["Imprint_Method"] = ""
    ImprintBasicInfo["Imprint_Color"] = ""
    ImprintBasicInfo["Imprint_Location"] = ""

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
                    ImprintBasicInfo["Imprint_Method"] = text.replace("Imprint Method","").strip()
                elif "Imprint Color" in text:
                    ImprintBasicInfo["Imprint_Color"] = text.replace("Imprint Color","").strip()
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
            ImprintBasicInfo["Imprint_Location"] = text.replace("Imprint Location","").strip()

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
                ImprintCharge['UQ1'] = ImprintQuantity
                ImprintCharge['UP1'] = ImprintPrice
                ImprintCharge['Upcharge_Details'] = ""
                if "Price Includes:" in block.get_text().strip():
                    index = block.get_text().strip().rfind("Price Includes:")
                    ImprintChargeDetail = block.get_text().strip()[index+len("Price Includes:"):].strip()
                    if "N/A" not in ImprintChargeDetail:
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
                ArtworkCharge['UQ1'] = ArtworkQuantity
                ArtworkCharge['UP1'] = ArtworkPrice
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
                        if "N/A" in rawtext:
                            pass
                        else:
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
                            # 此处在字符串尾部加上"\t"是为了防止excel把"5:"当成时间格式，而字典转化了
                            ProductionInformation["Rush_Time"] = str(begin)+":"+","+str(end)+":"+"\t"
                        else:
                            match1 = re.match(r'(\d+?) business days',rawtext)
                            if match1:
                                begin = match1.group(1)
                            else:
                                match2 = re.match(r'(\d+?) business day',rawtext)
                                if match2:
                                    begin = match2.group(1)
                            ProductionInformation["Rush_Time"] = str(begin)+":"+"\t"
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
                        if len(ShippingInfo) > 0:
                            if ShippingInfo[0] == ";":
                                ShippingInfo = ShippingInfo[1:].strip()
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
                    RushServiceCharge['Upcharge_Criteria_1'] = ""

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
                    RushServiceCharge['UQ1'] = RushQuantity
                    RushServiceCharge['UP1'] = RushPrice
                    if "Price Includes:" in dataFieldBlock.get_text().strip():
                        index = dataFieldBlock.get_text().strip().rfind("Price Includes:")
                        ArtworkChargeDetail = dataFieldBlock.get_text().strip()[index + len("Price Includes:"):].strip()
                        # 如果Detail中有N/A,那么设为空
                        if "N/A" in ArtworkChargeDetail:
                            ArtworkChargeDetail = ""
                        RushServiceCharge['Upcharge_Details'] = ArtworkChargeDetail

    return RushServiceCharge


"""这个函数是获取Safety and Compliance大块中的Comp_Cert字段"""
def getComp_Cert(bsObj):
    allData = bsObj.findAll("div", class_="attributesContainer")
    SafetyComplianceDiv = allData[4]
    Comp_Cert = ""

    # if "FDA" in SafetyComplianceDiv.prettify():
    #     Comp_Cert += "FDA,"
    # if "Food Grade"  in SafetyComplianceDiv.prettify():
    #     Comp_Cert += "Food Grade,"
    # if len(Comp_Cert) > 0:
    #     Comp_Cert = Comp_Cert[0:len(Comp_Cert)]
    if "Certifications and Compliance" in SafetyComplianceDiv.prettify():
        rawtexts = SafetyComplianceDiv.findAll("span",class_="strong addColon TxtLabel")
        for item in rawtexts:
            rawtext = item.get_text().strip()
            if "Certifications and Compliance" in rawtext:
                Comp_Cert = rawtext.replace("Certifications and Compliance","").strip()

    return Comp_Cert


'''最终写入csv文件中的时候，每个字段都要两边加上两个双引号，第二个双引号后面加上逗号，来保证不被逗号分隔错
如果列内容本身含有"，则用""表示 如某一列内容为c,"d",则csv格式为： a,b,"c,""d""",e
要将字段值中的双引号换成4引号
'''
def addQuot(rawstr):
    str1 = str(rawstr)
    str1 = str1.replace('"','""')
    str2 = '"'+str1+'"'+','
    return str2

def deleteDollar(str):
    str1 = str.replace("$","").strip()
    return str1

if __name__ == "__main__":
    url = "http://promomart.espwebsite.com/ProductDetails/?productId=4783582"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    html = requests.get(url, headers=headers).content
    bsObj = BeautifulSoup(html, 'html.parser')

    # rows = parser(Prodouct(url)).to_csv_row
    # for row in rows:
    #     print row

    # print "BasicInfomation",getBasicInfomation(bsObj)
    # print "Pricing",getPricing(bsObj)
    print "ProductDetail", getProductDetail(bsObj)
    # print "SampleCharge", getSampleCharge(bsObj)
    # print "ImprintInformation", getImprintInformation(bsObj)
    # print "ImprintMethodCharge", getImprintMethodCharge(bsObj)
    # print "Artwork_Proofs", getArtwork_Proofs(bsObj)
    # print "ProductionInformation", getProductionInformation(bsObj)
    # print "RushServiceCharge", getRushServiceCharge(bsObj)
    #
    # print addQuot("有没有引号和逗号")

