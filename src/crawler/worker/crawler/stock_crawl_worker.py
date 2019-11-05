import copy
import multiprocessing
import traceback
from Queue import Empty
from multiprocessing import Process
from common.util.sls_log_service import get_logger
from crawler.base.db_base.stock_db_base import StockDBBase
import importlib

from crawler.worker.crawler.TaskFactory import TaskFactory

DEFAULT_TASK_GET_TIMEOUT = 10

logger = get_logger()


class CrawlerWorker(StockDBBase, Process):
    def __init__(self, p_no, task_queue=multiprocessing.Queue(), result_queue=multiprocessing.Queue()):
        StockDBBase.__init__(self)
        Process.__init__(self)
        self.is_running = True
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.p_no = p_no

    def stop(self):
        self.is_running = False

    def start_crawl_task(self, symbol, crawl_type):
        task_update_sql = 'update stock_task_scheduler set crawl_status="running", crawl_start=now() ' \
                          'where symbol=%s and crawl_type=%s'
        task_cnt = self.execute_rowcount(task_update_sql, symbol, crawl_type)
        if task_cnt:
            logger.info('Start execute crawl task, crawl type: %s, symbol: %s' % (crawl_type, symbol))
        else:
            logger.info('Failed to update crawl task to start, crawl type: %s, symbol: %s' % (crawl_type, symbol))

    def finish_crawl_task(self, symbol, crawl_type, dt):
        task_update_sql = 'update stock_task_scheduler set crawl_status="finish", crawl_end=now(), last_crawl_day=%s ' \
                          'where symbol=%s and crawl_type=%s'
        task_cnt = self.execute_rowcount(task_update_sql, dt, symbol, crawl_type)
        if task_cnt:
            logger.info('Finish execute crawl task, crawl type: %s, symbol: %s' % (crawl_type, symbol))
        else:
            logger.info('Failed to update crawl task to finish, crawl type: %s, symbol: %s' % (crawl_type, symbol))

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

    def run(self):
        while self.is_running:
            try:
                task_define = self.task_queue.get(timeout=DEFAULT_TASK_GET_TIMEOUT)
                if not task_define:
                    break
            except Empty:
                logger.info("Crawl work process exit! Process no: %s" % self.p_no)
                break
            for i in xrange(5):
                try:
                    symbol = task_define['symbol']
                    crawl_type = task_define['crawl_type']
                    task = TaskFactory.init_task_instance(crawl_type)
                    # task_name = 'crawler.task.%s' % crawl_type
                    # m = importlib.import_module(task_name)
                    # t_clz = getattr(m, crawl_type)
                    # task = t_clz()
                    self.start_crawl_task(symbol, crawl_type)
                    result = task.run(task_define)
                    task.close()
                    self.finish_crawl_task(symbol, crawl_type, self.crawl_dt)
                    result_dict = copy.deepcopy(task_define)
                    result_dict['result'] = result
                    self.result_queue.put(result_dict)
                    break
                except Exception as e:
                    logger.error("Crawl worker-%s with exception, failed count: %s, exception detail: %s" %
                                 (self.p_no, i, traceback.format_exc()))


if __name__ == '__main__':
    try:
        c = CrawlerWorker()
        c.run()
    except Exception as e:
        logger.error(traceback.format_exc())
