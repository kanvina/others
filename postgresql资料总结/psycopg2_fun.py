'''
create by WYD
根据需求，PostgreSQL相关的所有函数汇总。
PS：持续更新。
'''

'''
"database": "amap_2019q1_wgds_0528",
"user": "postgres",
"password": "wayzpg@1234",
"host": "172.3.0.107",
"port": "5432"
'''

import psycopg2 #导入psycopg2库进行数据库操作。
import numpy as np
import pandas as pd
import datetime

def RunSQL(database_conn,SQL):
    # 传入参数 数据库名 用户名 用户密码 主机地址 端口
    conn = psycopg2.connect(database=database_conn['databasename'], user=database_conn['user'], password=database_conn['password'],
                            host=database_conn['host'], port=database_conn['port'])
    cur = conn.cursor()  # 建立操作游标
    cur.execute(SQL)# 传入的参数是 SQL 建表语句
    records = cur.fetchall()
    conn.commit()  # 注意，只有commit一下才会生效
    conn.close()
    return records

def RunSQL_withoutValue(database_conn,SQL):
    # 传入参数 数据库名 用户名 用户密码 主机地址 端口
    conn = psycopg2.connect(database=database_conn['databasename'], user=database_conn['user'], password=database_conn['password'],
                            host=database_conn['host'], port=database_conn['port'])
    cur = conn.cursor()  # 建立操作游标
    cur.execute(SQL)# 传入的参数是 SQL 建表语句
    conn.commit()  # 注意，只有commit一下才会生效
    conn.close()

def get_excel(code_name_xls):
    data_excel=np.array(pd.read_excel(code_name_xls))
    return data_excel

'''
获取制定表的结构
返回值为：字段名 字段类型
'''
def get_DB_Field_Type(database_conn,tablename):
    SQL_FieldName="SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull " \
                  "FROM pg_class as c,pg_attribute as a where c.relname = '{0}' and a.attrelid = c.oid and a.attnum>0".format(tablename)
    DB_filed=RunSQL(database_conn, SQL_FieldName)
    DB_filed=np.array(DB_filed)
    DB_filed_name=DB_filed[:,2]
    DB_filed_Type=DB_filed[:,1]
    DB_filed=np.concatenate((np.array([DB_filed_name]).transpose(),np.array([DB_filed_Type]).transpose()),axis=1)
    DB_field_list=[]
    DB_Type_list=[]
    for i in DB_filed:
        DB_field_list.append(i[0])
        DB_Type_list.append(i[1])
    return DB_field_list,DB_Type_list

def get_SQL_create_fromXLS(Field_Type_XLS,tablename):
    name_Type = pd.read_excel(Field_Type_XLS)
    name_Type = np.array(name_Type)
    text = ''
    for i in range(len(name_Type)):
        if i != len(name_Type) - 1:
            text = text + '{0} {1},'.format(name_Type[i, 0], name_Type[i, 1])
        else:
            text = text + '{0} {1}'.format(name_Type[i, 0], name_Type[i, 1])
    SQL_create_fromXLS = "CREATE TABLE {0} ({1}); ".format(tablename, text)
    return SQL_create_fromXLS

'''
在已经建立好的数据库中逐条导入数据库，无指定字段。
'''
def XLS2DB(dataXLS,database_conn,tablename):
    data=np.array(pd.read_excel(dataXLS))
    num_col=data.shape[1]
    num_row=data.shape[0]
    text_insert = ''
    for i in range(num_row):

        for n in range(num_col):

            if n ==0:
                text_insert = text_insert+"\'"+str(data[i,n])+'\''

            else:

                text_insert=text_insert+','+'\''+str(data[i,n])+'\''

        SQL_insert="INSERT INTO {0} VALUES ({1});".format(tablename,text_insert)
        RunSQL_withoutValue(database_conn,SQL_insert)
        text_insert=''
        print("第 {0} 条数据导入成功".format(i+1))

def get_batch(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i: i + size]

def update_by_batch(database_conn,tablename,update_list, keyword,update_field,batch_size):
    conn = psycopg2.connect(database=database_conn['databasename'], user=database_conn['user'], password=database_conn['password'],
                            host=database_conn['host'], port=database_conn['port'])
    print("开始更新")
    num=0
    num_all=len(update_list)
    print("共",num_all,"条数据待更新")

    for mini_batch in get_batch(update_list, batch_size):
        a=datetime.datetime.now()
        num=num+1
        qStr = "UPDATE {0} SET {1} = tmp.{2} FROM (VALUES ".format(str(tablename), str(update_field),str(update_field))
        qParams = []
        try:
            for r in mini_batch:
                try:
                    qStr += "(%s,%s),"
                    tag_name = r[1]
                    # if tag_name[0]=='nan':
                    #     tag_name = [None]
                    qParams.extend([int(r[0]),tag_name])#因为tag_names类型为字符串数组 所以为[tag_name]
                    # qParams.extend([int(r[0]), str(tag_name)])#若更新字段为字符串，改为此行代码

                except OSError:
                    print("第",num,"批次，第",r,'条数据出现问题')
                    print(int(r[0]))
                    print(tag_name)
                    pass
                continue

            qStr = qStr[:-1]
            qStr += " ) AS tmp({4},{0}) WHERE tmp.{1} = {2}.{3}".format(str(update_field),str(keyword),str(tablename),str(keyword),str(keyword))
            cur = conn.cursor()
            cur.execute(qStr,qParams)
            conn.commit()

            ratio_text = int((num * batch_size * 100) / num_all)
            b = datetime.datetime.now()
            c = (b - a).seconds
            if num_all - (num - 1) * batch_size >= batch_size:
                print(ratio_text, '%数据更新完成,本更新批次数量为:', batch_size, '条，耗时：', int(c), '秒')
            else:
                print(100, '%数据更新完成,本更新批次数量为:', num_all - (num - 1) * batch_size, '条，耗时：', int(c), '秒')


        except OSError:
            print("更新至第",num,"批次出现错误")
            print(int(r[0]))
            print([tag_name])
            pass
        continue
    conn.close()




if __name__=='__main__':

    my_test={
        'databasename':'my_test',
        'user':'postgres',
        'password':'123456',
        'host':'localhost',
        'port': '5432',
    }









