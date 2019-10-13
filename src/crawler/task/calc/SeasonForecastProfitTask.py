#-*- coding: UTF-8 -*-
import json

from crawler.task.BaseTask import BaseTask


class SeasonForecastProfitTask(BaseTask):
    def __init__(self):
        super(SeasonForecastProfitTask, self).__init__()

    def close(self):
        super(SeasonForecastProfitTask, self).close()

    def run(self, task_define):
        grow_list = self.get_last_season_revenue_grow_stock()
        if not grow_list:
            return
        grow_stock_list = [l['ts_code'] for l in grow_list]
        forecasted_list = self.get_no_forecast_stock(grow_stock_list)
        forecasted_stock_list = [l['ts_code'] for l in forecasted_list]
        # print json.dumps(forecasted_list)
        no_forecasted_list = [l for l in grow_list if l['ts_code'] not in forecasted_stock_list and l['trademarketcode'] in ('069001002003', '069001002002')]
        print len(no_forecasted_list)
        # market = set()
        # for l in no_forecasted_list:
        #     market.add(l['trademarketcode'])
        # print market

    def get_last_season_revenue_grow_stock(self):
        end_date = '2019-06-30'
        sql = "select * from stock_dfcf_season_report where reportdate='%s' and  ystz > '30' and yshz > '30';" % end_date
        revenue_grow_list = self.query(sql)
        return revenue_grow_list

    def get_no_forecast_stock(self, grow_list):
        end_date = '2019-09-30'
        sql = "select * from stock_dfcf_season_forecast where enddate=%s and ts_code in %s"
        forecasted_list = self.query(sql, end_date, grow_list)
        return forecasted_list

if __name__ == '__main__':
    t = SeasonForecastProfitTask()
    t.run({})