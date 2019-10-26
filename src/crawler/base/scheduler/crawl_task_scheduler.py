from common.util.sls_log_service import get_logger
from crawler.base.db_base.stock_db_base import StockDBBase
from multiprocessing.pool import Pool
from multiprocessing import Queue
from crawler.worker.crawler.stock_crawl_worker import CrawlerWorker

MULTI_PROCESS_NO = 2
PROCESS_EXIT_TIMEOUT = 120

logger = get_logger()

class CrawlTaskScheduler(StockDBBase):
    def __init__(self):
        super(CrawlTaskScheduler, self).__init__()
        self.worker_pools = []
        self.task_queue = Queue()
        self.result_queue = Queue()
        for i in xrange(MULTI_PROCESS_NO):
            p = CrawlerWorker(i+1, self.task_queue, self.result_queue)
            p.start()
            self.worker_pools.append(p)

    def start_schedule(self):
        t_sql = 'select * from stock_task_scheduler where status=1 and last_crawl_day<%s'
        c_tasks = self.query(t_sql, self.dt)
        logger.info("Need execute task: %s" % len(c_tasks))
        for task in c_tasks:
            task['cur_dt'] = self.dt
            self.task_queue.put(task)

    def stop(self):
        for p in self.worker_pools:
            # p.stop()
            # p.join(timeout=PROCESS_EXIT_TIMEOUT)
            p.join()

    def is_finish(self):
        return self.task_queue.empty()

    def run(self):
        self.start_schedule()