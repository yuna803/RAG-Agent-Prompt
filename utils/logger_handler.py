import logging
import os
from future.backports.datetime import datetime
from utils.path_tool import get_abs_path

"""创建日志工具"""
# 日志根目录
LOG_ROOT = get_abs_path("logs")
# 创建日志目录
os.makedirs(LOG_ROOT, exist_ok=True)

#日志的格式配置
DEFAULT_LOG_FORMAT=logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

def get_logger(name: str = "agent",
               console_level: int = logging.INFO,
               log_file: str = None,        # 仍接受外部指定，但内部会补 全默认值
               file_level: int = logging.DEBUG
               ) -> logging.Logger:
    """
        获取日志对象（默认同时输出到控制台和 logs 目录下的文件）
        :param name: 日志名称
        :param console_level: 控制台日志级别
        :param log_file: 自定义日志文件名（不含路径和扩展名），若为 None 则自动使用 '{name}.log'
        :param file_level: 文件日志级别
        :return: logger 对象
    """
    loger = logging.getLogger(name)
    loger.setLevel(logging.DEBUG)

    # 判断日志处理器是否已经存在
    if loger.handlers:
        return loger

    #控制台的Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    loger.addHandler(console_handler)

    # 文件Handler
    if not log_file:
        file_name = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        log_file = get_abs_path(os.path.join(LOG_ROOT, file_name))

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    loger.addHandler(file_handler)

    return loger


logger=get_logger()

if __name__ == '__main__':
    logger.info("信息日志")
    logger.debug("调试日志")
    logger.warning("警告日志")
    logger.error("错误日志")