import sqlite3
import pandas as pd
import streamlit as st
from PIL import Image
def run(query):
    conn = sqlite3.connect("sakila.db")
    st.write(pd.read_sql(query,conn))
    conn.close()

def check_answer(df_user,df_solution,question):
    try:
        df_user_sorted = df_user.sort_values(by=list(df_user.columns)).reset_index(drop=True)
        df_solution_sorted = df_solution.sort_values(by=list(df_solution.columns)).reset_index(drop=True)
    except Exception:
        df_user_sorted = df_user.reset_index(drop=True)
        df_solution_sorted = df_solution.reset_index(drop=True)
    if df_user_sorted.equals(df_solution_sorted):
        st.success("You solved this question. Good job!")
        if st.checkbox("Mark as solved", key = "mark_as_solved"+question):
            pass
    else:
        st.error("Result doesn't match the expected output.")
    if st.toggle("See expected output", key = "see_solution"+question):
        st.dataframe(df_solution)

def get_table_names():
    conn = sqlite3.connect("sakila.db")
    tables = pd.read_sql("select name from sqlite_master where type = 'table';",conn)
    table_text = ""
    for i,j in zip(tables.index, tables.name):
        if j != "sakila":
            table_text += "`"+j+"`"
            if i != tables.index[-1]:
                table_text += " | "
    conn.close()
    return table_text

def get_output_df(query):
    conn = sqlite3.connect("sakila.db")
    return pd.read_sql_query(query, conn)

def get_formattings(df):
    colnames = ""
    for i in df.columns.tolist():
        colnames += "`"+i+"`"+", "
    colnames = colnames[:-2]
    rows = df.shape[0]
    return [colnames, rows]

@st.dialog("TEST WINDOW", width = "large")
def test_query():
    st.write("You can `run any query` here. Simply type the query, put a semicolon ` ; ` at the end of the query, and press `Ctrl + ENTER` to execute.")
    st.markdown("List of table names:")
    st.subheader(get_table_names)
    query = st.text_area("Write your query here:")
    if len(query) != 0:
        try:
            run(query)
        except Exception as e:
            st.error(f"❌ SQL Error: {e}")

def select_level():
    c0,c1,c0 = st.columns([.5,3,.5])
    with c1:
        st.markdown("<div style='text-align: center'><h4>Select Material Level</h4>", unsafe_allow_html=True)
        level = st.selectbox("", ["Basics - Quick Start","Medium - Confident at Work","Advanced - Deployment Ready"])
        c0,c3,c4 = st.columns([.1,1,1.5])
        with c3:
            st.write("")
            if level == "Basics - Quick Start":
                st.image("level_1.jpeg", width = 150)
            elif level == "Medium - Confident at Work":
                st.image("level_2.jpeg", width = 150)
            elif level == "Advanced - Deployment Ready":
                st.image("level_3.jpeg", width = 150)
        with c4:
            st.write("")
            if level == "Basics - Quick Start":
                options = ["1 - SELECT FROM", "2 - AS (alias)", "3 - WHERE", "4 - String Operations", "5 - ORDER BY", "6 - LIMIT", "7 - JOIN", "8 - More JOINs", "9 - Basic Functions", "10 - GROUP BY", "11 - HAVING", "`HOW TOUGH ARE YOU? (EASY)`"]
                desc = '''Whether you're new to SQL or just need a quick refresher before work/interview, this section is a perfect starting point. 
                Learn how to write simple queries, filter data, and get comfortable with essential commands like `SELECT`, `WHERE`, and `JOIN`.'''
            elif level == "Medium - Confident at Work":
                options = ["1 - CASE WHEN", "2 - SUBQUERY", "3 - CTE", "4 - CTE vs Subquery", "5 - Window: Row Numbering", "6 - Window: Running Totals", "7 - Window: Comparing Rows", "8 - PARTITION", "`HOW TOUGH ARE YOU? (MEDIUM)`"]
                desc = '''Boost your SQL skills with more advanced operations that are commonly used in real work scenarios. 
                Explore `CASE WHEN`, `Subqueries`, `CTE`, and various `window functions` to handle more complex data tasks with confidence.'''
            elif level == "Advanced - Deployment Ready":
                options = ["coming soon"]
                desc = '''Strengthen your SQL skills with practical challenges using databases from various fields of work.
                Get familiar and fluent with day-to-day problem-solving tasks and business questions, giving you a clear picture of
                what it's like to work in each area — and a boost in your confidence using SQL.'''
            st.write(desc)
        st.divider()
    c0,c1,c0 = st.columns([.5,3,.5])
    with c1:
        st.write("")
        st.markdown("**After finishing this part, you will:**")
        if level == "Basics - Quick Start":
            st.write("- understand the concept of `relational database` and how tables connect using keys (columns),")
            st.write("- get comfortable exploring and querying structured data,")
            st.write("- be able to handle basic data analysis tasks using SQL, and")
            st.write("- develop an analytical mindset for finding specific information and insights.")
        elif level == "Medium - Confident at Work":
            st.write("- be able to tackle more complex analysis using conditional logic and subqueries,")
            st.write("- get used to breaking down problems into manageable steps using `CTEs`,")
            st.write("- be fluent in comparing rows and tracking changes using window functions, and")
            st.write("- write clearer, more modular SQL that is easier to debug, document, and maintain")
        elif level == "Advanced - Deployment Ready":
            st.write("- gain experience solving real-world business problems across different domains,")
            st.write("- build fluency writing SQL for ad-hoc analysis and reporting,")
            st.write("- understand how to adapt queries to different database structure and needs,")
            st.write("- have more confidence diving straight into unfamiliar datasets, and")
            st.write("- be more prepared to face practical, job-like scenarios.")
        st.write("")

    return level, options

