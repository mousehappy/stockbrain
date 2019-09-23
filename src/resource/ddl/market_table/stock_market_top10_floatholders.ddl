CREATE TABLE stock_market_top10_floatholders(
`ts_code` varchar(20) not null default '' comment 'TS股票代码',
`ann_date` varchar(20) not null default '' comment '公告日期',
`end_date` varchar(20) not null default '' comment '报告期',
`holder_name` varchar(20) not null default '' comment '股东名称',
`hold_amount` float(24) comment '持有数量（股）',
`hold_ratio` float(24) comment '持有比例',
key (ts_code, end_date)) COMMENT '前十大股东';
