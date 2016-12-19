# -*- coding:utf-8-*-

from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import send_from_directory
import sys,os
from downloadUtils import getThreadPoolAndStartContentByKeyword80, getFirstThreadPoolAndEndContentByKeyword, \
    getThreadPoolFromProdIDList, writeCsvByThreadPool
from nextPage import get80PerPage, getProdIDList, get80NextPageContent
from browser import get_webservertime, openBrowser


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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

    # 当内存数据库存了超过10个页面时，就删除之前的页面（非此keyword的页面）
    if len(memorydb) > 10:
        for key in memorydb.keys():
            if key[0] != keyword:
                memorydb.pop(key)

    if request.method == 'POST':
        threadPool4WriteCsv = []
        newPackage = memorydb[(keyword, num)]
        # print len(newPackage['threadPool'])

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

        path = sys.path[0]
        filename_withoudir = keyword +'_'+str(num) +'.csv'
        filename_withoudir_str = filename_withoudir.encode('utf-8')
        filename = str(path) + '/static/' + filename_withoudir_str
        writeCsvByThreadPool(threadPool4WriteCsv, filename)

        return send_from_directory('static', filename_withoudir_str, as_attachment=True)
        #return "hello kitty"

    pagebean = None
    test = None

    if (keyword, num) in memorydb.keys():
        # test = memorydb[(keyword, 1)]
        pagebean = memorydb[(keyword, num)]
        return render_template('product.html', prod=prod, page=page,pagebean=pagebean)
    else:
        if num == 1:
            singleBean = getFirstThreadPoolAndEndContentByKeyword(keyword)
            # pagebean = singleBean
            memorydb[(keyword, 1)] = singleBean
            return render_template('product.html', prod=prod, page=page,pagebean=singleBean)
        else:
            if num > 1:
                if (keyword, 1) in memorydb.keys():
                    loopstartnum = num
                    while (keyword, loopstartnum) not in memorydb.keys():
                        loopstartnum -= 1
                    startContent = memorydb[(keyword, loopstartnum)]['endContent']
                    url =  "http://promomart.espwebsite.com/ProductResults/?SearchTerms=" + keyword
                    for i in range(num-loopstartnum):
                        startContent = get80NextPageContent(url, startContent)

                    idList = getProdIDList(startContent)
                    # print "获取idlist完毕" + time.strftime('%Y-%m-%d %H:%M:%S')
                    threadPool = getThreadPoolFromProdIDList(idList)
                    # print "下载线程池全部下载完毕" + time.strftime('%Y-%m-%d %H:%M:%S')

                    package = {}
                    package['threadPool'] = threadPool
                    package['endContent'] = startContent
                    memorydb[(keyword, num)] = package
                    # print "写入内存对象完毕" + time.strftime('%Y-%m-%d %H:%M:%S')
                    return render_template('product.html', prod=prod, page=page,pagebean=package)
                # 在memorydb被清空后，防止从第5页点击上一页到第四页
                else:
                    new_url = '/' + unicode(keyword) + "/1"
                    return redirect(new_url)

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

    timeflag = get_webservertime()
    if timeflag:
        openBrowser()
        app.run(debug=True)
