package com.emsthymeleaf.server;


import com.emsthymeleaf.dao.UserDao;
import com.emsthymeleaf.entity.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;


import java.nio.charset.StandardCharsets;
import java.util.Optional;
@Service

public class UserServiceImpl implements UserService{
    private UserDao userDao;
    private final static Logger log= LoggerFactory.getLogger(UserServiceImpl.class);
    @Autowired
    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public User login(String username, String password) {
        User user = userDao.findByName(username);
        Optional<User> a = Optional.ofNullable(user);
        if (!a.isPresent()) {
            throw new RuntimeException("用户名不存在");
        }

        String passwordSecret = DigestUtils.md5DigestAsHex(password.getBytes(StandardCharsets.UTF_8));
        log.debug("输入密码为：{}，真正密码为：{}",passwordSecret,user.getPassword());
        if(!passwordSecret.equals(user.getPassword()))throw new RuntimeException("密码输入错误");
        return user;
    }

    @Override
    public void register(User user) {
        Optional<User> a = Optional.ofNullable(userDao.findByName(user.getUsername()));
        if (a.isPresent()) {
            throw new RuntimeException("用户名已被注册");
        }
        String newPassword = DigestUtils.md5DigestAsHex(user.getPassword().getBytes(StandardCharsets.UTF_8));
        user.setPassword(newPassword);
        userDao.save(user);
    }
}
