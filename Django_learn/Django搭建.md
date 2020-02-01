## Django搭建

- 参考：https://www.jb51.net/article/168817.htm

- #### 新建文件夹my_test

- #### 创建虚拟环境

  在my_test文件夹下

  ```
  python -m venv Django_test
  ```

  Django_test为新建的虚拟环境（文件夹）的名称，可修改。

- #### 激活虚拟环境

  ```
  Django_test\Scripts\activate
  ```

  

- #### 在虚拟环境中安装Django

  ```
  pip install Django
  ```

  可通过以下，测试是否可以调用

  ```
  django-admin help
  ```

  

- #### 新建项目

  在my_test文件夹下

  ```
  django-admin startproject my_blog .
  ```

  my_blog为项目名可改，注意结尾句点，让新项目使用合适的目录结构，这样开发完成后可轻松地将应用程序部署到服务器

- #### 启动服务

  ```
  python manage.py runserver
  ```

  

- 