def selection_1_1():
    st.subheader("`SELECT ___ FROM ___;`")
    st.write("")
    st.write("The most basic, shortest query in SQL to run is")
    st.code("SELECT column_name FROM table_name;", language = "sql")
    st.write("It takes the selected column(s) from the selected table and displays it as a new table.")
    st.markdown("*Example:*")
    st.write("Running this query")
    st.code("SELECT * FROM actor;", language = "sql")
    st.write("will give you all columns from the table called `actor` (see list of tables on this page's header).")
    st.write("You can select multiple columns from one table. Like this")
    st.code("SELECT actor_id, first_name, last_name FROM actor;", language = "sql")
    st.markdown("- You can select only from **one table** at a time, unless you are **appending/joining** multiple tables.")
    st.markdown("- Don't forget to put a semicolon ( ; ) at the end of your query.")

def selection_1_2():
    st.subheader("`SELECT ___ AS ___ FROM ___;`")
    st.write("")
    st.write("You can rename the column you selected using `AS` after mentioning the column_name.")
    st.code("SELECT first_name AS 'First Name' FROM actor;")
    st.write("You can also rename multiple columns in one query.")
    st.code("SELECT first_name AS 'First Name', last_name AS 'Last Name' FROM actor;", language = "sql")
    st.write("This is called giving an alias to columns.")
    st.write("You can also give aliases to the table, but this time we don't need to use `AS`.")
    st.code("SELECT first_name as 'First Name' FROM actor a;", language = "sql")
    st.write("- This method only changes the column names in the output. It doesn't change the actual column names in the database.")

def selection_1_3():
    st.subheader("`SELECT ___ FROM ___ WHERE ___;`")
    st.write("")
    st.write("You can give conditions when selecting the data. One of the method of putting conditions is using `WHERE`.")
    st.code("SELECT title, rating FROM film WHERE rating != 'R';", language = "sql")
    st.write("In this example, it gives us all film titles while excluding the ones with rating 'R'.")
    st.write("You can also put numerical conditions, like this")
    st.code("SELECT * FROM film WHERE length >= 150;", language = "sql")
    st.write("It gives us details of all films that has length of or more than 150 minutes.")
    st.write("To check if a value has a certain word/character, you can use `LIKE`.")
    st.code("SELECT * FROM film_list WHERE title LIKE '%panther%';", language = "sql")
    st.write("The `%` sign at the start and end of the string means there can be any character/string before and after the string we are looking for.")
    st.write("You can also put multiple conditions in one query.")
    st.code('''SELECT title AS movie_title, price as rent_price 
FROM film_list 
WHERE category="Horror" AND price <1.99;''', language = "sql")
    st.markdown("- Notice that you can use **multiple lines** while writing your query.")
    st.write("In fact, it makes it easier for us (and other people) to read the query, and is a good practice to do so.")
    st.markdown("SQL executes the query **from the first letter** (or from after the previous semicolon), up until the **semicolon ` ; `** at the end of the query,")
    st.write("")
    st.markdown("so make sure to **put semicolon at the end of your query.**")
    st.write("Here's a last, quick example on how to put more than two conditions in one query.")
    st.code('''SELECT * FROM film_list
WHERE actors LIKE "%johnny cage%"
AND category IN ("Horror", "Sci-Fi", "Documentary")
AND rating != "R"
AND length < 150;''', language = "sql")
    st.markdown("*Explanation on the code:*")
    st.write("It is looking for films that are starred by Johnny Cage; has category either Horror, Sci-Fi, or Documentary; isn't R-rated; and shorter than 150 minutes in film length.")
    st.markdown("**BONUS**")
    st.write("It is also a crucial function to find out rows that has `Null` values. Here's how.")
    st.code("SELECT * FROM rental WHERE return_date IS NULL;", language = "sql")
    st.write("Or in the opposite direction, if we want to just exclude rows with `Null` values:")
    st.code("SELECT * FROM rental WHERE return_date IS NOT NULL;", language = "sql")

def selection_1_4():
    st.subheader("String Operations")
    st.write("")
    st.write("This is commonly used to change text values in the columns, or to change the column name itself. Here's a quick example.")
    st.code("SELECT CONCAT(first_name, last_name) FROM customer;", language = "sql")
    st.write("If you run that query, you might notice that there's no separator between the first name and last name.")
    st.write("To add an empty space, we can do it like this")
    st.code("SELECT CONCAT(first_name, ' ', last_name) FROM customer;", language = "sql")
    st.write("Also notice that the column name is a mess. We can rename it using `AS`")
    st.code("SELECT CONCAT(first_name, ' ', last_name) AS customer_name FROM customer;", language = "sql")
    st.write("It can get more creative/complicated with more advanced string operations.")
    st.write("Let's say we want only the names' first letters to be capitalized. Here's how:")
    st.code('''SELECT CONCAT(SUBSTR(last_name,1,1),LOWER(SUBSTR(last_name,2)))
as last_name from customer;''', language = "sql")
    st.write("There are two new functions used here:")
    st.markdown("1. `SUBSTR` is a string operation that takes *n* letters of the string. It goes like this.")
    st.code("SUBSTR(column_name, start_position, length)", language = "sql")
    st.write("If we don't put in a number for the length, we will get all remaining letters from that string.")
    st.write("2. `LOWER` gives us the whole string back, but all lowercased.")
    st.code("SELECT LOWER(first_name) FROM customer;", language = "sql")

def selection_1_5():
    st.subheader("`SELECT ___ FROM ___ ORDER BY ___;`")
    st.write("")
    st.write("Sometimes we want to sort our output by a specific column, or by specific (multiple) columns. We can use `ORDER BY`.")
    st.code("SELECT column_name FROM table_name ORDER BY sorting_column;", language = "sql")
    st.write("By default, it sorts the output in ascending order. You can always re-mention the order to make double sure.")
    st.code("SELECT column_name FROM table_name ORDER BY sorting_column ASC;", language = "sql")
    st.write("To sort the output in descending order, just put `DESC` after the sorting_column.")
    st.code("SELECT column_name FROM table_name ORDER BY sorting_column DESC;", language = "sql")
    st.markdown("*Example:*")
    st.code('''SELECT title, category, price, length
FROM film_list
ORDER BY length DESC;''', language = "sql")
    st.write("You can also sort the data using multiple columns and with different orders.")
    st.code('''SELECT title, category, price, length
FROM film_list
ORDER BY category DESC, price;''', language = "sql")
    st.write("It sorts the output both by category and price columns.")
    st.write("First, it sorts category alphabetically in descending order, then sorts by price in ascending order.")
    st.markdown("*- if we don't put the sorting order, it will sort in ascending order by default.*")
    st.markdown("*- `ORDER BY` can not only sort by alphabet and numerical value, but also date and time, which is also super useful in many cases in the production.*")

