
import re
import matplotlib.pyplot as plt
import numpy as numpy
import sys
import requests
import json
import time
import os
import pandas as pd
from matplotlib.pyplot import MultipleLocator



rst = { "cpu": [], "cputotal": [], "memory": [], "memorytotal": [], "ts":[], "total_memory":0, "date": '' }


def getData():
    try:
        url = sys.argv[1]
        res = requests.get(url)
        _name = "android"
        if "iPad" in url :
            _name = "ipad"
        elif "iPhone" in url:
            _name = "iphone"
        return {"name": _name+"_"+url.split('_')[1], "line": res.text}
    except:
        print('日志地址为空')



def init(_name, line):
    rlist = line.split('\n')
    for index,item in enumerate(rlist):
        if index == 0:
            rst["total_memory"] = float(getTotalMemory(item.split("DEF:")[1].split(',')))
        if "PREF" in item:
            _sinfo = item.split('PREF:')[1].split(',')
            rst["ts"].append(item.split('|')[0].split('_')[1])
            rst['date'] = item.split('|')[0].split('_')[0]
            _rst = formatStr(_sinfo)
    showImage(rst['cpu'], rst['memory'], rst['cputotal'], rst['memorytotal'], rst["ts"], _name, rst['date'])


def getTotalMemory(_str):
    _memory = 0
    for item in _str:
        print('--',item)
        if item.split('=')[0].strip() == 'memory':
            if "MB" in item:
                _memory = (re.sub(r'MB', '', item.split('=')[1].strip()))
            else:
                _memory = float(re.sub(r'GB|G', '', item.split('=')[1].strip()))*1024
    return _memory


def showImage(cpu,memory, cputotal, memorytotal,ts,_name, date):
    plt.figure(num=1, figsize=(len(cpu)//10,20))
    plt.ylabel('percent', color='red')
    plt.xticks(rotation=45, fontsize=10) 
    plt.xlabel("time", fontsize=10)
    plt.xlim(0,len(memory))
    plt.ylim(0,100)
    y_major_locator=MultipleLocator(5)
    x_major_locator=MultipleLocator(len(cpu)//50)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1)
    plt.title(date+' cup and memory', fontsize=20)

    plt.grid(axis="both", linestyle=":", color="#cccccc")

    plt.plot(ts,cpu, color='green', linewidth=2, label='cpu')
    plt.plot(ts,cputotal, color='green',  linestyle='--',  linewidth=3, label='cputotal')
    
    plt.plot(ts,memory, color='red', linewidth=2, label='memory')
    plt.plot(ts,memorytotal, color='red', linestyle='--', linewidth=3, label='memorytotal')

    plt.legend(loc='upper left')
    plt.savefig(_name+".png", bbox_inches='tight')
    # plt.show();


def formatStr(_str):
    for item in _str:
        if item.split('=')[0] == 'cpu_app':
            _c = float(re.sub(r'%|Mb', '', item.split('=')[1]))
            rst['cpu'].append(_c)
        if item.split('=')[0] == 'cpu_total':
            _ct = float(re.sub(r'%|Mb', '', item.split('=')[1]))
            rst['cputotal'].append(_ct)
        if item.split('=')[0] == 'memory_app':
            _m = float(re.sub(r'%|Mb', '', item.split('=')[1]))
            rst['memory'].append(_m*100/rst["total_memory"])
        if item.split('=')[0] == 'memory_total':
            _mt = float(re.sub(r'%|Mb', '', item.split('=')[1]))
            rst['memorytotal'].append(_mt*100/rst["total_memory"])
    return rst

if __name__ == "__main__":
    obj = getData()
    init(obj['name'], obj['line'])