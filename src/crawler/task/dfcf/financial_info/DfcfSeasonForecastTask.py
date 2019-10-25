# coding=utf-8
import json
import math
import time

import arrow
import requests

from common.db.db_base import DBBase
from common.util.StringUtils import genRandomString
from common.util.sls_log_service import get_logger
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
业绩预告: http://data.eastmoney.com/bbsj/201906/yjyg.html

url_example: http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p=2&ps=30&js=var%20xsFnzmed={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^2019-09-30^)&rt=52288381
'''

base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p={pageNo}&ps={pageSize}&js=var%20{varName}={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^{enddate}^)&rt={rt}'
logger = get_logger()


class DfcfSeasonForecastTask(DfcfReportBaseTask):
    def __init__(self):
        super(DfcfSeasonForecastTask, self).__init__()
        self.base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token={token}&st=ndate&sr=-1&p={pageNo}&ps={pageSize}&js=var%20{varName}={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^{enddate}^)&rt={rt}'
        self.db_table = 'stock_dfcf_season_forecast'
        self.order_column = 'ndate'
        self.date_columns = ['enddate', 'ndate']

    def get_report_date(self):
        return self.get_season_end_date()