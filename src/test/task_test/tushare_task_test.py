# -*- coding: UTF-8 -*-
import importlib
import unittest

from crawler.worker.crawler.TaskFactory import TaskFactory


class TaskTestBase(unittest.TestCase):
    def init_task(self, task_define):
        # symbol = task_define['symbol']
        crawl_type = task_define['crawl_type']
        # task_name = 'crawler.task.%s' % crawl_type
        # m = importlib.import_module(task_name)
        # t_clz = getattr(m, crawl_type)
        # task = t_clz()
        # self.start_crawl_task(symbol, crawl_type)
        task = TaskFactory.init_task_instance(crawl_type, base_path='../../crawler/task')
        result = task.run(task_define)
        task.close()

    def test_hk_hold(self):
        task_define = {
            "symbol": "000001",
            "ts_code": "000001.SZ",
            "last_crawl_day": "2019-09-05",
            "crawl_type": "DailyTradeInfoTask",
            "cur_dt": "2019-09-06"
        }
        self.init_task(task_define)
        self.assertEqual('foo'.upper(), 'FOO')
