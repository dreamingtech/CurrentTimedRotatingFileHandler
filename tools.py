# import sys, os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)

# 常用工具
import logging
import os
import platform

try:
    from ctrf_handler import CTRFHandler
except:
    from common_tools.ctrf_handler import CTRFHandler

platform_name = platform.system().lower()


def singleton(cls, *args, **kwargs):
    """
    装饰器实现 python 单例模式
    https://www.cnblogs.com/PigeonNoir/articles/9392047.html
    https://www.cnblogs.com/jiangxinyang/p/8454418.html
    https://blog.csdn.net/qq_35462323/article/details/82912027
    """
    # 创建一个instances字典用来保存单例
    instances = {}

    # 创建一个内层函数来获得单例, 添加不定长参数, 以与 redis_conn 中 __init__ 中传递的参数相符合
    def _get_instance(*args, **kwargs):
        # 判断instances字典中是否含有单例，如果没有就创建单例并保存到instances字典中，然后返回该单例
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    # 返回内层函数 get_instance
    return _get_instance


def get_full_log_path(parent_path=None, log_folder_name="log", log_file_name_base="news_spider.log"):
    """
    获取日志文件保存的完整路径
    parent_path/log_folder_name/log_file_name_base
    news_spider 中, 所以的日志都保存到 根目录下的 log 目录中, 所以这里不再需要从外部传入 parent_path
    news_spider 中, 所有的日志都是以 news_spider.log 为前缀的, 所以这里也不再需要传入 log_file_name_base
    :param parent_path: 日志文件所在的目录的父级目录
    :param log_folder_name: 日志文件所在的目录
    :param log_file_name_base: 日志文件名的前缀
    :return:
    """
    # log_file_name_base = "goods_crawler.log"
    # log_folder_name = "log"

    # todo print(os.path.dirname(os.path.abspath(__file__)))
    # todo print(os.path.dirname(__file__))
    # 如果没有传递 parent_path 这个参数, 就使用 tools.py 所在的目录为父级目录
    # if parent_path is None:
    parent_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(parent_path)

    # 默认图片保存的目录名, 当前文件所在目录下 './log'
    log_folder_path = os.path.join(parent_path, log_folder_name)
    log_file_path_full = os.path.join(log_folder_path, log_file_name_base)

    # 判断文件保存的目录是否存在, 如果不存在, 就创建,
    if not os.path.exists(log_folder_path):
        os.mkdir(log_folder_path)

    return log_file_path_full


def get_logger(log_name=__name__, filename=None):
    """
    获取 logger 日志记录器
    :param log_name: 日志记录器的名称
    :param filename: 日志文件的文件名
    :return: logger 对象
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    # 定义 current timed rotating file handler
    # 每天的 00:00:00 进行日志的切换
    ctrf_handler = CTRFHandler(filename, when="midnight", encoding="utf-8")
    ctrf_handler.setLevel(logging.INFO)

    ctrf_handler_formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)-7s - [%(lineno)3d]:%(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    ctrf_handler.setFormatter(ctrf_handler_formatter)

    # 定义stream handler, stream=None等价于stream=sys.stderr, 等价于不写参数
    s_handler = logging.StreamHandler(stream=None)
    s_handler.setLevel(logging.DEBUG)
    s_handler_formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)-7s - [%(lineno)3d]:%(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    s_handler.setFormatter(s_handler_formatter)

    # 如果是在 windows 上运行, 同时添加 file handler 和 stream handler
    # 如果是在 linux 上运行, 只添加 file handler
    if platform_name.lower() == "windows":
        logger.addHandler(ctrf_handler)
        logger.addHandler(s_handler)
    if platform_name.lower() == "linux":
        logger.addHandler(ctrf_handler)

    return logger
