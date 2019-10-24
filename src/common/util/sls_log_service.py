# -*- coding: utf-8 -*-
import logging
import logging.config
import socket
import time
import os
from logging.handlers import TimedRotatingFileHandler
from threading import Lock
from aliyun.log import QueuedLogHandler


file_path = os.path.abspath(__file__)
# print file_path
src_path = file_path.split('/')
log_path = '/'.join(src_path[:-3]) + '/resource/logs/stock_brain.log'
# print log_path
# print log_path

# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.INFO)
# formatter = logging.Formatter('[%(asctime)s] [%(processName)s] [%(process)d] [%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
# # file_handler = TimedRotatingFileHandler('/Users/wjq/work/stockbrain/src/resource/logs/stock_brain.log', when='H', backupCount=30)
# file_handler = TimedRotatingFileHandler(log_path, when='H', backupCount=30)
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)


class SlsLogService(object):
    '''
    阿里云日志服务
    https://aliyun-log-python-sdk.readthedocs.io/README_CN.html#id4
    install:
        pip install -U aliyun-log-python-sdk
    usage:
        from sls_log_service import get_logger
        logger = get_logger("uuid")
        logger.info("test sls log")
    '''
    def __init__(
            self,
            action_uuid,
            console_print=False,
            endpoint='cn-hangzhou.log.aliyuncs.com',
            access_id='LTAI4vHYl1tgSbKJ',
            access_key='1o9vNeR6RqyulO6LWYUxK04ECIo9n9',
            project='shaozhe-private',
            logstore='stockbrain_log'):
        super(SlsLogService, self).__init__()
        self.endpoint = endpoint
        self.access_id = access_id
        self.access_key = access_key
        self.project = project
        self.logstore = logstore
        self.hostname = socket.gethostname()
        self.action_uuid = action_uuid
        self.logger = self.write_log()
        self.total_step = 100.0
        self.current_step = 0.0
        self.console_print=console_print
        self.local_logs = []
        self.log_idx_lock = Lock()
        self.log_idx = 0

    def write_log(self):

        # 配置
        conf = {'version': 1,
                'formatters': {'rawformatter': {'class': 'logging.Formatter',
                                                'format': '%(message)s'},
                               'fileformatter': {'class': 'logging.Formatter',
                                                 'format': '[%(asctime)s] [%(processName)s] [%(process)d] [%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s'}
                               },
                'handlers': {'sls_handler': {'()':'aliyun.log.QueuedLogHandler',
                                             'level': 'INFO',
                                             'formatter': 'fileformatter',

                                             # custom args:
                                             'end_point': self.endpoint,
                                             'access_key_id': self.access_id,
                                             'access_key': self.access_key,
                                             'project': self.project,
                                             'log_store': self.logstore,
                                             # 'fields': ['record_name', 'file_path', 'thread_id', 'thread_name',
                                             #            'process_id', 'process_name', 'level', 'func_name',
                                             #            'module', 'line_no'],
                                             'extract_kv': False,
                                             'extract_kv_drop_message': False,
                                             'buildin_fields_prefix': 'sys_'
                                             },
                             'file_handler': {'class': 'logging.handlers.TimedRotatingFileHandler',
                                              'level': 'INFO',
                                              'formatter': 'fileformatter',
                                              'filename': log_path,
                                              'when': 'D',
                                              'backupCount': 30
                                              },
                             'console_handler': {'class': 'logging.StreamHandler',
                                              'level': 'INFO',
                                              'formatter': 'fileformatter',
                                              }
                             },
                'loggers': {'sls': {'handlers': ['sls_handler', 'file_handler', 'console_handler'],
                                    'level': 'INFO',
                                    'propagate': False
                                    }
                            }
                }
        logging.config.dictConfig(conf)

        # 使用
        logger = logging.getLogger('sls')
        return logger
        # logger.info("Hello world")

    def build_msg(self, message, level, step, is_print=False):
        if not isinstance(message, str):
            message = str(message)
        self.log_idx_lock.acquire()
        try:
            time_str = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            local_log = "[%s] Level:[%s], step:[%s], message:[%s]" % (time_str, level, step, message)
            self.local_logs.append(local_log)
            if self.console_print or is_print:
                print(local_log)
            msg = 'begin_ts=\"%s\" host_name=%s level=%s action_uuid=%s uuid=%s step="%s" msg="%s" log_index=%s timestamp=%s' % \
                   (time_str ,self.hostname, level, self.action_uuid, self.action_uuid,
                    None if not step else step.replace("\"", "'"), None if not message else message.replace("\"", "'"),
                    self.log_idx, time.time())
            self.log_idx += 1
            return msg
        finally:
            self.log_idx_lock.release()

    '''
        message：必填，日志打印的具体内容
        step：选填，执行步骤
        is_print：是否打印到console
    '''
    def info(self, message, step=None, is_print=False):
        # self.logger.info(self.build_msg(message, "INFO", step, is_print))
        self.logger.info(message)

    def debug(self, message, step=None, is_print=False):
        # self.logger.debug(self.build_msg(message, "DEBUG", step, is_print))
        self.logger.debug(message)

    def error(self, message, step=None, is_print=False):
        # self.logger.error(self.build_msg(message, "ERROR", step, is_print))
        self.logger.error(message)

    def warn(self, message, step=None, is_print=False):
        # self.logger.warn(self.build_msg(message, "WARN", step, is_print))
        self.logger.warn(message)

    def set_total_steps(self, total_steps):
        self.total_step = float(total_steps)

    def set_step(self, step, title=None):
        if step < self.current_step:
            raise RuntimeError("Step can not backward!")
        if step > self.total_step:
            raise RuntimeError("Step can not exceed total steps!")
        self.current_step = step
        percentage = '%0.2f' % (step / self.total_step * 100)
        self.logger.info(self.build_msg(percentage, "PROGRESS", title))

    def print_local_log(self, error_only=False):
        for log in self.local_logs:
            if error_only and log.startswith("Level:[ERROR]"):
                print log
            elif not error_only:
                print log

    def set_console_print(self, is_console_print):
        self.console_print = is_console_print

