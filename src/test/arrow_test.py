#-*- coding: UTF-8 -*-
import arrow
import calendar

if __name__ == '__main__':
    start_dt = arrow.get('2019-09-01 05:00:00')
    end_dt = arrow.get('2019-09-14 01:00:00')

    # time_span = end_dt - start_dt
    # print time_span.days
    print start_dt.month
    print calendar.monthrange(2019, 1)[1]