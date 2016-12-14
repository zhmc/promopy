# -*- coding:utf-8-*-

from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import send_from_directory

from downloadUtils import getThreadPoolAndStartContentByKeyword80, getFirstThreadPoolAndEndContentByKeyword, \
    getThreadPoolFromProdIDList, writeCsvByThreadPool
from nextPage import get80PerPage, getProdIDList, get80NextPageContent

app = Flask(__name__)

memorydb = {}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        new_url = '/'+unicode(keyword)+"/1"
        return redirect(new_url)
    return render_template('index.html')


@app.route('/<prod>/<page>', methods=['POST', 'GET'])
def getTable(prod, page):
    keyword = unicode(prod)
    num = int(page)

    if request.method == 'POST':
        threadPool4WriteCsv = []
        newPackage = memorydb[(keyword, num)]
        print len(newPackage['threadPool'])

        form = request.form
        # if newPackage:
        #     print "exsit memorydb[(keyword, num)]"

        # 对字典按照键来排序，生成的是一个元素为元组的列表
        sorted_form  = sorted(form.items(), key=lambda d: int(d[0]) )
        for key in sorted_form:
            i = int(key[0])
            # print i
            # print len(newPackage['threadPool'])
            # 这个地方i是从1到80的，然而在列表里面取值要从0到79
            threadPool4WriteCsv.append(newPackage['threadPool'][int(key[0])-1])

        writeCsvByThreadPool(threadPool4WriteCsv,'static/temp.csv')

        return send_from_directory('static', 'temp.csv', as_attachment=True)

    pagebean = None
    test = None

    if (keyword, num) in memorydb.keys():
        # test = memorydb[(keyword, 1)]
        pagebean = memorydb[(keyword, num)]
    else:
        if num == 1:
            singleBean = getFirstThreadPoolAndEndContentByKeyword(keyword)
            # pagebean = singleBean
            memorydb[(keyword, 1)] = singleBean
        else:
            if num > 1:
                loopstartnum = num
                while (keyword, loopstartnum) not in memorydb.keys():
                    loopstartnum -= 1
                startContent = memorydb[(keyword, loopstartnum)]['endContent']
                url =  "http://promomart.espwebsite.com/ProductResults/?SearchTerms=" + keyword
                for i in range(num-loopstartnum):
                    startContent = get80NextPageContent(url, startContent)

                idList = getProdIDList(startContent)
                threadPool = getThreadPoolFromProdIDList(idList)

                package = {}
                package['threadPool'] = threadPool
                package['endContent'] = startContent
                memorydb[(keyword, num)] = package

    pagebean = memorydb[(keyword, num)]
    return render_template('product.html', prod=prod, page=page,pagebean=pagebean)


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        str1 = ""
        form = request.form
        sorted_form  = sorted(form.items(), key=lambda d: int(d[0]) )

        for key in sorted_form:
            str1 += str(key[0])+"\n"
        return render_template('test1.html',str=str1)

    return render_template('product1.html')



if __name__ == '__main__':
    app.run(debug=True)