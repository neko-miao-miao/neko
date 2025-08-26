import allure
import pytest
from common.contract_api import ContractAPI
from common.assert_util import AssertUtil

@allure.feature("合同管理")
class TestContract:
    
    @allure.story("创建合同")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_contract(self, req, headers, contract_data):
        """测试创建合同"""
        with allure.step("准备测试数据"):
            payload = contract_data["create_contract"]["valid_data"]
        
        with allure.step("发送创建合同请求"):
            contract_api = ContractAPI(req)
            response = contract_api.create_contract(payload, headers)
        
        with allure.step("验证响应结果"):
            AssertUtil.assert_response_success(response)
            assert "data" in response.json()
    
    @allure.story("查询合同")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_contract(self, req, headers, contract_data):
        """测试查询合同"""
        with allure.step("准备查询参数"):
            params = contract_data["get_contract"]["valid_params"]
        
        with allure.step("发送查询合同请求"):
            contract_api = ContractAPI(req)
            response = contract_api.get_contract(params, headers)
        
        with allure.step("验证响应结果"):
            AssertUtil.assert_response_success(response)
    
    @allure.story("更新合同")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("contract_id,update_data", [
        (1, {"name": "更新合同名称", "amount": 20000}),
        (2, {"status": "active"})
    ])#参数化
    def test_update_contract(self, req, headers, contract_id, update_data):
        """测试更新合同"""
        with allure.step(f"更新合同ID: {contract_id}"):
            contract_api = ContractAPI(req)
            response = contract_api.update_contract(contract_id, update_data, headers)
        
        with allure.step("验证更新结果"):
            AssertUtil.assert_response_success(response)