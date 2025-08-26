"""
项目管理相关API封装
"""
import allure
from common.logger import Logger

logger = Logger().get_logger()

class ProjectAPI:
    """项目管理API封装类"""
    
    def __init__(self, request_util):
        self.req = request_util
    
    @allure.step("创建项目")
    def create_project(self, payload, headers):
        """创建项目"""
        url = "/rpm-api/project/create"
        logger.info(f"创建项目请求: {payload}")
        response = self.req.send_request("POST", url, json=payload, headers=headers)
        logger.info(f"创建项目响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("查询项目列表")
    def get_project_list(self, params, headers):
        """查询项目列表"""
        url = "/rpm-api/project/list"
        logger.info(f"查询项目列表请求参数: {params}")
        response = self.req.send_request("GET", url, params=params, headers=headers)
        logger.info(f"查询项目列表响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("根据ID获取项目详情")
    def get_project_by_id(self, project_id, headers):
        """根据ID获取项目详情"""
        url = f"/rpm-api/project/{project_id}"
        logger.info(f"获取项目详情ID: {project_id}")
        response = self.req.send_request("GET", url, headers=headers)
        logger.info(f"获取项目详情响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("更新项目")
    def update_project(self, project_id, payload, headers):
        """更新项目"""
        url = f"/rpm-api/project/{project_id}"
        logger.info(f"更新项目ID: {project_id}, 数据: {payload}")
        response = self.req.send_request("PUT", url, json=payload, headers=headers)
        logger.info(f"更新项目响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("删除项目")
    def delete_project(self, project_id, headers):
        """删除项目"""
        url = f"/rpm-api/project/{project_id}"
        logger.info(f"删除项目ID: {project_id}")
        response = self.req.send_request("DELETE", url, headers=headers)
        logger.info(f"删除项目响应: {response.status_code} - {response.text}")
        return response
    
    @allure.step("搜索项目")
    def search_projects(self, params, headers):
        """搜索项目"""
        url = "/rpm-api/project/search"
        logger.info(f"搜索项目请求参数: {params}")
        response = self.req.send_request("GET", url, params=params, headers=headers)
        logger.info(f"搜索项目响应: {response.status_code} - {response.text}")
        return response
    
    #@allure.step("批量操作项目")
    #def batch_operate_projects(self, operation, project_ids, headers):
        """批量操作项目"""
        url = "/rpm-api/project/batch"
        payload = {
            "operation": operation,
            "project_ids": project_ids
        }
        logger.info(f"批量操作项目: {operation}, IDs: {project_ids}")
        response = self.req.send_request("POST", url, json=payload, headers=headers)
        logger.info(f"批量操作项目响应: {response.status_code} - {response.text}")
        return response 