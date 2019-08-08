## PostgreSQL 基本语法（持续更新）

- #### 参数介绍

  **databasename**：数据名

  **tablename**：表名

  **fieldname**：字段名

  **fieldclass**：字段类型

  **datavalue**：数据值

  

- #### 创建数据库

  ```sql
  CREATE DATABASE databasename;
  ```

  

- #### 删除数据库

  ```sql
  DROP DATABASE databasename;
  ```

  

- #### 创建表

  ```sql
  CREATE TABLE databasename(
      fieldname1  fieldclass1,
      fieldname2  fieldclass2
  );
  ```

  

- #### 删除表

  ```sql
  DROP TABLE tablename;
  ```

  

- #### 插入行

  1. 无指定字段。PS：字符串加‘’，如datavalue1，数值不加。

     ```sql
     INSERT INTO tablename VALUES ('datavalue1', datavalue2');
     ```

  2. 指定字段插入。

     ```sql
     INSERT INTO tablename (fieldname1, fieldname2) VALUES ('datavalue1', datavalue2);
     ```



- #### 查询

  1. 查询所有数据。

     ```sql
     SELECT * FROM tablename
     ```

  2. 查询指定字段。

     ```sql
     select fieldname1, fieldname2 from tablename
     ```

  3. 包含查询条件

     ```sql
     select fieldname1, fieldname2 from tablename where...(查询条件)
     ```

  4. 补充

     

- #### 获取数据库中所有表名

  注：此处，tablename非上述参数，使用时不改动。

  ```SQL
  select tablename from pg_tables where schemaname='public'
  ```

- 

- #### 数组相关

  - **Array 操作符**

  | 操作符 | 描述             | 例子                                       | 结果                        |
  | :----- | :--------------- | :----------------------------------------- | :-------------------------- |
  | `=`    | 等于             | `ARRAY[1.1,2.1,3.1]::int[] = ARRAY[1,2,3]` | `t`                         |
  | `<>`   | 不等于           | `ARRAY[1,2,3] <> ARRAY[1,2,4]`             | `t`                         |
  | `<`    | 小于             | `ARRAY[1,2,3] < ARRAY[1,2,4]`              | `t`                         |
  | `>`    | 大于             | `ARRAY[1,4,3] > ARRAY[1,2,4]`              | `t`                         |
  | `<=`   | 小于或等于       | `ARRAY[1,2,3] <= ARRAY[1,2,3]`             | `t`                         |
  | `>=`   | 大于或等于       | `ARRAY[1,4,3] >= ARRAY[1,4,3]`             | `t`                         |
  | `@>`   | 包含             | `ARRAY[1,4,3] @> ARRAY[3,1]`               | `t`                         |
  | `<@`   | 被包含于         | `ARRAY[2,7] <@ ARRAY[1,7,4,2,6]`           | `t`                         |
  | `&&`   | 重叠(有共同元素) | `ARRAY[1,4,3] && ARRAY[2,1]`               | `t`                         |
  | `||`   | 数组与数组连接   | `ARRAY[1,2,3] || ARRAY[4,5,6]`             | `{1,2,3,4,5,6}`             |
  | `||`   | 数组与数组连接   | `ARRAY[1,2,3] || ARRAY[[4,5,6],[7,8,9]]`   | `{{1,2,3},{4,5,6},{7,8,9}}` |
  | `||`   | 元素与数组连接   | `3 || ARRAY[4,5,6]`                        | `{3,4,5,6}`                 |
  | `||`   | 数组与元素连接   | `ARRAY[4,5,6] || 7`                        | `{4,5,6,7}`                 |

  - **Array 函数**

  | 函数                                            | 返回类型                               | 描述                                                         | 例子                                                 | 结果                                 |
  | :---------------------------------------------- | :------------------------------------- | :----------------------------------------------------------- | ---------------------------------------------------- | :----------------------------------- |
  | `array_append(anyarray,anyelement)`             | `anyarray`                             | 向数组末尾添加元素                                           | `array_append(ARRAY[1,2], 3)`                        | `{1,2,3}`                            |
  | `array_cat(anyarray,anyarray)`                  | `anyarray`                             | 连接两个数组                                                 | `array_cat(ARRAY[1,2,3], ARRAY[4,5])`                | `{1,2,3,4,5}`                        |
  | `array_ndims(anyarray)`                         | `int`                                  | 返回数组的维数                                               | `array_ndims(ARRAY[[1,2,3], [4,5,6]])`               | `2`                                  |
  | `array_dims(anyarray)`                          | `text`                                 | 返回数组维数的文本表示                                       | `array_dims(ARRAY[[1,2,3], [4,5,6]])`                | `[1:2][1:3]`                         |
  | `array_fill(anyelement,int[], [,int[]])`        | `anyarray`                             | 返回数组初始化提供的值和维度，可选下界不是1                  | `array_fill(7, ARRAY[3], ARRAY[2])`                  | `[2:4]={7,7,7}`                      |
  | `array_length(anyarray,int)`                    | `int`                                  | 返回数组维度的长度                                           | `array_length(array[1,2,3], 1)`                      | `3`                                  |
  | `array_lower(anyarray, int)`                    | `int`                                  | 返回数组维数的下界                                           | `array_lower('[0:2]={1,2,3}'::int[], 1)`             | `0`                                  |
  | `array_prepend(anyelement,anyarray)`            | `anyarray`                             | 向数组开头添加元素                                           | `array_prepend(1, ARRAY[2,3])`                       | `{1,2,3}`                            |
  | `array_remove(anyarray,anyelement)`             | `anyarray`                             | 从数组中删除所有等于给定值的元素（数组必须是一维的）         | `array_remove(ARRAY[1,2,3,2], 2)`                    | `{1,3}`                              |
  | `array_replace(anyarray,anyelement,anyelement)` | `anyarray`                             | 用新值替换每个等于给定值的数组元素                           | `array_replace(ARRAY[1,2,5,4], 5, 3)`                | `{1,2,3,4}`                          |
  | `array_to_string(anyarray,text [, text])`       | `text`                                 | 使用分隔符和null字符串连接数组元素                           | `array_to_string(ARRAY[1, 2, 3, NULL, 5], ',', '*')` | `1,2,3,*,5`                          |
  | `array_upper(anyarray, int)`                    | `int`                                  | 返回数组维数的上界                                           | `array_upper(ARRAY[1,8,3,7], 1)`                     | `4`                                  |
  | `cardinality(anyarray)`                         | `int`                                  | 返回数组中的总元素数量，或者如果数组是空的则为0              | `cardinality(ARRAY[[1,2],[3,4]])`                    | `4`                                  |
  | `string_to_array(text, text[, text])`           | `text[]`                               | 使用指定的分隔符和null字符串把字符串分裂成数组元素           | `string_to_array('xx~^~yy~^~zz', '~^~', 'yy')`       | `{xx,NULL,zz}`                       |
  | `unnest(anyarray)`                              | `setof anyelement`                     | 扩大一个数组为一组行                                         | `unnest(ARRAY[1,2])`                                 | `1 2`(2 rows)                        |
  | `unnest(anyarray, anyarray[, ...])`             | `setof anyelement, anyelement [, ...]` | 扩展多个数组（可能是不同的类型）到一组行。 仅在FROM子句中允许这样做 | `unnest(ARRAY[1,2],ARRAY['foo','bar','baz'])`        | `1    foo 2    bar NULL baz`(3 rows) |

- 

