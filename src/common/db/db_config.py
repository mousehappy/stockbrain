import sys

system = sys.platform

mode = 'remote'
if system == 'darwin':
    mode = 'local'

db_configs = {
    "stock_db": {
        # "host": "47.96.232.139",
        "host": {
            'remote': "47.96.232.139",
            'local': "127.0.0.1"}[mode],
        "port": 58002,
        "user": "root",
        "pwd": "wsz5225260",
        "db": "stock_brain"
    },
    "stock_test": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "pwd": "wsz5225260",
        "db": "stock_test"
    }
}
