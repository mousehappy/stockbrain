from crawler.base.db_base.stock_db_base import StockDBBase


class A(StockDBBase):
    def __init__(self):
        super(A, self).__init__()

    def __del__(self):
        print "A is destructed!"


class B(A):
    def __del__(self):
        super(B, self).__del__()
        print "B is destructed!"


def test_func():
    a = A()
    a.close()


if __name__ == '__main__':
    test_func()

