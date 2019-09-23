CREATE TABLE stock_finance_mainbz(
`ts_code` varchar(20) not null default '' comment 'TS代码',
`end_date` varchar(20) not null default '' comment '报告期',
`bz_item` varchar(20) not null default '' comment '主营业务来源',
`bz_sales` float(24) comment '主营业务收入(元)',
`bz_profit` float(24) comment '主营业务利润(元)',
`bz_cost` float(24) comment '主营业务成本(元)',
`curr_type` varchar(20) not null default '' comment '货币代码',
`update_flag` varchar(20) not null default '' comment '是否更新',
key (ts_code, end_date, bz_item)) COMMENT '主营业务构成';
