package com.emsthymeleaf.dao;

import com.emsthymeleaf.entity.User;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserDao {
    User findByName(String username);
    void save(User user);
}
