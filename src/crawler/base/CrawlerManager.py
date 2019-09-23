import time

from crawler.base.db_base.stock_db_base import logger
from crawler.base.scheduler.crawl_task_scheduler import CrawlTaskScheduler
from crawler.base.stock_cmdb.StockCmdb import StockCMDB
from crawler.base.task_generator.task_generator import TaskGenerator
import pandas as pd
import numpy as np


class CrawlerManager(StockCMDB):
    def __init__(self):
        super(CrawlerManager, self).__init__()
        self.stock_cmdb = StockCMDB()
        self.task_gen = TaskGenerator()
        self.task_scheduler = CrawlTaskScheduler()

    def run(self):
        self.stock_cmdb.run()
        self.task_gen.run()
        self.task_scheduler.run()
        # c_cnt = 1
        # while self.task_scheduler.is_finish():
        #     logger.info('Task not finish yet! Count: %s' % c_cnt)
        #     c_cnt += 1
        #     time.sleep(10)
        self.task_scheduler.stop()


if __name__ == '__main__':
    # tushare_api = ts.pro_api(tu_token)
    # df = tushare_api.trade_cal(start_date='20150101', end_date='20250101')
    # print df.size
    # for row in df[:100]:
    #     print row
    # print np.random.rand(2, 3, 4)
    # N=20
    #
    # df = pd.DataFrame({
    #    'A': pd.date_range(start='2016-01-01',periods=N,freq='D'),
    #    'x': np.linspace(0,stop=N-1,num=N),
    #    'y': np.random.rand(N),
    #    'C': np.random.choice(['Low','Medium','High'],N).tolist(),
    #    'D': np.random.normal(100, 10, size=(N)).tolist()
    # })
    #
    # np.random.normal()
    cm = CrawlerManager()
    cm.run()

