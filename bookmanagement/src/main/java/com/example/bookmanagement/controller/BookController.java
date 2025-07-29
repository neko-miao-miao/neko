package com.example.bookmanagement.controller;

import com.example.bookmanagement.model.Book;
import com.example.bookmanagement.service.BookService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;



@Controller
public class BookController {
    @Autowired
    private BookService bookService;

    @GetMapping("/")
    public String index(Model model) {//Model把后端的数据传给前端
        model.addAttribute("books", bookService.getAllBooks());
        //addAttribute(String attributeName, Object attributeValue)：添加一个键值对到模型中。
        //addAttribute(Object attributeValue)：添加一个对象到模型中，对象的类名（首字母小写）将作为键。
        //addAttribute(String attributeName)：添加一个默认值为 null 的键到模型中。
        return "index";
    }

    @GetMapping("/add")
    public String addBookForm(Model model) {
        model.addAttribute("book", new Book());
        return "add_book";
    }

    @PostMapping("/add")
    public String addBook(Book book) {
        bookService.saveBook(book);
        return "redirect:/";
    }

    @GetMapping("/edit/{id}")
    public String editBookForm(@PathVariable Long id, Model model) {
        model.addAttribute("book", bookService.getBookById(id));
        return "edit_book";
    }

    @PostMapping("/edit/{id}")
    public String editBook(@PathVariable Long id, Book book) {
        book.setId(id);
        bookService.saveBook(book);
        return "redirect:/";
    }

    @GetMapping("/delete/{id}")
    public String deleteBook(@PathVariable Long id) {
        bookService.deleteBook(id);
        return "redirect:/";
    }

    @GetMapping("/search")
    public String searchBooks(@RequestParam String title, Model model) {
        model.addAttribute("books", bookService.searchBooks(title));
        return "index";
    }
}