'''
    message：必填，日志打印的具体内容
    step：选填，执行步骤
    is_print：是否打印到console
'''
def get_logger(uuid=None, console_print=False,
               endpoint='cn-hangzhou.log.aliyuncs.com',
               access_id='LTAI4vHYl1tgSbKJ',
               access_key='1o9vNeR6RqyulO6LWYUxK04ECIo9n9',
               project='shaozhe-private',
               logstore='stockbrain_log'):
    sls_log = SlsLogService(uuid, console_print, endpoint=endpoint, access_id=access_id,
                             access_key=access_key, project=project, logstore=logstore)
    return sls_log.logger
    # raise RuntimeError('Initialize sls logger failed! Make sure uuid is supplied or vnet job')


if __name__ == '__main__':
    # 初始化logger，uuid为唯一标识符，变更平台中，使用action_uuid作为uuid初始化logger对象
    logger = get_logger(uuid='211c31cb-2ca8-43f6-b095-e2913d4e0e9d',)
    # 打印info日志，step用来展示当前操作步骤
    logger.info('test test test 1111')
    # set_total_steps: 设置操作总步数
    # set_step: 设置当前操作步数
    # 在进程一开始的时候调用set_total_steps，用来表示一共有多少步骤
    # 在执行过程中，不断调用set_step，设置递增的当前执行到的步骤
    # 这两个函数用来计算当前执行进度的的百分比
    # logger.set_total_steps(650)
    # logger.set_step(100)
    # time.sleep(2)
    # logger.set_step(200)
    # sls_log.logger.error("get error, reason=103 return_code=333 agent_type=ios")

