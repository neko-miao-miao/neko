package com.emsthymeleaf.dao;

import com.emsthymeleaf.entity.Employee;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface EmployeeDao {
    List<Employee> list();

    void save(Employee employee);

    Employee findById(Integer id);

    void update(Employee employee);

    void delete(Integer id);
}
