# -*- coding:utf-8-*-

from flask import Flask, render_template
from flask import request, redirect, url_for
from downloadUtils import getThreadPoolAndStartContentByKeyword80

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
    if (prod, page) in memorydb.keys():
        pagebean = memorydb[(prod, page)]
    else:
        pass
    return render_template('product.html', prod=prod, page=page)

if __name__ == '__main__':
    app.run(debug=True)