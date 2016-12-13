# -*- coding:utf-8-*-

from flask import Flask, render_template
from flask import request, redirect, url_for
from downloadUtils import getThreadPoolAndStartContentByKeyword80, getFirstThreadPoolAndEndContentByKeyword, \
    getThreadPoolFromProdIDList
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


@app.route('/<prod>/<page>')
def getTable(prod, page):
    pagebean = None
    test = None
    keyword = unicode(prod)
    num = int(page)
    if (keyword, num) in memorydb.keys():
        # test = memorydb[(keyword, 1)]
        pagebean = memorydb[(keyword, num)]
    else:
        if num == 1:
            singleBean = getFirstThreadPoolAndEndContentByKeyword(keyword)
            # pagebean = singleBean
            memorydb[(keyword, 1)] = singleBean
        else:
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

if __name__ == '__main__':
    app.run(debug=True)