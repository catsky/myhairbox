# -*- coding: utf-8 -*-
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


conn = MySQLdb.connect(host='localhost', user='root', passwd='1234',charset="utf8")

cursor=conn.cursor()

cursor.execute("drop database if exists myhairbox")
cursor.execute("create database if not exists myhairbox DEFAULT CHARSET=utf8")

conn.select_db('myhairbox')
cursor.execute("""CREATE TABLE IF NOT EXISTS `dianping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 NOT NULL,
  `tag` varchar(100) CHARACTER SET utf8 NOT NULL,
  `avgPrice` varchar(20) CHARACTER SET utf8 NOT NULL,
  `stars` varchar(20) CHARACTER SET utf8 NOT NULL,
  `address` varchar(100) CHARACTER SET utf8 NOT NULL,
  `contact` varchar(50) CHARACTER SET utf8 NOT NULL,
  `alias` varchar(20) CHARACTER SET utf8 NOT NULL,
  `details_info` varchar(500) CHARACTER SET utf8 NOT NULL,
  `recommand_dressor` varchar(100) CHARACTER SET utf8 NOT NULL,
  `service_time` varchar(50) CHARACTER SET utf8 NOT NULL,
  `bus_info` varchar(50) CHARACTER SET utf8 NOT NULL,
  `price_info` varchar(50) CHARACTER SET utf8 NOT NULL,
  `comments` mediumtext CHARACTER SET utf8 NOT NULL,
  `comments_count` varchar(20) CHARACTER SET utf8 NOT NULL,
  `link` varchar(100) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;""")
#insert values

name = ""
tag = ""
avgPrice = ""
stars = ""
address = ""
contact = ""
alias = ""
details_info = ""
recommand_dressor = ""
service_time = ""
bus_info = ""
price_info = ""
comments = ""
comments_count = ""
link = ""
        
            
            
f=file("items.json")
#out=file("items_out.json","w+")
results = []
count = 1
for item in f:
    print "processing %s line"%count
    count += 1
    #eval to the real dict
    item = item.decode("unicode_escape")
    
    #print "item:ken: %s"%item

    item =  eval(item) 
    for key in item:
        if key == "name":
            name = ','.join(item[key])
        elif key == "tag":
            tag = ','.join(item[key])
        elif key == "avgPrice":
            avgPrice = item[key]
        elif key == "stars":
            stars = ','.join(item[key])
        elif key == "address":
            address = ''.join(item[key])
        elif key == "alias":
            alias = ''.join(item[key])
        elif key == "details_info":
            details_info = ''.join(item[key])
        elif key == "recommand_dressor":
            recommand_dressor = ','.join(item[key])
        elif key == "service_time":
            service_time = ''.join(item[key])
        elif key == "bus_info":
            bus_info = ''.join(item[key])
        elif key == "price_info":
            price_info = ''.join(item[key])
        elif key == "comments":
            comm = ''
            for s in item[key]:
                comm += ''.join(s)
            comments = comm
            #comments = ''.join(str(item[key]).decode("utf-8"))
        elif key == "comments_count":
            comments_count = item[key]
        elif key == "link":
            link = item[key]
    value=[name,tag,avgPrice,stars,address,contact, alias,details_info,
            recommand_dressor,service_time,bus_info,price_info,
            comments,comments_count,link]
    cursor.execute("""insert into dianping(name,tag,avgPrice,stars,address,contact,alias,
        details_info,recommand_dressor,service_time,bus_info,price_info,comments,
        comments_count,link) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""", value)

cursor.close()
