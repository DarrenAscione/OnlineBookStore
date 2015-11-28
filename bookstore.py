import MySQLdb as mdb
import datetime

# con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
# #sql = "INSERT INTO Book VALUES('isbn3','book3','Anvi','sutd','Business',2011,85,'hardcover',1,'Management')"

# with con:
# 	cur = con.cursor()
# 	cur.execute(sql)
	# cur.executemany(
 #      """INSERT INTO Book (ISBN, title, author, publisher, keywords,year_of_publication,price,format,num_of_copies,subject)
 #      VALUES (%s, %s, %s, %s, %s, %d, %d, %s, %d, %s)""",
 #      [
 #      ("isbn1","book1","Wen Wen","sutd","Science",2013,80,"hardcover",2,"Biology"),
 #      ("isbn2","book2","Darren","sutd","Engineering",2012,100,"softcover",1,"Computational Structures" ),
 #      ("isbn3","book3","Anvi","sutd","Business",2011,100,"hardcover",3,"Management" )
 #      ] )



	# cur.execute("CREATE TABLE Book (ISBN varchar(20),\
	# 	title varchar(50) NOT NULL,\
	# 	author varchar(50),\
	# 	publisher varchar(20),\
	# 	keywords varchar(50),\
	# 	year_of_publication integer,\
	# 	price double,\
	# 	format varchar(10),\
	# 	num_of_copies integer,\
	# 	subject varchar(20),\
	# 	PRIMARY KEY(ISBN),\
	# 	CHECK (format = 'hardcover' or format = 'softcover'));")

	# cur.execute("CREATE TABLE Customer(login_name varchar(20),\
	# 	password varchar(20) NOT NULL,\
	# 	full_name varchar(30) NOT NULL,\
	# 	phone_num integer,\
	# 	address varchar(50),\
	# 	card_num integer,\
	# 	PRIMARY KEY(login_name)) ")


	# cur.execute("CREATE TABLE Feedback(customer_id varchar(20) references Customer(login_name),\
	# 	book_id varchar(20) references Book(ISBN),\
	# 	score integer,\
	# 	short_text varchar(100),\
	# 	feedback_date varchar(20) NOT NULL,\
	# 	PRIMARY KEY(customer_id,book_id))")
	# CHECK (score >= 1 and score <= 10)


	# cur.execute("CREATE TABLE OrderBook(customer_id varchar(20) references Customer(login_name),\
	# 	order_id integer unsigned auto_increment, \
	# 	book_id varchar(20) references Book(ISBN),\
	# 	order_date varchar(20) NOT NULL,\
	# 	order_status varchar(20),\
	# 	PRIMARY KEY(order_id))")

	# cur.execute("CREATE TABLE Rating(customer_id varchar(20) references customer(login_name),\
	# 	rater_id varchar(20) references Customer(login_name),\
	# 	book_id varchar(20) references Book(ISBN),\
	# 	rate integer,\
	# 	PRIMARY KEY (customer_id, rater_id, book_id))")

	# CHECK (rate <= 2 and rate >=0),\
	# CHECK (customer_id != rater_id))
	# cur.execute("alter table OrderBook auto_increment=1")
	# sql3="UPDATE book set num_of_copies='%d' where ISBN='%s'"%(5,'978-0470624708')
	# cur.execute(sql3)

def registration(login_name, password, full_name, phone_num, address, card_num):
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
		sql = "INSERT INTO Customer VALUES('%s','%s','%s','%d','%s','%d')" %\
		(login_name, password,full_name, phone_num, address, card_num)

		with con:
			cur = con.cursor()
			cur.execute(sql)
			print "Successful"
	except:
		print "Unsuccessful"

#registration("Anvi","1000459","Anvitha",892438157,"sutd",1000459)

