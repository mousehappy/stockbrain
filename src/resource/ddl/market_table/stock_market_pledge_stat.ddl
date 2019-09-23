CREATE TABLE stock_market_pledge_stat(
`ts_code` varchar(20) not null default '' comment 'Y	TS代码',
`end_date` varchar(20) not null default '' comment 'Y	截至日期',
`pledge_count` int comment 'Y	质押次数',
`unrest_pledge` float(24) comment 'Y	无限售股质押数量（万）',
`rest_pledge` float(24) comment 'Y	限售股份质押数量（万）',
`total_share` float(24) comment 'Y	总股本',
`pledge_ratio` float(24) comment 'Y	质押比例',
key (ts_code, end_date)) COMMENT '股权质押统计数据';
