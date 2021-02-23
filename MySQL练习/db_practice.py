#! /usr/bin/env python3
#  query donor information by his number

import pymysql
def main():
    
    find_name=input('input donor number:  ')
    params=[int(find_name)]
    conn=pymysql.connect(host='localhost',port=3306,database='fairfax',user='root',password='dw072489',charset='utf8')

    csl=conn.cursor()
    count=csl.execute('SELECT height,weight,eye_color,hair_color FROM donor_look WHERE donor_num=%s',params)
    print(count)

    for i in range(count):
        result=csl.fetchone()
        print(result)

    conn.commit()
    csl.close()
    conn.close()

dbName=input('input the databse name you want to query:  ')
if dbName.lower()=='fairfax':
    main()

    