def order(login_name, book_id, num_copy):
	
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")

		with con:
			cursor = con.cursor()
			sql = "SELECT num_of_copies from Book where ISBN = '%s'"%(book_id)
			cursor.execute(sql)
			original_copies = cursor.fetchone()[0]		
			if cursor.rowcount ==0 or original_copies < num_copy:
				#Book does not exist
				return "Unsuccessful \n Available Copies: %d"%(cursor.fetchone()[0])
			else:
				order_status='true'
				now=datetime.datetime.now()
				date="%s/%s/%s" % (now.day, now.month, now.year) 
				for i in xrange(num_copy):
					sql2 = "INSERT INTO OrderBook (customer_id,book_id,order_date,order_status) values ('%s','%s','%s','%s')"%(login_name,book_id,date,order_status)
					cursor.execute(sql2)
				sql3="UPDATE book set num_of_copies='%d' where ISBN='%s'"%(original_copies-num_copy,book_id)
				cursor.execute(sql3)
				print "Successful!!"
	except:
		print "Connection timeout"

#order("Anvi","978-0471134473",1)

def user_record(login_name):
	data={}
	
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
		
		with con:
			cursor = con.cursor()
			sql = "SELECT s1.full_name, s1.phone_num, s1.address, s1.card_num from Customer s1\
		 	where s1.login_name = '%s'"%(login_name)
			cursor.execute(sql)
			data[0]= cursor.fetchone()

			sql2 = "SELECT o1.book_id, o1.order_date, o1.order_status from OrderBook o1\
					where o1.customer_id = '%s'"%(login_name)
			cursor.execute(sql2)
			data[1]=cursor.fetchall()

			sql3 = "SELECT f1.book_id, f1.score, f1.short_text, f1.feedback_date from Feedback f1\
					where f1.customer_id = '%s'"%(login_name)
			cursor.execute(sql3)
			data[2] =cursor.fetchall()
			sql4 = "SELECT r1.rater_id, r1.book_id, r1.rate from Rating r1\
					where r1.customer_id = '%s'"%(login_name)
			cursor.execute(sql4)
			data[3]=cursor.fetchall()
			print data
	except:
		print "Unsuccessful"

#user_record('chenww')
def new_book(book_id, book_title, book_author, book_publisher, 
	book_kywrd, book_year, book_price, book_format, book_num_copy,
	book_subject):
	try:
		if book_format is "hardcover" or book_format is "softcover":
			con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
			with con:
				cursor = con.cursor()
				sql = "INSERT INTO Book VALUES ('%s','%s','%s','%s','%s','%d','%f','%s','%d','%s')"%\
						(book_id, book_title, book_author, book_publisher, 
						book_kywrd, book_year, book_price, book_format, book_num_copy,
						book_subject)
				cursor.execute(sql)
				print "Successful"
		else:
			return 'Invalid Format'
	except:
		print "Unsuccessful"
#new_book('978-0471134473','Basic Physics: A Self-Teaching Guide','Karl F. Kuhn','Wiley','Physics',1996,12.50,'hardcover',3,'Physics')
def copy_arrival(book_id, new_copies):
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
		with con:
			cursor = con.cursor()
			sql = "SELECT num_of_copies from Book where ISBN = '%s'"%(book_id)
			cursor.execute(sql)
			original_copies = cursor.fetchone()[0]	

			sql1 = "UPDATE Book set num_of_copies= '%d' where ISBN = '%s'"%(original_copies+new_copies,book_id)
			cursor.execute(sql1)

			print "Successful"
	except:
		return "Unsuccessful"
#copy_arrival('978-0471134473',2)

def feedback_record(login_name, book_id, rating, descript):
	if rating > 10 or rating < 1:
		return "Invalid Rating"
	else:
		try:
			con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
			with con:
				cursor = con.cursor()
				now=datetime.datetime.now()
				date="%s/%s/%s" % (now.day, now.month, now.year) 
				sql = "INSERT INTO Feedback VALUES ('%s','%s','%d','%s','%s')"%\
				(login_name, book_id, rating, descript,date)
				cursor.execute(sql)

				print "Successful"
		except:
			return "Unsuccessful"
#feedback_record('Anvi','978-0471134473',2,'sucks')