def selection_1_6():
    st.subheader("`SELECT ___ FROM ___ LIMIT ___;`")
    st.write("")
    st.write("`LIMIT` limits the number of rows displayed in the output.")
    st.markdown("*Example:*")
    st.code("SELECT * FROM rental ORDER BY last_update LIMIT 5;", language = "sql")
    st.write("What it does is, first it sorts all transaction by transaction date, and putting the latest transactions on top.")
    st.write("Then it takes only 5 first rows for the final output.")

def selection_1_7():
    st.subheader("`SELECT ___ FROM ___ JOIN ___ ON ___;`")
    st.write("")
    st.write("`JOIN` in SQL lets you combine data from multiple tables based on a related column.")
    st.write("It's something Excel can't do easily or at scale, and it's what makes databases powerful;")
    st.write("instead of storing all data in one big table (like in Excel), we normalize data into smaller tables that are related to each other.")
    st.write("Here's a quick example on how to get customer's names from table `customer` and their addresses from table `address`.")
    st.code('''SELECT customer.first_name, customer.last_name, 
CONCAT(address.address, ", ", address.district) AS address
FROM customer
JOIN address
ON customer.address_id = address.address_id;''', language = "sql")
    st.write("Joining two tables or more is possible if both respective tables have common column(s) they want to be joined on.")
    st.write("In this example, both tables `customer` and `address` have a column named `address_id`.")
    st.write("You can also write a cleaner syntax by creating aliases for table names.")
    st.code('''SELECT c.first_name, c.last_name, 
CONCAT(a.address, ", ", a.district) AS address
FROM customer c
JOIN address a
ON c.address_id = a.address_id;''', language = "sql")
    st.write("It's a quick tweak but helps in the long run.")
    st.divider()
    st.subheader("Multiple JOINs")
    st.write("There can be multiple `JOIN` in one query. Here's a good use-case example.")
    st.write("Say we want to find out which customers haven't returned the films they rented, and which films they are currently renting.")
    st.markdown("- We can start by looking at table `rental` and see which entries has `Null` in column `return_date`.")
    st.code("SELECT * FROM rental WHERE return_date IS NULL;", language = "sql")
    st.write("- In this output, there are several films that haven't been returned yet.")
    st.write("- We don't have the customer names and film titles, but we have columns `inventory_id` and `customer_id`.")
    st.write("- We will use column `inventory_id` to `JOIN` these tables: `rental` and `inventory`. Both tables happen to have this column.")
    st.write("- If we check the content of table `inventory`, we'll notice there's no film titles. But there is this column `film_id`.")
    st.write("- We can use the column `film_id` to make another `JOIN` with table `film`, to get the film titles.")
    st.write("- We will also use `customer_id` to `JOIN` these tables: `rental` and `customer`. We will retrieve the customer names from there.")
    st.write("")
    st.write("Using that logic, we can formulate the `JOIN` as following.")
    st.code('''SELECT CONCAT(c.first_name, " ",c.last_name) AS customer_name,
f.title, r.return_date
FROM rental r
            
JOIN inventory i -- here's the first JOIN with table 'inventory'
ON r.inventory_id = i.inventory_id
            
JOIN film f -- second JOIN with table 'film' to get film titles
ON i.film_id = f.film_id
            
JOIN customer c -- third JOIN to get customer names
ON r.customer_id = c.customer_id
            
WHERE r.return_date IS NULL
ORDER BY c.last_name, c.first_name;''', language = "sql")
    st.write("Notice that the original table `rental` isn't even used in the output, except for the last column with all `Null`.")
    st.write("We only use the table `rental` to get all the rows we want to have, which is all the films that are still rented and not returned.")
    st.write("What this query just did:")
    st.write("- It first checks all `film_id` from table `rental`, that are not yet returned.")
    st.write("- Still from table `rental`, it takes values from column `customer_id`.")
    st.write("- It uses column `customer_id` to retrieve customer's information from table `customer`.")
    st.write("- Still from table `rental`, it takes values from column `inventory_id`.")
    st.write("- It uses column `inventory_id` to retrieve item information from table `inventory`.")
    st.write("- Inside the table `inventory`, there's no column `title`, but there's a column called `film_id`, which we can use to do `JOIN` to table `film`.")
    st.write("- Using column `film_id`, we retrieve film titles from column `title` from table `film`.")

def selection_1_8():
    st.subheader("Different Types of JOIN")
    st.write("")
    st.write("In the previous part, we used `JOIN` to combine data from two or more tables.")
    st.write("In real practice, there are a few more types of `JOIN`, that we can use in SQL.")
    st.write("The first type was the `INNER JOIN`, or short `JOIN`, which takes only matching rows from table A and table B.")
    st.write("That is, rows where the value exists in both tables.")
    st.write("Here are some other types of `JOIN`.")
    img_join = Image.open("join.jpg")
    if st.toggle("Show Image"):
        st.image(img_join, use_container_width = False)
    st.write("Here's a practical use-case to use the second most used JOIN type: `LEFT JOIN`, compared to the basic `INNER JOIN`.")
    st.code('''SELECT c.first_name, r.rental_date
FROM customer c
INNER JOIN rental r on c.customer_id = r.customer_id;''', language = "sql")
    st.write("If you run this query, it will give us only customers who have rentals.")
    st.write("Now compare the result if we use `LEFT JOIN` instead.")
    st.code('''SELECT c.first_name, r.rental_date
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id;''', language = "sql")
    st.write("This query includes both customers that have rentals, but also the ones that haven't rented anything.")
    st.write("In this result, customers that have no rentals will have `NULL` in the column `rental_date`.")
    st.write("Using this method, we can find out all customers that have never rented anything. Like so:")
    st.code('''SELECT c.first_name, r.rental_date
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
WHERE r.rental_date is NULL;''', language = "sql")
    st.write("Feel free to try it on the test window!")

