import requests
import time
import allure
from common.logger import Logger

logger = Logger().get_logger()


class RequestUtil:
    """HTTP请求工具类"""
    
    def __init__(self, base_url, timeout=30, max_retries=3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        logger.info(f"初始化RequestUtil，base_url: {base_url}, timeout: {timeout}s")

    @allure.step("发送HTTP请求")
    def send_request(self, method, url, **kwargs):
        """发送HTTP请求，支持重试和详细日志"""
        full_url = self.base_url + url
        
        # 设置默认超时时间
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        start_time = time.time()
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"发送请求 - 方法: {method}, URL: {full_url}, 尝试: {attempt + 1}/{self.max_retries}")
                
                # 记录请求参数（敏感信息脱敏）
                safe_kwargs = self._sanitize_kwargs(kwargs.copy())
                logger.info(f"请求参数: {safe_kwargs}")
                
                response = requests.request(method, full_url, **kwargs)
                
                # 计算响应时间
                response_time = round((time.time() - start_time) * 1000, 2)
                
                # 记录响应信息
                logger.info(f"响应状态码: {response.status_code}, 响应时间: {response_time}ms")
                
                # 记录响应内容（限制长度）
                response_text = response.text[:500] + "..." if len(response.text) > 500 else response.text
                logger.info(f"响应内容: {response_text}")
                
                # 添加到allure报告
                allure.attach(
                    f"Method: {method}\nURL: {full_url}\nResponse Time: {response_time}ms\nStatus Code: {response.status_code}",
                    name="请求信息",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                allure.attach(
                    response.text,
                    name="响应内容",
                    attachment_type=allure.attachment_type.JSON if self._is_json_response(response) else allure.attachment_type.TEXT
                )
                
                # 如果状态码正常或者是最后一次尝试，直接返回
                if response.status_code < 500 or attempt == self.max_retries - 1:
                    return response
                    
                # 5xx错误进行重试
                logger.warning(f"服务器错误 {response.status_code}，将进行重试")
                time.sleep(2 ** attempt)  # 指数退避
                
            except requests.exceptions.Timeout:
                logger.warning(f"请求超时，第{attempt + 1}次尝试")
                if attempt == self.max_retries - 1:
                    logger.error("请求超时，达到最大重试次数")
                    raise
                time.sleep(2 ** attempt)
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"连接错误，第{attempt + 1}次尝试")
                if attempt == self.max_retries - 1:
                    logger.error("连接错误，达到最大重试次数")
                    raise
                time.sleep(2 ** attempt)
                
            except Exception as e:
                logger.error(f"请求发生未知错误: {str(e)}")
                raise
    
    def _sanitize_kwargs(self, kwargs):
        """对请求参数进行脱敏处理"""
        # 脱敏headers中的敏感信息
        if 'headers' in kwargs and kwargs['headers']:
            sanitized_headers = kwargs['headers'].copy()
            for key in sanitized_headers:
                if 'authorization' in key.lower() or 'token' in key.lower():
                    sanitized_headers[key] = "***"
            kwargs['headers'] = sanitized_headers
        
        # 脱敏json中的密码字段
        if 'json' in kwargs and kwargs['json']:
            sanitized_json = kwargs['json'].copy()
            for key in sanitized_json:
                if 'password' in key.lower() or 'pwd' in key.lower():
                    sanitized_json[key] = "***"
            kwargs['json'] = sanitized_json
        
        return kwargs
    
    def _is_json_response(self, response):
        """判断响应是否为JSON格式"""
        try:
            response.json()
            return True
        except:
            return False
    
    def get(self, url, **kwargs):
        """GET请求的便捷方法"""
        return self.send_request("GET", url, **kwargs)
    
    def post(self, url, **kwargs):
        """POST请求的便捷方法"""
        return self.send_request("POST", url, **kwargs)
    
    def put(self, url, **kwargs):
        """PUT请求的便捷方法"""
        return self.send_request("PUT", url, **kwargs)
    
    def delete(self, url, **kwargs):
        """DELETE请求的便捷方法"""
        return self.send_request("DELETE", url, **kwargs)