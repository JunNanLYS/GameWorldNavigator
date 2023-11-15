import logging

# 设置logging级别以及格式化器
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] | %(name)s | %(asctime)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
__log__ = True