def selection_1_9():
    st.subheader("Aggregate Functions - `COUNT()` | `COUNT(DISTINCT)` | `SUM()` | `AVG()` | `MIN()` | `MAX()`")
    st.write("")
    st.write("There are a few aggregate functions (or math operations) in SQL that you can use in your data cleaning and preparation processes.")
    st.write("`COUNT()` counts the rows based on conditions that we put in the query,")
    st.write("`COUNT(DISTINCT)` counts how many unique values exist in a column,")
    st.write("`SUM()` adds up numerical values in a column,")
    st.write("`AVG()` calculates the average of a column,")
    st.write("`MIN()` and `MAX()` get us the smallest and largest values in a column respectively.")
    st.write("When we use these functions, we are often in a situation where we also need to summarize data across multiple rows.")
    st.write("For example, `SUM()` adds values from multiple rows — like summing up all rentals made by a customer or in a city.")
    st.write("That's why, whenever we use aggregate functions in SQL, we also need to use `GROUP BY` in our query, which we will cover in the next section.")
    st.write("")
    st.subheader("Non Aggregate Functions - `JULIANDAY()` | `ROUND()` | `ABS()` | `COALESCE()` | `STRFTIME()`")
    st.write("")
    st.write("There are a few more math calculations and functions in SQL that are non-aggregate functions, such as")
    st.write("`JULIANDAY()` to calculate date difference,")
    st.code('''SELECT customer_id,
JULIANDAY(return_date)-JULIANDAY(rental_date) AS rental_duration
FROM rental;''', language = "sql")
    st.write("")
    st.write("`ROUND()` to round decimals,")
    st.code('''SELECT customer_id,
ROUND(JULIANDAY(return_date)-JULIANDAY(rental_date),1) AS rental_duration
FROM rental;''', language = "sql")
    st.write("")
    st.write("`ABS()` to always get the positive value (see that the position of `rental_date` and `return_date` is swapped in the subtraction, which will result in negative values if not using `ABS()`),")
    st.code('''SELECT customer_id,
ABS(ROUND(JULIANDAY(rental_date)-JULIANDAY(return_date),1)) AS rental_duration
FROM rental;''', language = "sql")
    st.write("")
    st.write("`IFNULL()` or `COALESCE()` to check `NULL` within a column and replace them with other values,")
    st.code('''SELECT customer_id, inventory_id,
COALESCE(return_date, "not returned")
FROM rental
ORDER BY return_date;''', language = "sql")
    st.write("")
    st.write("`STRFTIME()` to get specific format of a date value,")
    st.code('''SELECT DISTINCT STRFTIME('%Y-%m', payment_date) AS payment_month
FROM payment;''', language = "sql")
    st.write("and so on.")

def selection_1_10():
    st.subheader("`SELECT ___, SUM(___) AS ___ FROM ___ GROUP BY ___;`")
    st.write("")
    st.write("As mentioned in the previous section, whenever we do any math operation on the column(s), we need to group the rows based on values from another column.")
    st.write("We can group the values by e.g. `customer`, `city`, or `category`, so that SQL knows how to group the results of those math operations.")
    st.write("Here's a quick-start example for an aggregate function combined with `GROUP BY`:")
    st.code('''SELECT customer_id, SUM(amount) AS total_sales
FROM payment
GROUP BY customer_id;''', language = "sql")
    st.write("What it does is calculate total sales from the `payment` table for each `customer_id`, and shows the sales as one customer per row.")
    st.write("")
    st.write("Now there's a case where we `SELECT` a lot of columns, and some are aggregated while some aren't.")
    st.write("To make the query run successfully, we have to `GROUP BY` all columns that are not aggregated. Here's a quick example:")
    st.code('''SELECT category, rating,
AVG(length) FROM film_list
GROUP BY category, rating;''', language = "sql")
    st.write("In this query, we calculate the average film length, and group+sort it by columns `category` and `rating`.")
    st.write("Basically, we need to mention in the `GROUP BY` all columns that are not aggregated.")
    st.write("Here's another example, to help familiarize ourselves with the syntax.")
    st.write("")
    st.write('''We want to see the total payment per customer per month.
             In this query, we will use `STRFTIME()` to get the month and year of the column `payment_date`,
             and calculate the total payment using `SUM()`.''')
    st.code('''SELECT customer_id,
STRFTIME('%Y-%m', payment_date) AS payment_month,
SUM(amount) AS total_payment
FROM payment
GROUP BY customer_id, payment_month
ORDER BY customer_id, payment_month DESC;
''', language = "sql")
    st.write("")
    st.write("Another variation here is to have multiple aggregate functions in one query, which also works well in SQL.")
    st.write("Say we want to see following information:")
    st.write("- `total number of films` in the store,")
    st.write("- `average rental price`, and")
    st.write("- `average film duration`")
    st.write("... for each `film genre`.")
    st.code('''SELECT category AS film_genre,
COUNT(*) AS total_number_of_films,
ROUND(AVG(price),2) AS average_rental_price,
ROUND(AVG(length),0) AS average_film_duration
FROM film_list GROUP BY category
ORDER BY category ASC;''', language = "sql")
    st.write("This is one of the most useful and important operations in data analysis,")
    st.write("... so make sure to practice it plenty. :)")

