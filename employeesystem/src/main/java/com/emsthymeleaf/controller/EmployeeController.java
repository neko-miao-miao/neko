package com.emsthymeleaf.controller;


import com.emsthymeleaf.entity.Employee;
import com.emsthymeleaf.server.EmployeeService;
import jakarta.servlet.http.HttpSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Controller
@RequestMapping("/employee")
public class EmployeeController {
    private final static Logger log= LoggerFactory.getLogger(EmployeeController.class);
    private EmployeeService employeeService;
    @Autowired
    public EmployeeController(EmployeeService employeeService) {
        this.employeeService = employeeService;
    }
    @Value("${photo.file.path}")
    private String realpath;

    @RequestMapping("/delete")
    public String delete(Integer id,HttpSession session){
        if(session.getAttribute("user")==null){
            return "redirect:/loginAgain";
        }
        Employee employee = employeeService.findById(id);
        employeeService.delete(id);
        new File(realpath,employee.getPhoto()).delete();//删照片
        return "redirect:/employee/list";
    }

    @RequestMapping("/detail")//检索要更新的员工信息
    public String detail(Integer id,Model model,HttpSession session){
        if(session.getAttribute("user")==null){
            return "redirect:/loginAgain";
        }
        Employee employee=employeeService.findById(id);
        model.addAttribute("employee",employee);
        return "/updateEmp";
    }

    @RequestMapping("/update")//更新员工信息
    public String update(Employee employee, MultipartFile img, HttpSession session) throws IOException {
        if(session.getAttribute("user")==null){
            return "redirect:/loginAgain";
        }
        //添加了新头像
        if (!img.isEmpty()) {
            //删掉老图
            String oldPhoto = employeeService.findById(employee.getId()).getPhoto();
            File file = new File(realpath, oldPhoto);
            if(file.exists())file.delete();
            //添加新图
            String originalFilename = img.getOriginalFilename();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss-SSS");
            String fileNamePrefix = LocalDateTime.now().format(formatter);
            //分割链接命名
            String fileNameSuffix=originalFilename.substring(originalFilename.lastIndexOf("."));
            String newFileName=fileNamePrefix+fileNameSuffix;
            img.transferTo(new File(realpath,newFileName));

            employee.setPhoto(newFileName);


        }
        employeeService.update(employee);
        return "redirect:/employee/list";
    }

    @RequestMapping("/save")//添加员工信息
    public String save(Employee employee, MultipartFile img,HttpSession session) throws IOException {
        if(session.getAttribute("user")==null){
            return "redirect:/loginAgain";
        }
        log.debug("姓名:{}, 薪资:{}, 生日:{} ", employee.getName(), employee.getSalary(), employee.getBirthday());
        String originalFilename = img.getOriginalFilename();
        log.debug("头像名称: {}", originalFilename);
        log.debug("头像大小: {}", img.getSize());
        log.debug("上传的路径: {}", realpath);

        //保存照片
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm-ss-SSS");
        String fileNamePrefix = LocalDateTime.now().format(formatter);
        String fileNameSuffix=originalFilename.substring(originalFilename.lastIndexOf("."));
        String newFileName=fileNamePrefix+fileNameSuffix;
        img.transferTo(new File(realpath,newFileName));

        log.debug("文件名：{}",newFileName);
        employee.setPhoto(newFileName);
        employeeService.save(employee);
        return "redirect:/employee/list";
    }


    @RequestMapping("/list")
    public String list(Model model){
        log.debug("查询所有员工信息");
        List<Employee> employeeList = employeeService.list();
        model.addAttribute("employeeList",employeeList);
        return "/emplist";
    }

}
