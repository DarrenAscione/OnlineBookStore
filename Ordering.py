import MySQLdb as mdb


def registration(login_name, password, full_name, phone_num, address, card_num):
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		sql = "INSERT INTO Customer VALUES('%s','%s', '%d','%s','%s', '%d')" %\
			(login_name, password, full_name, phone_num, address, card_num)
		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			return "Successful"
	except:
		return "Unsuccessful"

def order(login_name, book_id, num_copy):
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")

		sql = "SELECT num_of_copies from Book where ISBN = book_id"

		with con:
			cursor = con.cursor()
			sql = "SELECT num_of_copies from Book where ISBN = book_id"
			cursor.execute(sql)
			if cursor.rowcount==0 or cursor.fetchone()[0] < num_copy:
				#Book does not exist
				return "Unsuccessful \n Available Copies: %d"%(cursor.fetchone()[0])
			else:
				sql2 = "INSERT INTO OrderBook values ('%s', '%s')"%(login_name,book_id)
				for i in xrange(num_copy):
					cursor.execute(sql2)
				return "Successful!!"
	except:
		return "Connection timeout"

def user_record(login_name):
	data = {}
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		sql = "SELECT s1.full_name, s1.phone_num, s1.address, s1.card_num from Customer s1\
				where s1.login_name = login_name"
		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			data[0].append(cursor.fetchone())
			sql2 = "SELECT o1.book_id, o1.order_date, o1.order_status from OrderBook o1\
					where o1.customer_id = login_name"
			cursor.execute(sql2)
			data[1].append(cursor.fetchall())
			sql3 = "SELECT f1.book_id, f1.score, f1.short_text, f1.feedback_date from Feedback f1\
					where f1.customer_id = login_name"
			cursor.execute(sql3)
			data[2].append(cursor.fetchall())
			sql4 = "SELECT r1.rater_id, r1.book_id, r1.rate from Rating r1\
					where r1.customer_id = login_name"
			cursor.execute(sql4)
			data[3].append(cursor.fetchall())
			return data
	except:
		return "Unsuccessful"

def new_book(book_id, book_title, book_author, book_publisher, 
	book_kywrd, book_year, book_price, book_format, book_num_copy,
	book_subject):
	try:
		if book_format != "hardcover" or book_format != "softcover":
			return "Invalid format"	
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		with con:
			cursor = con.cursor()
			sql = "INSERT INTO Book VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%\
					(book_id, book_title, book_author, book_publisher, 
					book_kywrd, book_year, book_price, book_format, book_num_copy,
					book_subject)
			cursor.execute(sql)
			return "Successful"
	except:
		return "Unsuccessful"


def copy_arrival(book_id, num_of_copies):
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		sql = "UPDATE num_of_copies from Book where ISBN = book_id"
		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			return "Successful"
	except:
		return "Unsuccessful"

def feedback_record(login_name, book_id, rating, descript):
	if rating > 10 or rating < 1:
		return "Invalid Rating"
	else:
		try:
			con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
			sql = "INSERT INTO Feedback VALUES ('%s','%s','%d','%s')"%\
			(login_name, book_id, rating, descript)
			with con:
				cursor = con.cursor()
				cursor.execute(sql)
				return "Successful"
		except:
			return "Unsuccessful"

# Refreshes the feedback table
def refresh_feedback():
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")

		sql = "SELECT f1.*, r1.rate from Feedback f1, Rating r1\
		where f1.customer_id = r1.customer_id and\
		f1.book_id = r1.book_id"

		with con:
			cursor = con.cursor()
			cursor.execute(sql)
			return cursor.fetchall()
	except:
		return "Unsuccessful"

def usefullness(login_name, rater_name, book, rates):
	try:
		if rates > 2 or rates < 0 or login_name == rater_name:
			return "Invalid Input"
		else:
			con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
			sql = "INSERT INTO Rating VALUES ('%s','%s','%s','%d')"%\
			(login_name, rater_name, book, rates)

			with con:
				cursor = con.cursor()
				cursor.execute(sql)
				return "Successful"
				## Please refresh on your own!!
	except:
		return "Unsuccessful"

#def book_browsing():

def useful_feedback(book, n):
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		sql = "SELECT f1.* from Feedback f1 JOIN (SELECT r1.customer_id, r1.book_id, avg(r1.rating) as average from Rating r1 \
			group by r1.book_id, r1.customer_id\
			having book_id = book) as temp order by temp.average desc"
		with con:
			cursor = con.cursor
			cursor.execute(sql)
			if n > cursor.rowcount:
				return cursor.fetchall()[:cursor.rowcount]
			else:
				return cursor.fetchall()[:n]
	except:
		return "Unsuccessful"

def book_recommendation(login_name, book):
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		sql = "SELECT book_id, count(*) as num from OrderBook where customer_id in \
		(SELECT customer_id from OrderBook where book_id = book and customer_id != 'login_name')\
		and book_id != book\
		group by book_id order by num desc"
		with con:
			cursor = con.cursor
			cursor.execute(sql)
			return cursor.fetchall()
	except:
		return "Unsuccessful"

def statistics(m, date):
	data = {}
	month = int(date[4:6])
	try:
		con = mdb.connect(host = "localhost", user = "root", passwd ="", db = "tutorial")
		with con:
			cursor = con.cursor
			sql = "SELECT book_id, count(*) as num from OrderBook where ____ currentmonth _____  group by book_id\
				order by num desc"
			cursor.execute(sql)
			data[0].append(cursor.fetchall()[:m])
			sql2 = "SELECT b1.author, count(*) as num from Book b1, OrderBook o1 where b1.ISBN = o1.book_id\
					and ____ currentmonth _____ \
					group by b1.author order by num desc"
			cursor.execute(sql2)
			data[1].append(cursor.fetchall()[:m])
			sql3 = "SELECT b1.publisher, count(*) as num from Book b1, OrderBook o1 where b1.ISBN = o1.book_id\
					and ____ currentmonth _____ \
					group by b1.publisher order by num desc"
			cursor.execute(sql3)
			data[2].append(cursor.fetchall()[:m])
			return data
	except:
		return "Unsuccessful"







