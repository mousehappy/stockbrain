import json
from arrow import Arrow
from crawler.base.db_base.stock_db_base import StockDBBase
from crawler.base.task_generator.task_configuration import task_configs
from crawler.base.db_base.stock_db_base import logger


class TaskGenerator(StockDBBase):
    def __init__(self):
        super(TaskGenerator, self).__init__()
        self.now = Arrow.now()
        self.dt = Arrow.now().date()

    def run(self):
        sql = 'select ts_code, symbol, list_date from stock_list'
        stock_list = self.query(sql)
        logger.info("Start generate crawl task records!")
        self._generate_task_data(stock_list)
        logger.info("Start refresh task records and disable invalid tasks")
        self._refresh_crawl_tasks(stock_list)

    def _generate_task_data(self, stock_list):
        crawl_tasks = []
        for task_config in task_configs:
            crawl_type = task_config['name']
            init_days = task_config.get('init_days', 365)
            type = task_config.get('type', 1)
            task = None
            crawl_start_day = self.now.replace(days=-init_days).date()
            if type == 1:
                task = {
                    'ts_code': 'all',
                    'symbol': 'all',
                    'crawl_type': crawl_type,
                    'last_crawl_day': crawl_start_day,
                    'status': 1
                }
            elif type == 2:
                for stock in stock_list:
                    list_date = stock['list_date']
                    crawl_start_day = list_date if list_date > crawl_start_day else crawl_start_day
                    task = {
                        'ts_code': stock['ts_code'],
                        'symbol': stock['symbol'],
                        'crawl_type': crawl_type,
                        'last_crawl_day': crawl_start_day,
                        'status': 1
                    }
            if task:
                crawl_tasks.append(task)
        self.write_db('stock_task_scheduler', crawl_tasks, insert_ignore=True)

    def _refresh_crawl_tasks(self, stock_list):
        # stock_symbols = ','.join([s['symbol'] for s in stock_list])
        # crawl_types = ','.join(['\'%s\'' % t['name'] for t in task_configs])
        stock_symbols = [s['ts_code'] for s in stock_list]
        stock_symbols.append('all')
        crawl_types = [t['name'] for t in task_configs]
        update_sql = 'update stock_task_scheduler set dt=%s, status=1 where ts_code in %s and crawl_type in %s'
        update_cnt = self.execute_rowcount(update_sql, self.dt, stock_symbols, crawl_types)
        logger.info("Update crawl tasks: %s" % update_cnt)
        delete_sql = 'update stock_task_scheduler set status=0 where dt!=%s'
        delete_cnt = self.execute_rowcount(delete_sql, self.dt)
        logger.info("Delete invalid tasks: %s" % delete_cnt)


if __name__ == '__main__':
    t = TaskGenerator()
    t.run()

