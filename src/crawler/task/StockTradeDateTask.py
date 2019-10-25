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
import listcompare

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
板块大盘: http://quote.eastmoney.com/center/boardlist.html#concept_board

url_example: http://37.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87&_=1569638458193
'''

base_url = 'http://{randint}.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87&_={ts}'


class StockTradeDateTask(BaseTask):
    def __init__(self):
        super(StockTradeDateTask, self).__init__()
        self.db_table = ''
        self.order_column = ''
        self.date_columns = []
        self.base_url = ''
        self.pageSize = 30

    def close(self):
        super(StockTradeDateTask, self).close()

    def get_crawl_date(self):
        now_dt = arrow.now()
        hour = now_dt.hour
        if hour < 8:
            ts_date = now_dt.shift(days=-1).format('YYYYMMDD')
        elif hour > 15:
            ts_date = now_dt.format('YYYYMMDD')
        else:
            raise RuntimeError('Illegal crawl time: %s' % now_dt)
        self.ts_client.query('trade_cal', start_date=ts_date, end_date=ts_date)

    def run(self, task_define):
        # Arrow.now().date()
        # start_dt = Arrow.fromdate(task_define['last_crawl_day'])  # .strftime('%Y%m%d')
        # end_dt = Arrow.fromdate(task_define['cur_dt'])
        # for r_dt in Arrow.range('day', start_dt, end_dt):
        logger.info('Start to crawl data of task: %s, dt: %s' % (self.__class__.__name__, self.dt))
        year = self.dt.year
        # year = 2019
        start_date = '%s0101' % year
        end_date = '%s0101' % (year + 1)
        tu_data = self.ts_client.query('trade_cal', start_date=start_date, end_date=end_date)
        self.write_db_with_df('stock_trade_date', tu_data)
        logger.info('Success to crawl task: %s, crawl size: %s' % (self.__class__.__name__, tu_data.__len__()))


if __name__ == '__main__':
    cit = StockTradeDateTask()
    cit.run({})