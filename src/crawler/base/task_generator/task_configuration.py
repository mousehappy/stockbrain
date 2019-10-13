# -*- coding: UTF-8 -*-
task_configs = [
    # {
    #     'name': 'DailyTradeInfoTask',
    #     'init_days': 600,  # 初始抓取数据天数
    #     'type': 1  # 1:全部stock， 2:每个stock一个任务
    # },
    # {
    #     'name': 'DailyBasicInfoTask',
    #     'init_days': 600,
    #     'type': 1  # 1:全部stock， 2:每个stock一个任务
    # },
    # {
    #     'name': 'DailyBasicInfoTask',
    #     'init_days': 600,
    #     'type': 1  # 1:全部stock， 2:每个stock一个任务
    # },
    {
        'name': 'DfcfConceptInfoDailyTask',
        'init_days': 1,  # 初始抓取数据天数
        'type': 1  # 1:全部stock， 2:每个stock一个任务
    },
    {
        'name': 'DfcfSeasonForecastTask',
        'init_days': 1,  # 初始抓取数据天数
        'type': 1  # 1:全部stock， 2:每个stock一个任务
    },
]
