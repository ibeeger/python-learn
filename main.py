import matplotlib.pyplot as plt
import numpy as numpy
import sys
import requests
import json
import time
import pandas as pd
from matplotlib.pyplot import MultipleLocator
import config
import taskthread


argv = sys.argv

print(argv[1])

_os = ""

token = config.getToken()
url = config.getUrl()

if(len(argv)>2):
    _os="$os='"+argv[2]+"' and"

gstart = argv[1] #'2020-6-3'
gend =  time.strftime("%Y-%m-%d", time.localtime())

width = 0

def showResult(slist, helplist):
    nums = [] #人数
    dates = [] #日期
    hnums = [] #求助人数
    _i = 0
    for item in slist:
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
    if(len(hnums)<len(nums)):
        hnums.append(0)
    showImage(nums, dates, hnums)





def showImage(xs,ys,hs):
    plt.figure(num=1, figsize=(len(xs)//5,10))
    plt.ylabel('count', color='red')
    plt.xticks(rotation=45, fontsize=10) 
    plt.xlabel("date", fontsize=10)
    plt.xlim(0,len(ys))
    plt.ylim(0,max(xs)+100)
    y_major_locator=MultipleLocator(200)
    x_major_locator=MultipleLocator(len(xs)//30)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
    plt.title(gstart+"~"+gend, fontsize=20)
    plt.plot(ys,xs, color='green', linewidth=3, label='total')
    plt.plot(ys,hs, color='red', linestyle='--', linewidth=2, label='support')
        
    plt.legend()
    plt.savefig("上课人数-"+gstart+"~"+gend+".png", bbox_inches='tight')
    # plt.show();


def getHelpData(start, end):
    sql = "select count(button_name) as num, date from (select distinct(stu_id), button_name, business, date from events where "+_os+" date between '"+start+"' and '"+end+"') tmp where button_name='求助' and business='优优小班'  group by date order by date;"
    print(sql)
    data = {'format': 'json', 'q': sql}
    req_url = "https://"+url+"/api/sql/query?token="+token+"&project=production"
    req_header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    response = requests.post(req_url,data = data, headers = req_header)
    rst = response.text.split('\n')
    del rst[-1]
    print('help'+str(len(rst)))
    return rst


 
def getData(start, end):
    sql = "select count(distinct(stu_id)) as num, date from events where "+_os+" date between '"+start+"' and '"+end+"' and business='优优小班'   group by date order by date"
    print(sql)
    data = {'format': 'json', 'q': sql}
    req_url = "https://"+url+"/api/sql/query?token="+token+"&project=production"
    req_header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    response = requests.post(req_url,data = data, headers = req_header)
    rst = response.text.split('\n')
    del rst[-1]
    print('user'+str(len(rst)))

    return rst


def getUserTask(arg):
    return getData(arg[0], arg[1])

def getHelpTask(arg):
    return getHelpData(arg[0], arg[1])



def main():
    usertask = taskthread.TaskThread(getUserTask, args=[gstart, gend])
    helptask = taskthread.TaskThread(getHelpTask, args=[gstart, gend])
    tasklist = [usertask,helptask]
    usertask.start()
    helptask.start()

    resultlist = []
    for task in tasklist:
        task.join()
        resultlist.append(task.getresult())

    showResult(resultlist[0], resultlist[1])




if __name__ == "__main__":
    _sts = int(time.time()*1000)
    # user = getData(gstart, gend)
    # helplist = getHelpData(gstart, gend)
    # showResult(user, helplist)
    main()
    print('dur',int(time.time()*1000) - _sts)
    
