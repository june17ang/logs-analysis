import psycopg2

db = psycopg2.connect(database='news')
c = db.cursor()

# Count visitor statistic
statistic_query = "create view statistic as select count(path)::decimal as view, regexp_replace(path, '^(.*[\\\/])', '', 'g') as slug from log where path != '/' group by slug"

c.execute(statistic_query)

# Find top three artcles
top3articles_query = "select articles.title, statistic.view from articles left join statistic on articles.slug = statistic.slug order by statistic.view desc limit 3"

c.execute(top3articles_query)
top3articles = c.fetchall()

# Find top five authors
top5authors_query = "select authors.name, sum(statistic.view)::decimal as total_view from authors left join articles on authors.id = articles.author left join statistic on articles.slug = statistic.slug group by authors.name order by total_view desc limit 5"

c.execute(top5authors_query)
top5authors = c.fetchall()

# Find day on request error more then 1%
request_statistic = "select date(time) as date, round(sum(case when status != '200 OK' then 1 else 0 end)::decimal / count(id)::decimal * 100, 1) as error_rate from log group by date having (sum(case when status != '200 OK' then 1 else 0 end)::decimal / count(id)::decimal * 100) > 1"
c.execute(request_statistic)
day_error = c.fetchone()

db.close()

# Result
result = 'The most popular 3 articles: \n'
for title, views in top3articles:
    result += "\"{title}\" - {views} views\n".format(title=title, views=views)

result += '\n\n'
result += 'The most popular 5 article authors:\n'
for author, views in top5authors:
    result += "{author} - {views} views\n".format(author=author, views=views)

result += '\n\n'
result += 'More than 1% of requests lead to errors:\n'
result += "{date} - {rate}% errors\n".format(date=day_error[0].strftime("%b %d, %Y"), rate=day_error[1])

# Write file
writefile = open('result.txt', 'w+')
writefile.write(result)
writefile.close()

print('Completed!')