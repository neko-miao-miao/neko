package com.emsthymeleaf.Exception;

import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public String tooBigImg(Model model){
        model.addAttribute("erromessage","上传照片过大，请重新上传");
        return "/imgerro";
    }



}
