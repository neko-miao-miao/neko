package com.emsthymeleaf.server;

import com.emsthymeleaf.entity.User;


public interface UserService {
    public void register(User user) ;

    public User login(String username, String password);
}
