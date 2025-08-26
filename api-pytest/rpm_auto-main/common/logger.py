"""
日志管理工具
"""
import logging
import os
from datetime import datetime


class Logger:
    """日志管理类"""
    
    def __init__(self, name=None, level=logging.INFO):
        self.logger = logging.getLogger(name or __name__)
        self.logger.setLevel(level)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 创建logs目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 文件处理器
        log_file = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d')}.log")#文件命名
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """获取logger实例"""
        return self.logger
    
    def info(self, message):
        """记录信息级别日志"""
        self.logger.info(message)
    
    def debug(self, message):
        """记录调试级别日志"""
        self.logger.debug(message)
    
    def warning(self, message):
        """记录警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录错误级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """记录严重错误级别日志"""
        self.logger.critical(message)
