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
            "crawl_type": "DailyHkHoldTask",
            "cur_dt": "2019-09-06"
        }
        self.init_task(task_define)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_DfcfConceptInfoDailyTask(self):
        task_define = {
            "symbol": "000001",
            "ts_code": "000001.SZ",
            "last_crawl_day": "2019-09-05",
            "crawl_type": "DfcfConceptInfoDailyTask",
            "cur_dt": "2019-10-10"
        }
        self.init_task(task_define)
        self.assertEqual('foo'.upper(), 'FOO')


    def test_dfct_season_forecast(self):
        task_define = {
            "symbol": "000001",
            "ts_code": "000001.SZ",
            "last_crawl_day": "2019-09-05",
            "crawl_type": "DfcfSeasonForecastTask",
            "cur_dt": "2019-09-06"
        }
        self.init_task(task_define)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_dfct_season_report(self):
        task_define = {
            "symbol": "000001",
            "ts_code": "000001.SZ",
            "last_crawl_day": "2019-09-05",
            "crawl_type": "DfcfSeasonReportTask",
            "cur_dt": "2019-09-01"
        }
        self.init_task(task_define)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_dfct_season_report_appointment(self):
        task_define = {
            "symbol": "000001",
            "ts_code": "000001.SZ",
            "last_crawl_day": "2019-09-05",
            "crawl_type": "DfcfSeasonReportAppointmentTask",
            "cur_dt": "2019-09-01"
        }
        self.init_task(task_define)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_batch_dfct_season_report(self):
        task_define = {
            "symbol": "000001",
            "ts_code": "000001.SZ",
            "last_crawl_day": "2019-09-05",
            "crawl_type": "DfcfSeasonReportTask",
            "cur_dt": "2019-04-01"
        }
        dt_list = ['2016-01-01', '2016-04-01', '2016-07-01', '2016-10-01',
                   '2017-01-01', '2017-04-01', '2017-07-01', '2017-10-01',
                   '2018-01-01', '2018-04-01', '2018-07-01', '2018-10-01',
                   '2019-01-01', '2019-04-01']
        for dt in dt_list:
            task_define['cur_dt'] = dt
            self.init_task(task_define)