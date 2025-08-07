package com.emsthymeleaf.server;

import com.emsthymeleaf.entity.Employee;
import org.springframework.stereotype.Service;

import java.util.List;


public interface EmployeeService {
    List<Employee> list();

    void save(Employee employee);

    Employee findById(Integer id);

    void update(Employee employee);

    void delete(Integer id);


}
