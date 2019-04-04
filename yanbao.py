# -*- coding=utf-8 -*-

# 中泰证券研报
# url0 = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=SRCC&stat=0&js=var%20zzsrYpDY={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=25"
# url1 = "&p={}&code=80000157&rt=51774703"
# 个股研报
url0 = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20sHbElhIt={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50"
url1 = "&p={}&mkt=0&stat=0&cmd=2&code=&rt=51774793"

import requests
import collections
import pandas as pd
import xlrd
import numpy as np
from  connmongo import MongoConn

class getreports():
    def __init__(self,page):
        self.page = page

    def parsepage(self):
        for i in range(1, self.page):
            murl = url1.format(i)
            jsondata = requests.get(url0 + murl)
            print(jsondata.text)
            yield eval(jsondata.text.split('=')[1])


if __name__ == '__main__':
    test = getreports(page=10)
    my_conn = MongoConn()
    finalrst = []
    keys = set()
    for dt in test.parsepage():
        rst = []
        for d in dt['data']:
            rst.append({d['secuName']:d['rate']})
            keys.add(d['secuName'])
        finalrst.extend(rst)
    final2 = dict.fromkeys(keys)
    for item in finalrst:
        mkey = list(item.keys())[0]
        mval = list(item.values())[0]
        if not final2.get(mkey):
            final2[mkey] = [mval]
        else:
            final2[mkey].append(mval)
    print(final2)
    final3 = dict.fromkeys(keys)
    for jk, jval in final2.items():
        final3[jk] = collections.Counter(jval)
    print(final3)
    final4 = pd.DataFrame.from_dict(final3)
    final5 = final4.transpose()
    final6 = final5.sort_index(by=["买入","增持"],ascending=[False,False])
    print(final6)
    final6.to_csv("个股评论.csv",encoding='utf_8_sig')





