import MySQLdb as mdb

con = mdb.connect(host = "localhost", user = "root", passwd = "", db = "tutorial")

with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE Book (ISBN varchar(20),\
		title varchar(50) NOT NULL,\
		author varchar(50),\
		publisher varchar(20),\
		keywords varchar(50),\
		year_of_publication integer,\
		price double,\
		format varchar(10),\
		num_of_copies integer,\
		subject varchar(20),\
		PRIMARY KEY(ISBN),\
		CHECK (format = 'hardcover' or format = 'softcover'));")
	cur.execute("CREATE TABLE Customer(login_name varchar(20),\
		password varchar(20) NOT NULL,\
		full_name varchar(30) NOT NULL,\
		phone_num integer,\
		address varchar(50),\
		card_num integer,\
		PRIMARY KEY(login_name)) ")
	cur.execute("CREATE TABLE Order(customer_id varchar(20),\
		book_id varchar(20),order_date date NOT NULL,\
		order_status varchar(20),time timestamp,\
		PRIMARY KEY(customer_id,book_id,time),\
		FOREIGN KEY customer_id REFERENCES Customer(login_name),\
		FOREIGN KEY book_id REFERENCES Book(ISBN))")
	cur.execute("CREATE TABLE Feedback(customer_id varchar(20),\
		book_id varchar(20),\
		score integer,\
		short_text varchar(100),\
		PRIMARY KEY(customer_id,book_id),\
		FOREIGN KEY customer_id REFERENCES Customer(login_name),\
		FOREIGN KEY book_id REFERENCES Book(ISBN),\
		CHECK (score >= 1 and score <= 10))")
	cur.execute("CREATE TABLE Rating(customer_id varchar(20),\
		rater_id varchar(20),\
		book_id varchar(20),\
		rate integer,\
		PRIMARY KEY (customer_id, rater_id, book_id),\
		FOREIGN KEY customer_id references customer(login_name),\
		FOREIGN KEY rater_id references customer(login_name),\
		FOREIGN KEY book_id references Book(ISBN),\
		CHECK (rate <= 2 and rate >=0),\
		CHECK (customer_id != rater_id))")


