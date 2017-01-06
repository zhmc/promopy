import urllib2
import time
import webbrowser

def get_webservertime():
    response = urllib2.urlopen('https://www.baidu.com/')

    ts = response.headers['date']

    # print ts
    # print ts[5:25]
    #
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")

    # 1481894183 now 2016-12-16-21-16
    # 1482723101  2016-12-26-11-32
    # add 8 hours for beijing time
    timestamp = time.mktime(ltime)  + 8*60*60
    # print int(timestamp)

    # day_left = ((1482723101 + 3 *24* 60 *60) - timestamp) / (24* 60 *60)
    # print day_left
    
    # print time.time()

    # time a week later
    if timestamp > 1482723101 + 3 *24* 60 *60:
        return False
    else:
        return True




def openBrowser():

    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)

if __name__ == '__main__':
    print get_webservertime()