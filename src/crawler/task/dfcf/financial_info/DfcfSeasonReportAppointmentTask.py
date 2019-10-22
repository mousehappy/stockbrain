# coding=utf-8
import json
import math
import time

import arrow
import requests

from common.db.db_base import DBBase
from common.util.StringUtils import genRandomString
from crawler.base.db_base.stock_db_base import logger
from crawler.task.BaseTask import BaseTask
from arrow import Arrow

from crawler.task.dfcf.financial_info.DfcfReportBaseTask import DfcfReportBaseTask

'''
{
    "data_start_day": "2019-09-01",
    "status": 1,
    "crawl_end": "2019-09-01",
    "data_end_day": "2019-09-01",
    "gmt_create": "2019-09-07 13:54:35",
    "symbol": "000001",
    "ts_code": "000001.SZ",
    "gmt_modify": "2019-09-07 14:01:51",
    "last_crawl_day": "2018-01-15",
    "crawl_type": "BasicTradeInfo",
    "dt": "2019-09-07",
    "crawl_start": "2019-09-01 12:00:00",
    "crawl_status": "waiting",
    "cur_dt": "2019-09-08"
}
'''
API_NAME = 'dfcf_season_forecast'

'''
预约披露时间: http://data.eastmoney.com/bbsj/201909/yysj.html

url_example: http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=YJBB21_YYPL&token=70f12f2f4f091e459a279469fe49eca5&st=frdate&sr=1&p=1&ps=200&js={"pages":(tp),"data":%20(x),"font":(font)}&filter=(securitytypecode=%27058001001%27)(reportdate=^2019-09-30^)&rt=52391859
'''

# base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p={pageNo}&ps={pageSize}&js=var%20{varName}={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^{enddate}^)&rt={rt}'
base_url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=YJBB21_YYPL&token=70f12f2f4f091e459a279469fe49eca5&st=frdate&sr=1&p={pageNo}&ps={pageSize}&js={"pages":(tp),"data":%20(x),"font":(font)}&filter=(securitytypecode=%27058001001%27)(reportdate=^{enddate}^)&rt={rt}'


class DfcfSeasonReportAppointmentTask(DfcfReportBaseTask):
    def __init__(self):
        global base_url
        super(DfcfSeasonReportAppointmentTask, self).__init__()
        self.base_url = base_url
        self.db_table = 'stock_dfcf_season_report_appointment'
        self.order_column = ''
        self.date_columns = []
        self.pageSize = 100

    def continue_crawl(self, batch_record, latest_record, date_columns=[]):
        return True

    def get_report_date(self):
        return self.get_season_end_date()

    def get_report_data(self, pageNo, enddate):
        pageSize = self.pageSize
        rt = int(arrow.now().timestamp / 30)
        cur_url = self.base_url.replace('{token}', self.token).replace('{pageNo}', str(pageNo)).replace('{pageSize}', str(pageSize)).replace(
            '{rt}', str(rt)).replace('{enddate}', enddate)
        # print cur_url
        resp = requests.request('GET', cur_url)
        data = resp.content
        # data = data.replace('data:', '"data":').replace('pages:', '"pages":').replace('font:', '"font":')
        formatted_data = json.loads(data)
        return formatted_data

    '''
    "frdate": "2019-10-22T00:00:00",
    "fcdate": "-",
    "scdate": "-",
    "tcdate": "-",
    '''
    def special_process_record(self, record={}):
        keys = ['tcdate', 'scdate', 'fcdate', 'frdate']
        for key in keys:
            dt = record.get(key, None)
            if not dt:
                record['finaldate'] = dt
                break

    def get_latest_record(self, table, order_column):
        return None