def selection_1_11():
    st.subheader("`SELECT ___, SUM(___) AS ___ FROM ___ GROUP BY ___ HAVING ___;`")
    st.write("The function `HAVING` has a similar concept to `WHERE`, that is to filter our output based on conditions.")
    st.write("The difference lies mainly on the target column. With `WHERE`, we can apply conditions on almost any column.")
    st.write("With `HAVING` on the other hand, we put conditions on the aggregated column.")
    st.markdown("*For example:*")
    st.write("- We want to check which customer (marked with `customer_id`) has rented more than 40 times in total.")
    st.write("- We will use `COUNT()` to count the occurence, and use `HAVING` to put in the condition for the aggregated values.")
    st.code('''SELECT customer_id, COUNT(rental_date) AS times_rented
FROM rental
GROUP BY customer_id
HAVING times_rented > 40;''', language = "sql")
    st.write("Now we have seen both `WHERE` and `HAVING`in SQL.")
    st.write("In case someone asks you in an interview about the difference between `WHERE` and `HAVING`,")
    st.write("- `WHERE` is used to filter output based on conditions put on non-aggregated columns, whereas")
    st.write("- `HAVING` is used to filter output based on conditions put on aggregated columns.")
    st.divider()
    st.subheader("EXTRAS – All commands together")
    st.write("Here's a real quick example on how to write a query using all commands.")
    st.write("SQL has its specific syntax order that we need to follow when writing our queries.")
    st.code('''SELECT CONCAT(c.first_name,  " ", c.last_name) AS customer_name,
COUNT(r.rental_date) AS times_rented
FROM rental r
JOIN customer c
ON r.customer_id = c.customer_id
GROUP BY customer_name
HAVING times_rented > 30
ORDER BY times_rented DESC
LIMIT 10;''', language = "sql")
    st.write("")
    st.write("So the order is as following:")
    st.write("`SELECT` | `FUNCTIONS` | `AS` | `FROM` | `JOIN` | `ON` | `GROUP BY` | `HAVING` | `ORDER BY` | `LIMIT`.")

def selection_2_1():
    st.subheader("`SELECT CASE WHEN ___ THEN ___ END FROM ___;`")
    st.write("")
    st.write("Think of `CASE WHEN` like a decision helper in SQL, or as `Labeling` function to make labels or categories.")
    st.markdown("It tells us: *Look at this value. Depending on what it is, we will label it as this and that, and so on.*")
    st.write("Here's a quick example to show what `CASE WHEN` does, and how we write it in SQL.")
    st.code('''SELECT length, CASE
WHEN length < 60 THEN "short"
WHEN length BETWEEN 60 AND 90 THEN "medium"
WHEN length BETWEEN 91 AND 120 then "long"
WHEN length > 120 THEN "epic"
END AS length_label
FROM film;''', language = "sql")
    st.write("")
    st.write("Based on the values of the column `length`, we put a conditioned labeling on a new column called `length_label`.")
    st.write("If the value is so and so, we give it `label A`, if it's so and so, we give it `label B`, and so on.")
    st.write("Notice that when we use `CASE WHEN`, we create a new column instead of just retrieving existing columns from a table.")
    st.write("")
    st.write("")
    st.write("You can also use a different method of labeling. This time we're not using range of values, but we're searching for exact values instead. Here's an example.")
    st.code('''SELECT first_name, last_name,
CASE active
WHEN 1 then "active"
WHEN 0 then "inactive"
ELSE "no information"
END
FROM customer;''', language = "sql")
    st.write("In this example, we search for exact values `0` and `1` in column `active`, then puts label to each value however we seem fit.")
    st.write("")
    st.write("")
    st.write("There's also a method to use `CASE WHEN` inside aggregate functions.")
    st.write("For example, we want to count how many `active` and `inactive` customers from table `customer`. We can do it like this.")
    st.code('''SELECT
COUNT(CASE WHEN active = 1 THEN 1 ELSE 0 END) AS total_active_customers,
COUNT(CASE WHEN active = 0 THEN 1 ELSE 0 END) AS total_inactive_customers
FROM customer;''', language = "sql")
    st.write("")
    st.write("This query checks the value in column `active` from table `customer` and create two new labeling columns: `total_active_customers` and `total_inactive_customers`;")
    st.write("- Each time the value in column `active` has value `1`, the column `total_active_customers` will receive a value `1` in that same row.")
    st.write("- The function `SUM` then adds up all the `1`s in that new column and presents it as the number of active customers in the output.")
    st.write("- The same logic goes for column `total_inactive_customers`, except it puts value `1` for each `0` in column `active`.")
    st.write("")
    st.write("")
    st.write("`CASE WHEN` is one of the most used function in data modeling and preprocessing. Feel free to check this page again in the future to see how to write the correct syntax!")

def selection_2_2():
    st.subheader("`SELECT ___ FROM ( SELECT ___ FROM ___ );`")
    st.write("")
    st.write("A `subquery` is a query inside another query. It helps break down complex logic by using one query to do one step, then write another query to do the next step.")
    st.write("It's like executing a process on top of a result of a different process.")
    st.write("We can place one or more `subqueries` inside a larger query to combine their results into a single output.")
    st.write("")
    st.write("")
    
    st.markdown("*Example:*")
    st.code('''SELECT first_name, last_name
FROM customer
WHERE customer_id IN
    (
    SELECT customer_id, COUNT(*)
    FROM rental
    GROUP BY customer_id
    HAVING count(*) > 40
    );''', language = "sql")
    st.write("We want to find all `customer_names` who have rented more than 40 times. We can do that by")
    st.write("- first, listing all `customer_id` that appear at least 40 times in table `rental` (we can see this in the lower part of the query),")
    st.write("- then, selecting the `customer_names` from table `customer`, whose `customer_id` are in that list.")
    st.write("")
    st.write("")
    st.write("We can also put multiple subqueries inside a query, and in various places. Here are osme examples.")
    st.code('''SELECT
    (SELECT COUNT(*) FROM customer) as total_customers,
    (SELECT COUNT(*) FROM film) as total_films;''', language = "sql")
    st.write("- We count the total number of rows in table `customer` and serve it as a single-row number in a new column called `total_customers`")
    st.write("- We also count the total number of rows in table `films` and serve it as a single-row number in a new column called `total_films`")
    st.write("- both tables `customer` and `film` are not connected/related with each other in this case, and are not joined either. The first column is completely unrelated to the second column.")
    st.write("")
    st.write("")
    st.write("Here's another variation: a `query` inside a `query` inside a `query` (see indentation to help identify each query).")
    st.write("Try to figure out what this query does!")
    st.code('''SELECT first_name, last_name
FROM customer
WHERE customer_id IN

    (
    SELECT r.customer_id
    FROM rental r
    JOIN inventory i
    ON r.inventory_id = i.inventory_id
    JOIN film f
    ON i.film_id = f.film_id
    WHERE f.rental_rate = 

        (
        SELECT MAX(rental_rate)
        FROM film
        )
    );''', language = "sql")

