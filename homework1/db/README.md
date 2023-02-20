# Design a database for a ChatGPT app

## Tasks:
Imagine that you are building a ChatGPT app that allows users to ask questions and receive answers from the app.

1. Design a database using MySQL to store the questions and answers exchanged between users and the app.

2. Create a table for the questions with the following fields: id (Primary Key, Auto Increment), user_id (Foreign Key referencing the Users table), question, and timestamp.

3. Create a table for the answers with the following fields: id (Primary Key, Auto Increment), question_id (Foreign Key referencing the Questions table), answer, and timestamp.

4. Create a table for the users, with the following fields: id (Primary Key, Auto Increment), username, password, and email.

## Answer:
TODO: you need to add your sql query to each task here.
create database chatgpt;
use chatgpt;
create table users (username VARCHAR(100),password VARCHAR(100),email VARCHAR(100));
use chatgpt;
create table chat_table(chat_column LONGTEXT);
此外我还使用了DataGrip对数据库进行了一些操作。

