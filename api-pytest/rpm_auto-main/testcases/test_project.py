import allure
import pytest
from common.project_api import ProjectAPI
from common.assert_util import AssertUtil

@allure.feature("项目管理")
class TestProject:
    
    @allure.story("创建项目")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_project(self, req, headers):
        """测试创建项目"""
        with allure.step("准备测试数据"):
            payload = {
                "name": "自动化测试项目",
                "description": "这是一个自动化测试创建的项目",
                "type": "clinical_trial",
                "status": "planning"
            }
        
        with allure.step("发送创建项目请求"):
            project_api = ProjectAPI(req)
            response = project_api.create_project(payload, headers)
        
        with allure.step("验证响应结果"):
            AssertUtil.assert_response_success(response)
            AssertUtil.assert_response_contains_field(response, "data")
    
    @allure.story("查询项目列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_project_list(self, req, headers):
        """测试查询项目列表"""
        with allure.step("准备查询参数"):
            params = {
                "page": 1,
                "size": 10,
                "status": "active"
            }
        
        with allure.step("发送查询项目列表请求"):
            project_api = ProjectAPI(req)
            response = project_api.get_project_list(params, headers)
        
        with allure.step("验证响应结果"):
            AssertUtil.assert_response_success(response)
            AssertUtil.assert_response_data_not_empty(response)
    
    @allure.story("获取项目详情")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("project_id", [1, 2])
    def test_get_project_detail(self, req, headers, project_id):
        """测试获取项目详情"""
        with allure.step(f"获取项目ID: {project_id} 的详情"):
            project_api = ProjectAPI(req)
            response = project_api.get_project_by_id(project_id, headers)
        
        with allure.step("验证项目详情"):
            AssertUtil.assert_response_success(response)
            project_data = response.json()["data"]
            required_fields = ["id", "name", "status", "created_time"]
            AssertUtil.assert_dict_contains_keys(project_data, required_fields)
    
    @allure.story("更新项目状态")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_project_status(self, req, headers):
        """测试更新项目状态"""
        project_id = 1
        
        with allure.step("准备更新数据"):
            update_data = {
                "status": "active",
                "remarks": "状态更新测试"
            }
        
        with allure.step(f"更新项目ID: {project_id} 的状态"):
            project_api = ProjectAPI(req)
            response = project_api.update_project(project_id, update_data, headers)
        
        with allure.step("验证更新结果"):
            AssertUtil.assert_response_success(response)
    
    @allure.story("删除项目")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_project(self, req, headers):
        """测试删除项目"""
        project_id = 999  # 使用不存在的ID进行测试
        
        with allure.step(f"删除项目ID: {project_id}"):
            project_api = ProjectAPI(req)
            response = project_api.delete_project(project_id, headers)
        
        with allure.step("验证删除结果"):
            # 预期删除不存在的项目会返回错误
            AssertUtil.assert_response_error(response, expected_message="项目不存在")
    
    @allure.story("搜索项目")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("keyword", ["测试", "clinical", "auto"])
    def test_search_projects(self, req, headers, keyword):
        """测试项目搜索功能"""
        with allure.step(f"搜索关键词: {keyword}"):
            params = {
                "keyword": keyword,
                "page": 1,
                "size": 20
            }
            
            project_api = ProjectAPI(req)
            response = project_api.search_projects(params, headers)
        
        with allure.step("验证搜索结果"):
            AssertUtil.assert_response_success(response)
            # 搜索结果可能为空，这是正常的