# Refreshes the feedback table(double check)
def refresh_feedback():
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")

		with con:
			cursor = con.cursor()
			sql = "SELECT f1.*, r1.rate from Feedback f1, Rating r1\
			where f1.customer_id = r1.rater_id and\
			f1.book_id = r1.book_id"
			cursor.execute(sql)
			print cursor.fetchall()
	except:
		return "Unsuccessful"

#refresh_feedback()

def usefullness(login_name, rater_name, book, rates):
	try:
		if rates > 2 or rates < 0 or login_name == rater_name:
			return "Invalid Input"
		else:
			con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
			sql = "INSERT INTO Rating VALUES ('%s','%s','%s','%d')"%\
			(login_name, rater_name, book, rates)

			with con:
				cursor = con.cursor()
				cursor.execute(sql)
				print "Successful"
				## Please refresh on your own!!
	except:
		return "Unsuccessful"
#usefullness('chenww', 'Anvi', '978-0471134473', 2)

def book_browsing(sort,search_author="",search_publisher="",search_title="",search_subject=""):
	search_author = "%" + search_author + "%"
	search_publisher = "%" + search_publisher + "%"
	search_title = "%" + search_title + "%"
	search_subject = "%"+ search_subject + "%"
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")
		if sort==1:
			sql = "SELECT * from Book where title LIKE '%s' and author LIKE '%s' and publisher LIKE '%s' and subject LIKE '%s' order by year_of_publication" %\
			(search_title,search_author,search_publisher,search_subject)
	
		else:
			sql ="SELECT b1.* from Book b1 join Feedback where b1.title LIKE '%s' and b1.author LIKE '%s' and b1.publisher LIKE'%s' and b1.subject LIKE '%s' \
			group by b1.ISBN order by AVG(score)"%\
			(search_title,search_author,search_publisher,search_subject)
        
		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			print cursor.fetchall()
	except:
		return "Unsuccessful"
#book_browsing(sort=2,search_author='Thomas')

def useful_feedback(book, n):
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")

		sql = "SELECT f1.* from Feedback f1 JOIN (SELECT r1.customer_id, r1.book_id, avg(r1.rate) as average from Rating r1 \
			group by r1.book_id, r1.customer_id\
			having book_id = '%s') as temp order by temp.average desc"%(book)
		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			print 'here'
			if n > cursor.rowcount:
				print cursor.fetchall()[:cursor.rowcount]
			else:
				print cursor.fetchall()[:n]
	except:
		return "Unsuccessful"
#useful_feedback('978-0471134473',1)

def book_recommendation(login_name, book):
	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")

		sql = "SELECT book_id, count(*) as num from OrderBook where customer_id in \
		(SELECT customer_id from OrderBook where book_id = '%s' and customer_id != '%s')\
		and book_id != '%s'\
		group by book_id order by num desc"%(book,login_name,book)
		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			print cursor.fetchall()
	except:
		return "Unsuccessful"

#book_recommendation('chenww','978-0470624708')

def statistics(m):
	data = {}

	try:
		con = mdb.connect(host="localhost",port=3306,user='root',passwd="database",db="bookstore")

		with con:
			cursor = con.cursor()
			now=datetime.datetime.now()
			date="%"+ "%s/%s" % (now.month, now.year) 

			sql = "SELECT book_id, count(*) as num from OrderBook where order_date like '%s'  group by book_id\
				order by num desc"%(date)
			
			cursor.execute(sql)

			data[0]=cursor.fetchall()[:m]

			sql2 = "SELECT b1.author, count(*) as num from Book b1, OrderBook o1 where b1.ISBN = o1.book_id\
					and order_date like '%s'\
					group by b1.author order by num desc"%(date)
			
			cursor.execute(sql2)
			data[1]=cursor.fetchall()[:m]

			sql3 = "SELECT b1.publisher, count(*) as num from Book b1, OrderBook o1 where b1.ISBN = o1.book_id\
					and order_date like '%s'\
					group by b1.publisher order by num desc"%(date)
			
			cursor.execute(sql3)
			data[2]=cursor.fetchall()[:m]
			print data
	except:
		return "Unsuccessful"
#statistics(2)











