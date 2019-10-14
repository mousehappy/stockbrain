# coding=utf-8
import json
import math
import time

import arrow
import requests

from common.util.StringUtils import genRandomString
from crawler.base.db_base.stock_db_base import logger
from crawler.task.BaseTask import BaseTask
import numpy as np
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
    "crawl_type": "DfcfConceptInfoDailyTask",
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


class DfcfConceptInfoDailyTask(BaseTask):
    def __init__(self):
        super(DfcfConceptInfoDailyTask, self).__init__()

    def close(self):
        super(DfcfConceptInfoDailyTask, self).close()

    def get_crawl_date(self):
        now_dt = arrow.now()
        hour = now_dt.hour
        if hour < 8:
            ts_date = now_dt.shift(days=-1).format('YYYYMMDD')
        elif hour > 15:
            ts_date = now_dt.format('YYYYMMDD')
        else:
            raise RuntimeError('Illegal crawl time: %s' % now_dt)
        sql = "select * from stock_trade_date where cal_date <= '%s' and is_open=1 order by cal_date desc limit 1;" % ts_date
        trade_dt = self.query(sql)
        if not trade_dt:
            raise RuntimeError('Failed to load trade date: %s' % ts_date)
        return trade_dt[0]['cal_date']

    def run(self, task_define):
        # Arrow.now().date()
        # start_dt = Arrow.fromdate(task_define['last_crawl_day'])  # .strftime('%Y%m%d')
        # end_dt = Arrow.fromdate(task_define['cur_dt'])
        # for r_dt in Arrow.range('day', start_dt, end_dt):
        logger.info('Start to crawl data of task: %s, dt: %s' % (self.__class__.__name__, self.dt))
        trade_dt = self.get_crawl_date()
        cur_ts = arrow.now().timestamp
        rand_int = np.random.randint(10, 100)
        url = base_url.replace('{randint}', str(rand_int)).replace('{ts}', str(cur_ts))
        logger.info('Formatted url: %s' % url)
        resp_json = requests.get(url).json()
        records = resp_json['data']['diff']
        logger.info('Task [%s], total crawl records: %s' % (self.__class__.__name__, len(records)))
        # print json.dumps(repoart_data)
        records = list(filter(lambda x: x['f2'] != '-', records))
        for record in records:
            for k, v in record.items():
                if v == '-':
                    record[k] = 0
            record['dt'] = trade_dt
        self.write_db('stock_dfcf_concept_daily_info', records)


if __name__ == '__main__':
    cit = DfcfConceptInfoDailyTask()
    cit.run({})