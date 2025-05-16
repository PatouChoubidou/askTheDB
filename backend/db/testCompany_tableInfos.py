tables_create_stmts = """

These SQL create table statements help you to understand all the tables of the database and the existing assiociated columns:

CREATE TABLE Contacts (
    contact_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    street TEXT NOT NULL,
    house_nr TEXT NOT NULL,
    country_code TEXT,
    city TEXT,
    country TEXT
);

CREATE TABLE Customers (
    customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email EXT UNIQUE NOT NULL,
    contact_id INTEGER,
    FOREIGN KEY (contact_id) 
        REFERENCES contacts (contact_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE Orders (
    order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_ID INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    total_amount REAL NOT NULL,
        FOREIGN KEY (customer_ID) REFERENCES Customers(customer_ID)
);

CREATE TABLE OrderDetails (
    order_detail_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    order_ID INTEGER NOT NULL,
    product_ID INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal REAL NOT NULL,
        FOREIGN KEY (order_ID) REFERENCES Orders(order_ID),
        FOREIGN KEY (product_ID) REFERENCES Products(product_ID)
 );

CREATE TABLE Products (
    product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company TEXT,
    description TEXT,
    image TEXT,
    price REAL,
    stock INTEGER,
    rating INTEGER,
    categorie INTEGER,
        FOREIGN KEY (categorie) REFERENCES Categories(categorie_ID)
);

CREATE TABLE Invoices (
    invoice_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_ID INTEGER,
    order_ID INTEGER NOT NULL,
    status TEXT,
        FOREIGN KEY (contact_ID) REFERENCES Contacts(contact_ID),
        FOREIGN KEY (order_ID) REFERENCES Orders(order_ID)
);

CREATE TABLE Employees (
    employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    position_ID INTEGER,
    contract_ID INTEGER NOT NULL,
         FOREIGN KEY (position_ID) REFERENCES Positions(position_ID),
         FOREIGN KEY (contract_ID) REFERENCES Contracts(contract_ID)
);

CREATE TABLE Contracts (
    contract_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    salary_year REAL,
    start_at TEXT,
    ends_at TEXT,
    created_at DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
);

CREATE TABLE Positions (
    position_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    departement TEXT,
    job_description TEXT,
    contact_ID INTEGER,
    created_at DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
        FOREIGN KEY (contact_ID) REFERENCES Contacts(contact_ID)  
);

CREATE TABLE Skills (
    skill_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skill_description TEXT
);

CREATE TABLE EmployeeSkills (
    employee_skill_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_ID INTEGER,
    skill_ID INTEGER ,
        FOREIGN KEY (skill_ID) REFERENCES Skills(skill_ID),
        FOREIGN KEY (employee_ID) REFERENCES Employees(employee_ID)  
);


CREATE TABLE Categories (
    categorie_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE Alpacas (
    alpaca_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hair_cut TEXT,
    hair_streak_color TEXT
);

CREATE TABLE Spits (
    spit_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    spit_consistence TEXT NOT NULL,
    spit_distance REAL,
    spit_hit_rate REAL,
    alpaca_ID,
        FOREIGN KEY (alpaca_ID) REFERENCES Alpacas(alpaca_ID)
);

"""


