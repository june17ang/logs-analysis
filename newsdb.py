#!/usr/bin/env python
import os
import psycopg2
import sys


def write_file(output):
    writefile = open('result.txt', 'a')
    writefile.write(output)
    writefile.close()


def database_connection(database_name):
    """Connect to the database.  Returns a database connection."""
    try:
        db = psycopg2.connect(database=database_name)
        return db
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def execute_queries(query, result_fetch_one=False):
    """
    execute_query takes a SQL query as a parameter.
            Executes the query and returns the results as a list of tuples.
           args:
               query - an SQL query statement to be executed.

           returns:
               A list of tuples containing the results of the query.
    """
    db = database_connection('news')
    csr = db.cursor()

    csr.execute(query)
    result = csr.fetchone() if result_fetch_one else csr.fetchall()

    csr.close()
    db.close()

    return result


def print_top_articles():
    """Prints out the top 3 articles of all time."""
    print("Processing to find Top 3 articles...")
    print("---------------------------------------------------------")
    query = "SELECT title, COUNT(*)::decimal AS views " \
            "FROM log JOIN articles " \
            "ON log.path = CONCAT('/article/', articles.slug) " \
            "GROUP BY title " \
            "ORDER BY views DESC " \
            "LIMIT 3"

    results = execute_queries(query)
    # add code to print results
    output = 'The most popular 3 articles:\n'
    for title, views in results:
        output += "\"{title}\" - {views} views\n".format(
            title=title, views=views)

    output += '---------------------------------------------------------\n'
    write_file(output)
    print(output)


def print_top_authors():
    """Prints out the top 5 authors of all time."""
    print("Processing to find Top 5 authors...")
    print("---------------------------------------------------------")
    query = "SELECT authors.name AS author_name, COUNT(*)::decimal AS views " \
        "FROM log JOIN articles " \
            "ON log.path = CONCAT('/article/', articles.slug) " \
        "JOIN authors ON articles.author = authors.id " \
        "GROUP BY author_name " \
        "ORDER BY views DESC " \
        "LIMIT 5"

    results = execute_queries(query)
    # add code to print results
    output = 'The most popular 5 article authors:\n'
    for author, views in results:
        output += "{author} - {views} views\n".format(
            author=author, views=views)

    output += '---------------------------------------------------------\n'
    write_file(output)
    print(output)


def print_errors_over_one():
    """
    Prints out the days where more than 1% of logged access
    requests were errors.
    """
    print("Processing to find a day on request error more then 1%...")
    print("---------------------------------------------------------")
    query = "SELECT to_char(date, 'FMMonth FMDD, YYYY'), err/total AS ratio " \
            "FROM " \
            "(SELECT time::date AS date, COUNT(*) aS total, " \
            "SUM((status != '200 OK')::int)::float AS err " \
            "FROM log GROUP BY date) AS errors " \
            "WHERE err/total > 0.01"

    results = execute_queries(query, True)
    # add code to print results
    output = 'More than 1% of requests lead to errors: \n'
    output += "{date} - {rate}% errors \n".format(
        date=results[0], rate=results[1])
    output += '---------------------------------------------------------\n'
    write_file(output)
    print(output)


if __name__ == '__main__':
    if os.path.exists("result.txt"):
        os.remove("result.txt")

    print_top_articles()
    print_top_authors()
    print_errors_over_one()
    print('Completed!')
