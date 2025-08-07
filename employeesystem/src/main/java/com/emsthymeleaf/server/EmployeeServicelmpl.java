package com.emsthymeleaf.server;

import com.emsthymeleaf.dao.EmployeeDao;
import com.emsthymeleaf.entity.Employee;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class EmployeeServicelmpl implements EmployeeService{
    private EmployeeDao employeeDao;
    @Autowired
    public EmployeeServicelmpl(EmployeeDao employeeDao) {
        this.employeeDao = employeeDao;
    }

    @Override
    public List<Employee> list() {

        return employeeDao.list();
    }

    @Override
    public void save(Employee employee) {
        employeeDao.save(employee);
    }

    @Override
    public Employee findById(Integer id) {
        return employeeDao.findById(id);
    }

    @Override
    public void update(Employee employee) {
         employeeDao.update(employee);
    }

    @Override
    public void delete(Integer id) {
        employeeDao.delete(id);
    }


}