def selection_2_3():
    st.subheader("`WITH ___ AS(SELECT ___ FROM ___) SELECT ___ FROM ___;`")
    st.write("")
    st.markdown("**CTE** (short for 'Common Table Expression') lets you define a **temporary result** (like a mini output table) that you can use in the main query.")
    st.write("It helps us:")
    st.write("- break complex queries into readable steps,")
    st.write("- avoid repeating the same subquery multiple times,")
    st.write("- make our SQL cleaner and easier to follow.")
    st.write("")
    st.write("It is defined using `WITH` keyword, then followed with a name / an alias for that temporary table, and then added with `AS` and a full query inside a parentheses `( ... )`.")
    st.write("The query inside the `( ... )` defines our temporary table, and it can be called as many times as we want inside our main query.")
    st.write("")
    st.markdown("*Example:*")
    st.code('''WITH top_customers_list AS
    (
    SELECT customer_id
    FROM rental
    GROUP BY customer_id
    HAVING COUNT(*) > 40
    )
SELECT * FROM top_customers_list;''', language = "sql")
    st.write("Notice that we don't have a table called `top_customers_list` in our database. That table is our temporary table, that was defined in the upper half of the query using `CTE`. See indented part between `(` and `)`.")
    st.write("")
    st.write("We can also `JOIN` a `CTE` table with a real, existing table. SQL treats `CTE` like regular tables because the result is stored in temporary memory, allowing us to combine it with other data, add more filters, or select additional columns.")
    st.write("")
    st.markdown("*Example with `JOIN`:*")
    st.code('''WITH rental_counts AS
    (
    SELECT customer_id, COUNT(*) AS total_rentals
    FROM rental
    GROUP BY customer_id
    )
SELECT c.first_name, c.last_name, rc.total_rentals
FROM customer c
JOIN rental_counts rc
ON c.customer_id = rc.customer_id;''', language = "sql")
    st.write("")
    st.write("What this query does:")
    st.write("- it counts the `number of rentals` from each `customer`, grouped by the `customer_id`")
    st.write("- it stores that output as a temporary table, or we call it `CTE`, and rename that table as `rental_counts`")
    st.write("- it then runs `JOIN` that table with the already existing table `customer`, to get the customers' `first_name` and `last_name` using their unique `customer_id`")

def selection_2_4():
    st.subheader("CTE vs. Subquery")
    st.write("")
    st.markdown("We’ve now seen both `subquery` and `CTE`, and if we look closely, they actually serve a similar purpose — *breaking down a complex query into smaller parts.*")
    st.write("Both let us run one query inside another, but they shine in slightly different situations.")
    st.write("- Use a `subquery` when you just need a quick, simple filter or calculation inside your main query.")
    st.write("- Use a `CTE` when your logic is longer, reused multiple times, or you want the query to stay clean and readable.")
    st.write("In short, `subqueries` are quick and compact, while `CTEs` are better for clarity and maintainability. But in real practice, there's almost no case where one method can be used and the other cannot.")
    st.write("")
    st.write("")
    st.write("Here's an example showing how both give the same result, even though one uses a `subquery` and the other uses a `CTE` for the same logic.")
    st.write("We want to find the first name and last name of customers who have rented more than 40 times in total.")
    st.write("")
    st.markdown("*Subquery:*")
    st.code('''SELECT first_name, last_name
FROM customer
WHERE customer_id IN
    (
    SELECT customer_id
    FROM rental
    GROUP BY customer_id
    HAVING COUNT(*) > 40
    );
''', language = "sql")
    st.write("")
    st.markdown("*CTE:*")
    st.code('''WITH frequent_payers AS
    (
    SELECT customer_id
    FROM rental
    GROUP BY customer_id
    HAVING COUNT(*) > 40
    )

SELECT c.first_name, c.last_name
FROM customer c
JOIN frequent_payers f
ON c.customre_id = f.customer_id;''', language = "sql")

def selection_2_5():
    st.subheader("Window Function: Row Numbering & Ranking")
    st.write("")
    st.write("Sometimes we need to assign a position or ranking to each row — for example, to number the rows in a result, or find the top 3 items per category.")
    st.write("SQL provides special window functions for this purpose: `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`.")
    st.write("They all assign a number to each row based on a sorting order, but they behave slightly differently when there are ties.")
    st.write("Here's an example on how each window function is written and what they give us in the output:")
    st.code('''WITH payment_totals AS
    (
    SELECT 
    customer_id,
    SUM(amount) AS total_paid
    FROM payment
    GROUP BY customer_id
    )

SELECT 
customer_id,
total_paid,
ROW_NUMBER() OVER (ORDER BY total_paid DESC) AS row_num,
RANK() OVER (ORDER BY total_paid DESC) AS rank,
DENSE_RANK() OVER (ORDER BY total_paid DESC) AS dense_rank
FROM payment_totals
ORDER BY total_paid DESC
LIMIT 10;''', language = "sql")
    st.markdown("*Explanation:*")
    st.write("- `ROW_NUMBER()` gives a unique number to each row, even if the `total paid` is the same.")
    st.write("- `RANK()` gives the same number to ties, but then skips the next number(s). See the query result with row number 4 to 6.")
    st.write("- `DENSE_RANK()` gives the same number to ties, but does not skip any numbers. See the query result with row number 4 to 6.")

