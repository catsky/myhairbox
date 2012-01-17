import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')

cursor=conn.cursor()

cursor.execute("drop database if exists myhairbox")
cursor.execute("create database if not exists myhairbox")

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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;""")
#insert values

name = ""
tag = ""
avgPrice = ""
stars = ""
address = ""
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
for item in f:
    #eval to the real dict
    item = item.decode("unicode_escape")
    item =  eval(item) 
    for key in item:
        print key
        if key == "name":
            name = item[key]
        elif key == "tag":
            tag = item[key]
        elif key == "avgPrice":
            avgPrice = item[key]
        elif key == "stars":
            stars = item[key]
        elif key == "address":
            address = item[key]
        elif key == "alias":
            alias = item[key]
        elif key == "details_info":
            details_info = item[key]
        elif key == "recommand_dressor":
            recommand_dressor = item[key]
        elif key == "service_time":
            service_time = item[key]
        elif key == "bus_info":
            bus_info = item[key]
        elif key == "price_info":
            price_info = item[key]
        elif key == "comments":
            comments = item[key]
        elif key == "comments_count":
            comments_count = int(item[key])
        elif key == "link":
            link = item[key]
    value=[name,tag,avgPrice,stars,address,alias,details_info,
            recommand_dressor,service_time,bus_info,price_info,
            comments,comments_count,link]
    print value
    cursor.execute("""insert into dianping(name,tag,avgPrice,stars,address,alias,
        details_info,recommand_dressor,service_time,bus_info,price_info,comments,
        comments_count,link) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""", value)

cursor.close()
