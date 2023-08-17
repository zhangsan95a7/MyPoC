## MyPoC工具介绍

一款自由度更高的POC工具，可根据需要自定义POC，该工具提供批量测试、测试结果的展示和输出等功能。



还有更多的功能与POC等待开发，期待更多师傅们的加入。



项目开始时间：2023年8月13日

项目地址：https://github.com/zhangsan95a7/MyPoC



## 基本使用

```
# 单个URL测试
python MyPoC.py -u "https://www.example.com" -p "用友NC BeanShell RCE(CNVD-2021-30167)"

# 多个URL测试
python MyPoC.py -f target.txt -p "用友NC BeanShell RCE(CNVD-2021-30167)"
```



其他参数的使用请参考工具的帮助信息

```
python MyPoC.py -h
```



## 待开发功能

- ##### --poc-update

  更新POC库，预期：所有使用该框架的使用者执行该参数后，从项目中拉取本地没有的POC，并且将本地自创POC上传至项目POC库



- ##### --out-put

  指定保存结果的文件类型，支持txt，html，excel，可同时输出多种类型，eg: --out-put=txt|html|excel

  目前支持txt、html类型，excel待添加





## 自定义POC

##### POC模板路径：

MyPoC/model/model.py



##### POC的编写和测试：

- ###### 编写

  在MyPoC/poc目录下创建一个目录（必须与POC同名），
  
  将POC模板复制到MyPoC/poc/pocname/路径下进行编写，编写好的POC也放在该目录



- ###### 测试

  ```
  python MyPoC.py -u "https://www.example.com" -p "POC名称"
  ```

  

##### POC命名规范：

- 为防止POC重名和方便后续的查找，有漏洞编号的就添加到后方，如：用友NC BeanShell RCE(CNVD-2021-30167)。对于没有漏洞编号的，可以在括号中加上POC创建的时间，如：用友NC BeanShell RCE(2023-08-15)





## Tips

- 测试多个URL时，可根据URL数量适当增加线程（如果只测试单个POC，则最大线程数可与URL数相等）；如果对单个URL测试，线程适当减小，防止IP被ban





##### 免责声明，本代码仅用于学习，切勿用于其他非法用途，否则后果由使用者自负！！！