def selection_2_6():
    st.subheader("Window Function: Running Totals & Aggregates")
    st.write("")
    st.write("In many real-world cases, we don’t just want totals — we want to see how those totals grow over time.")
    st.write("This is where running totals come in. Using window functions like `SUM()` or `COUNT()` with `OVER()`, we can calculate values row by row while keeping the full detail.")
    st.write("It’s perfect for tracking daily revenue, cumulative sales, or rental activity over time.")
    st.write("")
    st.write("Here's an example to help us understand what this window function gives us as an output.")
    st.code('''SELECT 
DATE(payment_date) AS pay_date,

SUM(amount) AS daily_sum,
SUM(amount) OVER (ORDER BY DATE(payment_date)) AS running_sum,

AVG(amount) AS daily_avg,
AVG(amount) OVER (ORDER BY DATE(payment_date)) AS running_avg,

COUNT(*) AS daily_count,
COUNT(*) OVER (ORDER BY DATE(payment_date)) AS running_count,

MIN(amount) AS daily_min,
MIN(amount) OVER (ORDER BY DATE(payment_date)) AS running_min,

MAX(amount) AS daily_max,
MAX(amount) OVER (ORDER BY DATE(payment_date)) AS running_max

FROM payment
GROUP BY DATE(payment_date)
ORDER BY pay_date
LIMIT 10;''', language = "sql")
    st.write("")
    st.write("Normal aggregate functions summarize each group. Window functions let us calculate totals, averages, and more — without collapsing the rows.")

def selection_2_7():
    st.subheader("Window Function: Comparing Rows")
    st.write("")
    st.write("There are times when we want to compare one row to another — like checking how today’s number is different from yesterday’s.")
    st.write("Window functions like `LAG()` and `LEAD()` help us do that.")
    st.write("They let us look at the value from the previous or next row, without doing anything complicated.")
    st.write("This is useful when we want to see changes over time, track growth, or spot differences in a list of values.")
    st.write("")
    st.write("Here's a quick example on how it's written and how the output looks like.")
    st.code('''SELECT 
payment_id,
payment_date,
amount,

LAG(amount) OVER (ORDER BY payment_date) AS previous_amount,
LEAD(amount) OVER (ORDER BY payment_date) AS next_amount,
FIRST_VALUE(amount) OVER (ORDER BY payment_date) AS first_amount,
LAST_VALUE(amount) OVER (ORDER BY payment_date) AS last_amount

FROM payment
ORDER BY payment_date
LIMIT 20;''', language = "sql")
    st.write("")
    st.write("Here's what each window function does:")
    st.write("- `LAG()` shows the value from the previous row — like looking back one step.")
    st.write("- `LEAD()` shows the value from the next row — like looking forward one step")
    st.write("- `FIRST_VALUE()` shows the very first value in the ordered list.")
    st.write("- `LAST_VALUE()` shows the last value in the ordered list.")
    st.write("")
    st.write("All these functions help you compare each row with other rows around it, without removing any rows from the results.")

def selection_2_8():
    st.subheader("`PARTITION BY`")
    st.write("")
    st.write("So far, we’ve seen window functions like `SUM()` or `ROW_NUMBER()` applied across all rows.")
    st.write("But what if we want to restart the calculation for each customer, city, or category?")
    st.write("This is where `PARTITION BY` comes in — it splits the data into groups, and the window function works **within each group**.")
    st.write("Unlike `GROUP BY`, `PARTITION BY` doesn’t collapse rows — it keeps the full detail of the data.")
    st.write("")
    st.write("Here's an example on how to use `PARTITION` to calculate cumulative payments per customer.")
    st.code('''SELECT customer_id, payment_id, amount, payment_date,
SUM(amount) OVER
    (
    PARTITION BY customer_id 
    ORDER BY payment_date
    ) 
    AS running_total
FROM payment
ORDER BY customer_id, payment_date
LIMIT 20;''', language = "sql")
    st.write("This shows:")
    st.write("- Each customer gets their own `running total` of payments,")
    st.write("- resetting at each `customer_id`.")
    st.write("")
    st.write("")
    st.write("To give a better idea of how `PARTITION BY` works, we can take a look at this second example, where we want to give `ROW_NUMBER()` per customer, to give numbers for each transaction/rental of each individual user.")
    st.code('''SELECT customer_id, payment_id, payment_date, amount,
ROW_NUMBER() OVER
    (
    PARTITION BY customer_id 
    ORDER BY payment_date
    )
    AS payment_sequence
FROM payment
ORDER BY customer_id, payment_sequence
LIMIT 20;''', language = "sql")
    st.write("")
    st.write("This example shows how to give number to each customer's `payments` in order, then resets the counting when we switch to the next `customer`.")
    st.write("That is exactly what `PARTITION` does: it splits the data into separate groups (in this case, by customer), so that the window function starts fresh in each group.")

def test_easy():
    st.write("")
    st.write("")
    st.markdown(
    "<h3 style='text-align: center; font-style: italic;'>HOW TOUGH ARE YOU? (level: easy)</h3>", 
    unsafe_allow_html=True)
    st.write("")
    st.write("")
    with st.container(border=1):
        st.write("###### Learned plenty enough? Here are some warm-up questions that check whether you’ve really got the basics nailed down. Nothing fancy yet — just enough to make sure you can fetch, filter, and sort data without breaking a sweat.")
    df = pd.read_csv("sakila.csv")
    df = df[df.level =="easy"]
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    for no,question,solution in zip(df["no"].values.tolist(), df["question"].values.tolist(), df["solution"].values.tolist()):
        q1,q2 = st.columns([1,8])
        q1.subheader(str(int(no)))
        q2.write(question)
        df_solution = get_output_df(solution)
        with st.expander("Write your queries here:"):
            st.write(get_table_names())
            query = st.text_area("",key = "query_"+question)
            if (len(query) != 0) or (st.button("Run", key = "run"+question)):
                try:
                    df_user = get_output_df(query)
                    st.dataframe(df_user)
                    st.write("Expected columns in the output: "+ get_formattings(df_solution)[0])
                    st.write("Expected number of rows: `"+str(get_formattings(df_solution)[1])+"`")
                    st.write("Your number of rows: `"+str(df_user.shape[0])+"`")
                    check_answer(df_user,df_solution,question)
                except Exception as e:
                    st.error(f"❌ SQL Error: {e}")
        st.write("")
        st.write("")
        st.write("")

