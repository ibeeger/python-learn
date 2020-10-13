import matplotlib.pyplot as plt
import numpy as numpy
import sys
import requests
import json
import time
import pandas as pd
from matplotlib.pyplot import MultipleLocator


# x = np.linspace(-1,1,50)
# y = 2*x+1
# plt.figure(num=4, figsize=(4,3))
# plt.plot(x,y, color='red', linewidth=4)
# plt.show()

argv = sys.argv

print(argv[1])

_os = ""

if(len(argv)>2):
    _os="$os='"+argv[2]+"' and"

gstart = argv[1] #'2020-6-3'
gend =  time.strftime("%Y-%m-%d", time.localtime())

width = 0

def showResult(slist, helplist):
    nums = []
    dates = []
    hnums = []
    _i = 0
    for index,item in enumerate(slist):
        _json = json.loads(item)
        nums.append(_json['num'])
        dates.append(_json['date'])
        if(_i<len(helplist)):
            _hjson = json.loads(helplist[_i])
            if _hjson['date'] == _json['date']:
                hnums.append(_hjson['num'])
                _i=_i+1
            else:
                hnums.append(0)
    

    showImage(nums, dates, hnums)





def showImage(xs,ys,hs):
    plt.figure(num=1, figsize=(len(xs)//5,10))
    plt.ylabel('count', color='red')
    plt.xticks(rotation=45, fontsize=10) 
    plt.xlabel("date", fontsize=10)
    y_major_locator=MultipleLocator(500)
    x_major_locator=MultipleLocator(len(xs)//35)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
    plt.title(gstart+"~"+gend, fontsize=20)

    x =list(range(len(xs)))
    plt.bar(x, xs, width=4, label='user', tick_label=ys, fc = 'y')
    plt.legend()
    plt.savefig("bar人数-"+gstart+"~"+gend+".png")
    # plt.show();




def getHelpData(start, end):
    sql = "select count(button_name) as num, date from (select distinct(stu_id), button_name, date from events where "+_os+" date between '"+start+"' and '"+end+"') tmp where button_name='求助'  group by date order by date;"
    print(sql)
    data = {'format': 'json', 'q': sql}
    req_url = "https://banmatianxia.cloud.sensorsdata.cn/api/sql/query?token=29fbcd3f0939482de2b17746bde3d59155d6a2c5859cfb46f69e411c84412b69&project=production"
    req_header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    response = requests.post(req_url,data = data, headers = req_header)
    rst = response.text.split('\n')
    del rst[-1]
    width = len(rst)
    print('help')
    return rst


 
def getData(start, end):
    sql = "select count(distinct(stu_id)) as num, date from events where "+_os+" date between '"+start+"' and '"+end+"'  group by date order by date"
    print(sql)
    data = {'format': 'json', 'q': sql}
    req_url = "https://banmatianxia.cloud.sensorsdata.cn/api/sql/query?token=29fbcd3f0939482de2b17746bde3d59155d6a2c5859cfb46f69e411c84412b69&project=production"
    req_header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    response = requests.post(req_url,data = data, headers = req_header)
    rst = response.text.split('\n')
    del rst[-1]
    width = len(rst)
    print('user')
    return rst



if __name__ == "__main__":
    user = getData(gstart, gend)
    helplist = getHelpData(gstart, gend)
    showResult(user, helplist)
