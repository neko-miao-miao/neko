import allure
import pytest
from common.contract_api import ContractAPI
from common.assert_util import AssertUtil
from common.data_validator import DataValidator

@allure.feature("合同管理数据校验")
class TestContractValidation:
    
    @allure.story("创建合同 - 完整数据校验")
    def test_create_contract_full_validation(self, req, headers, contract_data):
        """测试创建合同的完整数据校验"""
        with allure.step("准备测试数据"):
            payload = contract_data["create_contract"]["valid_data"]
            expected_schema = contract_data["create_contract"]["expected_response"]["schema"]
            business_rules = contract_data["create_contract"]["expected_response"]["business_rules"]
        
        with allure.step("发送创建合同请求"):
            contract_api = ContractAPI(req)
            response = contract_api.create_contract(payload, headers)
        
        with allure.step("基础响应校验"):
            AssertUtil.assert_response_success(response)
        
        with allure.step("数据结构校验"):
            validator = DataValidator(response)
            validator.validate_schema(expected_schema)
        
        with allure.step("业务规则校验"):
            validator.validate_business_rules(business_rules)
        
        with allure.step("自定义字段校验"):
            # 校验创建时间格式
            AssertUtil.assert_field_regex(response, "data.created_time", r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
            
            # 校验金额范围
            AssertUtil.assert_field_value_range(response, "data.amount", min_value=1, max_value=10000000)
            
            # 校验合同编号不为空
            AssertUtil.assert_field_contains(response, "data.contract_no", "CT")
    
    @allure.story("查询合同 - 列表数据校验")
    def test_get_contract_list_validation(self, req, headers, contract_data):
        """测试查询合同列表的数据校验"""
        with allure.step("准备查询参数"):
            params = contract_data["get_contract"]["valid_params"]
            expected_schema = contract_data["get_contract"]["expected_response"]["schema"]
            business_rules = contract_data["get_contract"]["expected_response"]["business_rules"]
        
        with allure.step("发送查询请求"):
            contract_api = ContractAPI(req)
            response = contract_api.get_contract(params, headers)#返回多个合同表
        
        with allure.step("响应数据校验"):
            validator = DataValidator(response)
            validator.validate_schema(expected_schema).validate_business_rules(business_rules)
        
        with allure.step("列表项数据校验"):
            response_data = response.json()
            contract_list = response_data.get("data", [])
            
            if contract_list:
                # 校验第一个合同的必需字段
                first_contract = contract_list[0]
                required_fields = ["id", "name", "amount", "status", "created_time"]
                AssertUtil.assert_dict_contains_keys({"data": first_contract}, 
                                                   [f"data.{field}" for field in required_fields])
                
                # 校验所有合同的状态值
                for contract in contract_list:
                    status = contract.get("status")
                    assert status in ["draft", "active", "pending", "completed"], f"无效的合同状态: {status}"
    
    @pytest.mark.parametrize("test_case", [
        {
            "name": "金额校验",
            "field": "data.amount",
            "rules": [
                {"operator": "gte", "value": 0, "message": "金额不能为负数"},
                {"operator": "lte", "value": 10000000, "message": "金额不能超过1000万"}
            ]
        },
        {
            "name": "状态校验", 
            "field": "data.status",
            "rules": [
                {"operator": "in", "value": ["draft", "active", "pending"], "message": "状态值无效"}
            ]
        }
    ])
    def test_contract_field_validation(self, req, headers, contract_data, test_case):
        """参数化测试合同字段校验"""
        with allure.step(f"执行{test_case['name']}"):
            payload = contract_data["create_contract"]["valid_data"]
            
            contract_api = ContractAPI(req)
            response = contract_api.create_contract(payload, headers)
            
            AssertUtil.assert_response_success(response)
            
            # 应用自定义校验规则
            validator = DataValidator(response)
            for rule in test_case["rules"]:
                business_rule = {
                    "field": test_case["field"],
                    "operator": rule["operator"],
                    "value": rule["value"],
                    "message": rule["message"]
                }
                validator.validate_business_rules([business_rule])