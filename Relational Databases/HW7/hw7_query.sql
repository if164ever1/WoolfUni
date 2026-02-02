use mydb;

/*1. Write SQL query that extracts the year, month, and day from the date attribute for the orders table. 
Display them as three separate attributes alongside the id attribute and the original date attribute (resulting in total of 5 attributes).
*/
SELECT 
	id, date,
    YEAR(date) AS year,
    MONTH(date) AS month,
    DAY(date) AS day
FROM
	orders;
    
/*
2. Write SQL query that adds one day to the date attribute for the orders table. Display the id attribute, 
-he original date attr-ibute, and the result of the addition on the screen. 
*/
SELECT 
	id, date,
    DATE_ADD(date, INTERVAL 1 DAY) AS date_plus_one
FROM
	orders;


/*
3. Write a SQL query that displays the number of seconds since the epoch (timestamp value) for the date attribute in the orders table. 
To do this, find and apply the necessary function. 
Display the id attribute, the original date attribute, and the result of the function on the screen.
*/
SELECT 
	id, date,
    UNIX_TIMESTAMP(date) AS timestamp_value
FROM
	orders;

/*
4. Write a SQL query that counts how many rows
 the order table contains with date attribute falling between 1996-07-10 00:00:00 and 1996-10-08 00:00:00.
*/
SELECT COUNT(*) AS orders_count
FROM orders
WHERE date BETWEEN '1996-07-10 00:00:00' AND '1996-10-08 00:00:00';

/*
5. Write a SQL query that displays the id attribute ,  
the date attribute and JSON object {“id”: <row id attribute>, “date”: <row date attribute>} 
from the orders table. Use a function to create the JSON object.
*/
SELECT 
	id, date,
    JSON_OBJECT('id', id, 'date', date) AS json_data
FROM 
	orders;
