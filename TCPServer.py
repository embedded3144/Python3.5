import socket
import time
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup


import pickle

#Open database connection
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mirero', db='Sensor',charset='utf8',autocommit=True)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")


# Fetch a single row using fetchone() method.


data = cursor.fetchone()

print ("Database version : %s " % data)

#현재 사용중인 DB
cursor.execute("SELECT DATABASE()")
print (cursor.fetchone())


cursor.execute("select * from mytable")
print (cursor.fetchone())






#db.close()


HOST='192.168.10.20' #호스트를 지정하지 않으면 가능한 모든 인터페이스를 의미한다.
PORT=56789 #포트지정
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1) #접속이 있을때까지 기다림
conn, addr=s.accept() #접속 승인
print('Connected by',addr)

count = 0
while True:
    try:
        time.sleep(1)
        data=conn.recv(1024)
        if not data:
            print("Empty Data")
            continue
        else:        
            conn.send(data) #받은 데이터를 그대로 클라이언트에 전송


            pickledata = pickle.loads(data)
            print(repr(pickledata))
            print('Received:',  pickledata[0])
     
            add_dataDB = ("INSERT INTO mytable VALUES(%s,%s,%s,%s,%s,%s,%s)")


            data_DB = (count,pickledata[0],pickledata[1],pickledata[2],'40','59','60')
            #data_DB = (count,pickledata,'2','30','40','59','60')
            cursor.execute(add_dataDB, data_DB)	    
    
            count=count+1
    except:
        print("Excetion!!!")
        conn.close()
	#db.close()
        break
