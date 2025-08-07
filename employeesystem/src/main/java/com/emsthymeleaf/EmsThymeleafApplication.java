package com.emsthymeleaf;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class EmsThymeleafApplication {//localhost:8088/ems-thymeleaf/login启动
//运行前先修改application.properties中的图片存储绝对路径和mysql数据库的配置
	public static void main(String[] args) {
		SpringApplication.run(EmsThymeleafApplication.class, args);
	}

}
