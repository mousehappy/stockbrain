# -*- coding: UTF-8 -*-
import json

import requests
import arrow
import random,string

header = {
    'GET': '/recommend/pofriends.json?type=1&code=SZ002231&start=0&count=14&_=1568463240615 HTTP/1.1',
    'Host': 'xueqiu.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'none',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': '_ga=GA1.2.1813339536.1543766326; device_id=de560128f0d426bd09fa9523094584fe; aliyungf_tc=AQAAALH4XQPFXQIA5c3Ac26qHpJ0z/8V; acw_tc=2760828315678235651652095e645fc17e78d91ee2f9c47a6a8b99facf1933; xq_a_token=75661393f1556aa7f900df4dc91059df49b83145; xq_r_token=29fe5e93ec0b24974bdd382ffb61d026d8350d7d; u=681567823566024; Hm_lvt_1db88642e346389874251b5a1eded6e3=1567823577,1568463026; s=by12ep725j; __utma=1.1813339536.1543766326.1568463147.1568463147.1; __utmc=1; __utmz=1.1568463147.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=1.3.10.1568463147; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1568463241'
}

temp_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st={sortType}&sr={sortRule}&p={page}&ps={pageSize}&js=var {jsname}={pages:(tp),data: (x),font:(font)}{param}'
url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p={pageNo}&ps={pageSize}&js=var%20xsFnzmed={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^{enddate}^)&rt=52288381'

base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p={pageNo}&ps={pageSize}&js=var%20{varName}={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^{enddate}^)&rt={rt}'
# parseInt(new Date().getTime()) / 30000


def genRandomString(slen=8):
    return ''.join(random.sample(string.ascii_letters, slen))


def get_season_forecast(enddate):
    pageNo = 1
    pageSize = 2
    rt = int(arrow.now().timestamp / 30)
    varName = genRandomString()
    cur_url = base_url.replace('{pageNo}', str(pageNo)).replace('{pageSize}', str(pageSize)).replace(
        '{rt}', str(rt)).replace('{enddate}', enddate).replace('{varName}', varName)
    # print cur_url
    resp = requests.request('GET', cur_url)
    data = resp.content
    data = data.split(varName + '=')[1]
    data = data.replace('data:', '"data":').replace('pages:', '"pages":').replace('font:', '"font":')
    print data
    # json_data = json.loads(data)
    # print json_data


if __name__ == '__main__':
    # url = 'https://xueqiu.com/recommend/pofriends.json?type=1&code=SZ002231&start=0&count=14&_=1568463240615'
    # url = 'https://xueqiu.com/recommend/pofriends.json?type=1&code=SZ002115&start=0&count=14&_=1568463240615'
    # resp = requests.request('GET', url)
    # print resp.content
    get_season_forecast('2019-09-30')
