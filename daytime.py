import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import requests
import json
from matplotlib.pyplot import MultipleLocator
import config


# print(time.strftime("%H", time.localtime()))

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

def showResult(slist):
    nums = np.zeros(24, np.int32)
    hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] #日期
    _i = 0
    for item in slist:
        _item = json.loads(item)
        _hour = int(_item['time'].split(" ")[1].split(':')[0])
        # print(_hour, type(_hour))
        nums[_hour]=int(nums[_hour])+1
    showImage(nums, hours)




def showImage(users,hours):
    plt.figure(num=1, figsize=(len(hours),10))
    plt.ylabel('count')
    plt.xticks(rotation=45, fontsize=10) 
    plt.xlabel("time", fontsize=10)
    plt.xlim(0,len(hours))
    plt.ylim(0,max(users)+500)
    y_major_locator=MultipleLocator(max(users)//10)
    x_major_locator=MultipleLocator(1)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
    plt.title(gstart+"~"+gend, fontsize=20)
    plt.plot(hours, users,  color='green', linewidth=3, label='count')
    plt.legend()
    plt.savefig("上课区间-"+gstart+"~"+gend+".png", bbox_inches='tight')
    # plt.show();

 
def getData(start, end):
    sql = "select time, event from events where business='优优小班' and event ='ClassstartAI' and date between '"+start+"' and '"+end+"' order by time"
    print(sql)
    data = {'format': 'json', 'q': sql}
    req_url = "https://"+url+"/api/sql/query?token="+token+"&project=production"
    req_header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    response = requests.post(req_url,data = data, headers = req_header)
    rst = response.text.split('\n')
    del rst[-1]
    print('num'+str(len(rst)))

    return rst

 


if __name__ == "__main__":
    _sts = int(time.time()*1000)
    user = getData(gstart, gend)
    showResult(user)
    print('dur',int(time.time()*1000) - _sts)
    
