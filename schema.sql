-- Create DB (choose ONE name and use it consistently)
CREATE DATABASE dbms_project;
USE dbms_project;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name  VARCHAR(50),
  last_name   VARCHAR(50),
  phone_no    VARCHAR(20),
  email       VARCHAR(100),
  address     VARCHAR(100)
);

CREATE TABLE branch (
  branch_id   INT PRIMARY KEY AUTO_INCREMENT,
  branch_name VARCHAR(100),
  phone_no    VARCHAR(20),
  address     VARCHAR(100)
);

CREATE TABLE accounts (
  account_id  INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT,
  branch_id   INT,
  balance     DECIMAL(10,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (branch_id)   REFERENCES branch(branch_id)
);

CREATE TABLE Transactions (
  transaction_id   INT PRIMARY KEY AUTO_INCREMENT,
  account_id       INT,
  transaction_type ENUM('withdraw','deposit'),
  amount           DECIMAL(10,2),
  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE Loans (
  loan_id     INT PRIMARY KEY AUTO_INCREMENT,
  customer_id INT,
  loan_amount DECIMAL(10,2),
  loan_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
