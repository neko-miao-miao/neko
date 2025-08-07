package com.emsthymeleaf.controller;

import com.emsthymeleaf.entity.User;
import com.emsthymeleaf.server.UserService;
import com.emsthymeleaf.utils.VerifyCodeUtils;
import jakarta.servlet.ServletOutputStream;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;



import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.IOException;

@Controller
@RequestMapping("/user")
public class UserController {
    private final static Logger log= LoggerFactory.getLogger(UserController.class);
    private UserService userService;
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @RequestMapping("/logout")
    public String logout(HttpSession session){
        session.invalidate();
        return "redirect:/login";
    }

    @RequestMapping("/login")
    public String login(String username,String password,HttpSession session){
        log.debug("用户名:{}",username);
        log.debug("密码:{}",password);
        try {
            User user=userService.login(username,password);
            session.setAttribute("user",user);
        } catch (RuntimeException e) {
            e.printStackTrace();
            return "redirect:/login";
        }
        return "redirect:/employee/list";
    }

    @RequestMapping("/register")
    public String register(User user, String code,HttpSession session){
        log.debug("用户名:{},真名:{},性别:{}",user.getUsername(),user.getRealname(),user.getGender());
        try {
            String sessioncode=session.getAttribute("code").toString();
            if(!sessioncode.equalsIgnoreCase(code)){
                throw new RuntimeException("验证码输入错误");
            }
            userService.register(user);
        } catch (RuntimeException e) {
            e.printStackTrace();
            return "redirect:/regist";//注册失败
        }
        return "redirect:/login";//注册成功
    }
    @RequestMapping("/generateImageCode")
    public void generateImageCode(HttpSession session, HttpServletResponse response) throws IOException {
        String code= VerifyCodeUtils.generateVerifyCode(4);
        session.setAttribute("code",code);
        response.setContentType("image/png");
        ServletOutputStream os = response.getOutputStream();
        VerifyCodeUtils.outputImage(220,60, os,code);
    }


}
