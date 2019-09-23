CREATE TABLE stock_finance_forecast(
`ts_code` varchar(20) not null default '' comment 'TS股票代码',
`ann_date` varchar(20) not null default '' comment '公告日期',
`end_date` int(20) not null default 0 comment '报告期',
`type` varchar(20) not null default '' comment '业绩预告类型(预增/预减/扭亏/首亏/续亏/续盈/略增/略减)',
`p_change_min` float(20) comment '预告净利润变动幅度下限（%）',
`p_change_max` float(20) comment '预告净利润变动幅度上限（%）',
`net_profit_min` float(20) comment '预告净利润下限（万元）',
`net_profit_max` float(20) comment '预告净利润上限（万元）',
`last_parent_net` float(20) comment '上年同期归属母公司净利润',
`first_ann_date` varchar(20) not null default '' comment '首次公告日',
`summary` varchar(20) not null default '' comment '业绩预告摘要',
`change_reason` varchar(20) not null default '' comment '业绩变动原因',
key (ts_code, end_date))
PARTITION BY RANGE(end_date)
(
PARTITION p2016 VALUES LESS THAN (20170101),
PARTITION p2017 VALUES LESS THAN (20180101),
PARTITION p2018 VALUES LESS THAN (20190101),
PARTITION p2019 VALUES LESS THAN (20200101),
PARTITION p2020 VALUES LESS THAN (20210101),
PARTITION p2021 VALUES LESS THAN (20220101),
PARTITION p2022 VALUES LESS THAN (20230101)
);
