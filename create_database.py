import sqlite3
import random
import datetime

create_sales_table = '''CREATE TABLE sales (
                        sale_id INTEGER PRIMARY KEY,
                        sale_date DATE,
                        customer_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        unit_price DECIMAL(10, 2),
                        total_price DECIMAL(10, 2),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                    )'''
                    
create_products_table = '''CREATE TABLE products (
                           product_id INTEGER PRIMARY KEY,
                           product_name TEXT,
                           unit_cost DECIMAL(10, 2) 
                        )'''
                        
create_customers_table = '''CREATE TABLE customers(
                            customer_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT,
                            phone TEXT
                        )'''
                        
insert_products_data = '''INSERT INTO products (product_name, unit_cost) VALUES (?,?)'''

insert_sales_data = '''INSERT INTO sales (sale_date, customer_id, product_id, quantity, unit_price, total_price) VALUES (?,?,?,?,?,?)'''

insert_customers_data = '''INSERT INTO customers (first_name, last_name, email, phone) VALUES (?,?,?,?)'''

products = [('Product A', 50.00), ('Product B', 25.00), ('Product C', 75.00), ('Product D', 40.00), ('Product D', 60.00)]

customers = [
    ('John', 'Doe', 'johndoe@email.com', '555-1234'),
    ('Jane', 'Doe', 'janedoe@email.com', '555-5678'),
    ('Bob', 'Smith', 'bobsmith@email.com', '555-9012'),
    ('Alice', 'Jones', 'alicejones@email.com', '555-3456'),
    ('David', 'Brown', 'davidbrown@email.com', '555-7890'),
    ('Emily', 'Davis', 'emilydavis@email.com', '515-1234'),
    ('Frank', 'Wilson', 'frankwilson@email.com', '515-5678'),
    ('Henry', 'Chen', 'henrychen@email.com', '515-9012'),
    ('Isabel', 'Garcia', 'isabelgarcia@email.com', '515-3456'),
]

start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)

with sqlite3.connect('sales.db') as con:
    con.execute(create_sales_table)
    con.execute(create_products_table)
    con.execute(create_customers_table)
    
    for product in products:
        con.execute(insert_products_data, product)
        
    for customer in customers:
        con.execute(insert_customers_data, customer)
    
    for i in range(1000):
        sale_date = start_date + datetime.timedelta(days=random.randint(0,364))
        customer_id = random.randint(1, len(customers))    
        product_id = random.randint(1, len(products))   
        quantity = random.randint(1, 10)
        unit_price = products[product_id-1][1]
        total_price = quantity * unit_price
        con.execute(insert_sales_data, (sale_date, customer_id, product_id, quantity, unit_price, total_price))
        
    con.commit()
    
    print('Database created!') 