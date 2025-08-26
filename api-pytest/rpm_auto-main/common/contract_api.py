"""
合同管理相关API封装
"""
import allure
from common.logger import Logger

logger = Logger().get_logger()

class ContractAPI:
    """合同管理API封装类"""
    
    def __init__(self, request_util):
        self.req = request_util
    
    @allure.step("创建合同")
    def create_contract(self, payload, headers):
        """创建合同"""
        url = "/rpm-api/contract/create"
        logger.info(f"创建合同请求: {payload}")
        response = self.req.send_request("POST", url, json=payload, headers=headers)
        logger.info(f"创建合同响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("查询合同")
    def get_contract(self, params, headers):
        """查询合同"""
        url = "/rpm-api/contract/list"
        logger.info(f"查询合同请求参数: {params}")
        response = self.req.send_request("GET", url, params=params, headers=headers)
        logger.info(f"查询合同响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("根据ID获取合同详情")
    def get_contract_by_id(self, contract_id, headers):
        """根据ID获取合同详情"""
        url = f"/rpm-api/contract/{contract_id}"
        logger.info(f"获取合同详情ID: {contract_id}")
        response = self.req.send_request("GET", url, headers=headers)
        logger.info(f"获取合同详情响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("更新合同")
    def update_contract(self, contract_id, payload, headers):
        """更新合同"""
        url = f"/rpm-api/contract/{contract_id}"
        logger.info(f"更新合同ID: {contract_id}, 数据: {payload}")
        response = self.req.send_request("PUT", url, json=payload, headers=headers)
        logger.info(f"更新合同响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("删除合同")
    def delete_contract(self, contract_id, headers):
        """删除合同"""
        url = f"/rpm-api/contract/{contract_id}"
        logger.info(f"删除合同ID: {contract_id}")
        response = self.req.send_request("DELETE", url, headers=headers)
        logger.info(f"删除合同响应: {response.status_code} - {response.text}")
        return response 