def test_medium():
    st.write("")
    st.write("")
    st.markdown(
    "<h3 style='text-align: center; font-style: italic;'>HOW TOUGH ARE YOU? (level: medium)</h3>", 
    unsafe_allow_html=True)
    st.write("")
    st.write("")
    with st.container(border=1):
        st.write("###### Ready to test your mettle? These questions go one step further, using subqueries, CTEs, and window functions. They’re not meant to break you — just to stretch your thinking and prepare you for the kind of SQL puzzles you’ll meet in real projects.")
    df = pd.read_csv("sakila.csv")
    df = df[df.level =="medium"]
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    for no,question,solution in zip(df["no"].values.tolist(), df["question"].values.tolist(), df["solution"].values.tolist()):
        q1,q2 = st.columns([1,8])
        q1.subheader(str(int(no)))
        q2.write(question)
        df_solution = get_output_df(solution)
        with st.expander("Write your queries here:"):
            st.write(get_table_names())
            query = st.text_area("",key = "query_"+question)
            if (len(query) != 0) or (st.button("Run", key = "run"+question)):
                try:
                    df_user = get_output_df(query)
                    st.dataframe(df_user)
                    st.write("Expected columns in the output: "+ get_formattings(df_solution)[0])
                    st.write("Expected number of rows: `"+str(get_formattings(df_solution)[1])+"`")
                    st.write("Your number of rows: `"+str(df_user.shape[0])+"`")
                    check_answer(df_user,df_solution,question)
                except Exception as e:
                    st.error(f"❌ SQL Error: {e}")
        st.write("")
        st.write("")
        st.write("")
            


@st.dialog("Info Corner")
def open_info_corner():
    c1,c2 = st.columns([3,1])
    with c1:
        info_corner = st.selectbox("Got any question?",["What is SQL, and what do I use it for?","What is this database about?","How does this app work?"])
    with c2:
        st.write("")
        st.write("")
        st.image("infodesk.jpeg", width=70)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    if info_corner == "What is SQL, and what do I use it for?":
        st.write('''SQL (Structured Query Language) is the language used to communicate with databases.
                    It helps you find, add, update, or delete data stored in structured tables — 
                    kind of like how Excel has rows and columns.''')
        st.write('''But unlike Excel, SQL works with much larger datasets and allows you to connect multiple tables together. 
                    This is useful when you want to pull out meaningful insights from messy or complex data.''')
        st.write('''Whether you're tracking sales, users, or inventory, 
                    SQL is a powerful tool that helps you ask specific questions and get the exact answers you need.''')
    elif info_corner == "What is this database about?":
        st.write('''The database used in this tutorial is the Sakila database — 
                    a sample dataset created by MySQL to simulate a DVD rental business.''')
        st.write('''It contains data on movies, actors, customers, rentals, payments, and staff. 
                    For example, you can check which films were rented, who rented them, and how much they paid.''')
        st.write('''Sakila is widely used for learning SQL because it’s realistic, well-structured, 
                    and gives you a hands-on feel for working with real business data.''')
    elif info_corner == "How does this app work?":
        st.write('''This app is built to help you learn and practice SQL in a simple and hands-on way. 
                 It starts with tutorials that explain how SQL commands work and what they’re used for, 
                 followed by real-world business questions from various industries.''')
        st.markdown('''*Who this app is for:*''')
        st.write("- 🟢 Beginners – A great way to learn SQL step by step and discover how different industries use it.")
        st.write("- 🧠 Experienced users – A helpful reminder of SQL syntax and logic when you need a quick refresh.")
        st.write("- 💼 Job seekers – A solid exercise to build confidence and prepare for SQL-based tasks or interviews.")

def page():
    st.write("")
    st.write("")
    if st.button("Open Info Corner"):
        open_info_corner()
    with st.container(border = True):
        level, options = select_level()
    st.write("")

    if (level == "Basics - Quick Start") or (level == "Medium - Confident at Work"):
        c1,c0,c2 = st.columns([1.2,.4,1])
        with c1:
            table_names = get_table_names()
            st.subheader("List of Table Names")
            st.write("")
            st.write("")
            st.write(table_names)
        with c2:
            st.subheader("Select Content")
            selection = st.pills("", options, selection_mode = "single", default = options[0])
        st.divider()
        if selection == "1 - SELECT FROM":
            selection_1_1()

        elif selection == "2 - AS (alias)":
            selection_1_2()
            
        elif selection == "3 - WHERE":
            selection_1_3()

        elif selection == "4 - String Operations":
            selection_1_4()

        elif selection == "5 - ORDER BY":
            selection_1_5()

        elif selection == "6 - LIMIT":
            selection_1_6()

        elif selection == "7 - JOIN":
            selection_1_7()

        elif selection == "8 - More JOINs":
            selection_1_8()

        elif selection == "9 - Basic Functions":
            selection_1_9()

        elif selection == "10 - GROUP BY":
            selection_1_10()

        elif selection == "11 - HAVING":
            selection_1_11()

        elif selection == "`HOW TOUGH ARE YOU? (EASY)`":
            test_easy()

        elif selection == "`HOW TOUGH ARE YOU? (MEDIUM)`":
            test_medium()

        elif selection == "1 - CASE WHEN":
            selection_2_1()

        elif selection == "2 - SUBQUERY":
            selection_2_2()

        elif selection == "3 - CTE":
            selection_2_3()    

        elif selection == "4 - CTE vs Subquery":
            selection_2_4()

        elif selection == "5 - Window: Row Numbering":
            selection_2_5()

        elif selection == "6 - Window: Running Totals":
            selection_2_6()

        elif selection == "7 - Window: Comparing Rows":
            selection_2_7()

        elif selection == "8 - PARTITION":
            selection_2_8()
        else:
            st.write("Coming Soon")
        st.write("")
        if st.button("OPEN TEST WINDOW", key = "test_query", use_container_width=True):
            test_query()
    elif level == "Advanced - Deployment Ready":
        return level