import logging

# 配置日志级别为 DEBUG（默认是 WARNING）
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("这是 DEBUG 级别日志")
logging.info("这是 INFO 级别日志")
logging.warning("这是 WARNING 级别日志")
