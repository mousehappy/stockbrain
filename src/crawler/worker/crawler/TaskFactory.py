# -*- coding: UTF-8 -*-
import json
import os
import importlib

file_path = os.path.abspath(__file__)
# print file_path
src_path = file_path.split('/')
TASK_BASE_PATH = '/'.join(src_path[:-3]) + '/task'
# print task_path

# TASK_BASE_PATH = '/Users/wjq/work/stockbrain/src/crawler/task'
BASE_PKT_PATH = 'crawler.task'

module_map = dict()


class TaskFactory(object):
    @classmethod
    def init_task_instance(cls, clz_name, base_path=TASK_BASE_PATH):
        if len(module_map) == 0:
            cls.search_path(base_path, BASE_PKT_PATH, module_map)
        if clz_name not in module_map:
            raise RuntimeError('Task class [%s] not found!' % clz_name)
        module_name = module_map.get(clz_name)
        m = importlib.import_module(module_name)
        t_clz = getattr(m, clz_name)
        task = t_clz()
        return task

    @classmethod
    def search_path(cls, path, pkt_path, task_map):
        dirs = os.listdir(path)
        for filename in dirs:
            fileabspath = os.path.join(path, filename)
            if os.path.isdir(fileabspath):
                new_pkt_path = pkt_path + '.' + filename
                cls.search_path(fileabspath, new_pkt_path, task_map)
            elif os.path.isfile(fileabspath):
                if filename.endswith('.py') and filename != '__init__.py':
                    module_name = filename.split('.')[0]
                    module_path = pkt_path + '.' + module_name
                    task_map[module_name] = module_path


if __name__ == '__main__':
    # t = TaskFactory()
    task = TaskFactory.init_task_instance('DailyHkHoldTask')
    print type(task)
