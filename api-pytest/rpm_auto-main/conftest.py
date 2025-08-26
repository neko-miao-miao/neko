import pytest
import yaml
import time
import os
from common.request_util import RequestUtil
from common.logger import Logger

logger = Logger().get_logger()

@pytest.fixture(scope="session")
def config():
    """加载配置文件，支持环境变量覆盖"""
    # 支持通过环境变量指定配置文件
    env = os.getenv("TEST_ENV", "default")
    config_file = f"config/config_{env}.yaml" if env != "default" else "config/config.yaml"#环境的切换
    
    if not os.path.exists(config_file):
        config_file = "config/config.yaml"  # 回退到默认配置
    
    logger.info(f"加载配置文件: {config_file}")
    with open(config_file, encoding="utf-8") as f:
        config_data = yaml.safe_load(f)#加载环境配置文件
    
    # 环境变量覆盖配置#命令行set BASE_URL="..."可以覆盖
    if os.getenv("BASE_URL"):
        config_data["base_url"] = os.getenv("BASE_URL")
    if os.getenv("USERNAME"):
        config_data["username"] = os.getenv("USERNAME")
    if os.getenv("PASSWORD"):
        config_data["password"] = os.getenv("PASSWORD")
    
    logger.info(f"当前配置: base_url={config_data.get('base_url')}, username={config_data.get('username')}")
    return config_data

@pytest.fixture(scope="session")
def req(config):
    """请求工具实例"""
    return RequestUtil(config["base_url"])

@pytest.fixture(scope="session")
def captcha_and_checkkey(req):
    """自动获取验证码和checkKey，带重试机制"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            url = f"/rpm-api/auth/generateCaptcha?checkKey=&_t={int(time.time() * 1000)}"
            headers = {
                "accept": "application/json, text/plain, */*",
                "appid": "app-7zpfoeqntj6",
                "content-type": "application/json;charset=UTF-8",
            }
            response = req.send_request("GET", url, headers=headers)
            assert response.status_code == 200
            assert response.json()["code"] == "200"
            data = response.json()["data"]
            logger.info(f"成功获取验证码和checkKey，第{attempt + 1}次尝试")
            return data["checkKey"]
        except Exception as e:
            logger.warning(f"获取验证码失败，第{attempt + 1}次尝试: {str(e)}")
            if attempt == max_retries - 1:
                logger.error("获取验证码达到最大重试次数，测试终止")
                raise
            time.sleep(2)  # 重试前等待2秒

@pytest.fixture(scope="session")
def token(req, config, captcha_and_checkkey):#登陆
    """通过登录接口获取token，动态获取checkKey，带重试机制"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            checkKey = captcha_and_checkkey
            url = "/rpm-api/auth/login"
            headers = {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json;charset=UTF-8",
                "appid": "app-7zpfoeqntj6",
            }
            data = {
                "username": config["username"],
                "password": config["password"],
                "checkKey": checkKey,
                "captcha": config["captcha"]
            }
            logger.info(f"尝试登录，第{attempt + 1}次尝试")
            response = req.send_request("POST", url, json=data, headers=headers)
            assert response.status_code == 200
            assert response.json()["code"] == "200"
            token_value = response.json()["data"]["token"]
            logger.info("登录成功，获取到token")
            return token_value
        except Exception as e:
            logger.warning(f"登录失败，第{attempt + 1}次尝试: {str(e)}")
            if attempt == max_retries - 1:
                logger.error("登录达到最大重试次数，测试终止")
                raise
            time.sleep(2)  # 重试前等待2秒
    return None


@pytest.fixture(scope="session")
def headers(token):
    """自动生成带token的请求头"""
    headers_dict = {"Authorization": f"Bearer {token}"}
    logger.info("生成请求头成功")
    return headers_dict

@pytest.fixture(scope="session")
def contract_data():
    """加载合同测试数据"""
    data_file = "data/contract_data.yaml"
    logger.info(f"加载测试数据文件: {data_file}")
    with open(data_file, encoding="utf-8") as f:
        return yaml.safe_load(f)

# pytest钩子函数
def pytest_configure(config):
    """pytest配置钩子"""
    logger.info("=" * 80)
    logger.info("开始执行自动化测试")
    logger.info("=" * 80)

def pytest_unconfigure(config):
    """pytest结束钩子"""
    logger.info("=" * 80)
    logger.info("自动化测试执行完成")
    logger.info("=" * 80)

def pytest_runtest_setup(item):
    """每个测试用例开始前的钩子"""
    logger.info(f"开始执行测试用例: {item.name}")

def pytest_runtest_teardown(item):
    """每个测试用例结束后的钩子"""
    logger.info(f"测试用例执行完成: {item.name}")

@pytest.fixture(autouse=True)
def log_test_info(request):
    """自动记录测试信息的fixture"""
    test_name = request.node.name
    logger.info(f"当前测试: {test_name}")
    yield
    # 测试结束后的清理工作可以在这里添加