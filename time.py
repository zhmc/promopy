import urllib2
import time
import os
def get_webservertime():
    response = urllib2.urlopen('https://www.sogou.com/')
    
    ts = response.headers['date']
    
    print ts
    print ts[5:25]
    #
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")

    # 1481894183 now 2016-12-16-21-16
    # add 8 hours for beijing time
    timestamp = time.mktime(ltime)  + 8*60*60
    print int(timestamp)
    
    # print time.time()
    # if timestamp > 1481894183:
    #     print "yes"
    # else:
    #     print "no"

    # time a week later
    if timestamp > 1481894183 + 8 *24* 60 *60:
        print "yes"
    else:
        print "no"

    leftday = (1481894183 + 8 *24 * 60 *60 - timestamp)/(60 *60*24)
    print "leftday:", leftday

    
get_webservertime()


import sys
import webbrowser


# url = 'http://www.baidu.com'
# webbrowser.open(url)
# print webbrowser.get()

keyword = u'cat'
num = 1

path = sys.path[0]
filename_withoudir = keyword +'_'+str(num) +'.csv'
filename = str(path) + '/static/' + filename_withoudir.encode('ascii')

print filename_withoudir, filename