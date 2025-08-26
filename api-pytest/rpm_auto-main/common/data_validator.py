"""
数据校验器
"""
import allure
from typing import Dict, Any, List, Union
from common.logger import Logger

logger = Logger().get_logger()

class DataValidator:
    """响应数据校验器"""
    
    def __init__(self, response):
        self.response = response
        self.data = response.json()
    
    @allure.step("校验响应数据结构")
    def validate_schema(self, expected_schema: Dict[str, type]):
        """校验响应数据结构
        
        Args:
            expected_schema: 期望的数据结构，格式：{"field_name": expected_type}
        """
        #判断键是否存在
        for field_name, expected_type in expected_schema.items():
            if field_name not in self.data:
                assert False, f"响应中缺少必需字段: {field_name}"

            #判断类型是否正确
            actual_value = self.data[field_name]
            if not isinstance(actual_value, expected_type):
                assert False, f"字段{field_name}类型错误，期望{expected_type.__name__}，实际{type(actual_value).__name__}"
        
        logger.info(f"数据结构校验通过: {list(expected_schema.keys())}")
        return self
    
    @allure.step("校验业务规则")
    def validate_business_rules(self, rules: List[Dict[str, Any]]):
        """校验业务规则
        
        Args:
            rules: 业务规则列表，每个规则包含：
                - field: 字段名
                - operator: 操作符 (eq, ne, gt, lt, gte, lte, in, not_in, contains, regex)
                - value: 期望值
                - message: 自定义错误信息（可选）
        """
        for rule in rules:
            field = rule['field']
            operator = rule['operator']
            expected = rule['value']
            custom_message = rule.get('message', '')#没有message字段返回‘ ’
            
            actual = self._get_nested_value(field)#获取要比较的两个value
            
            if not self._check_rule(actual, operator, expected):
                error_msg = custom_message or f"业务规则校验失败: {field} {operator} {expected}，实际值: {actual}"
                assert False, error_msg
        
        logger.info(f"业务规则校验通过: {len(rules)}条规则")
        return self
    
    def _get_nested_value(self, field_path: str):
        """获取嵌套字段值"""
        value = self.data
        for field in field_path.split('.'):
            if isinstance(value, dict) and field in value:
                value = value[field]#获取返回json中相应field下的value
            else:
                return None
        return value
    
    def _check_rule(self, actual, operator: str, expected) -> bool:
        """检查单个规则"""
        import re
        
        operators = {
            'eq': lambda a, e: a == e,
            'ne': lambda a, e: a != e,
            'gt': lambda a, e: a > e,
            'lt': lambda a, e: a < e,
            'gte': lambda a, e: a >= e,
            'lte': lambda a, e: a <= e,
            'in': lambda a, e: a in e,
            'not_in': lambda a, e: a not in e,
            'contains': lambda a, e: e in str(a),
            'regex': lambda a, e: bool(re.match(e, str(a))),
            'length': lambda a, e: len(a) == e if hasattr(a, '__len__') else False,
            'min_length': lambda a, e: len(a) >= e if hasattr(a, '__len__') else False,
            'max_length': lambda a, e: len(a) <= e if hasattr(a, '__len__') else False,
        }
        
        if operator not in operators:
            raise ValueError(f"不支持的操作符: {operator}")
        
        return operators[operator](actual, expected)#传入参数调用lambda比较返回json的value和yaml里的value