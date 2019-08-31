## Udacity Full Stack Wed Developer Nanodegree - Project 1
#### Project Description
List all top 3 articles, top 5 authors and find request error that more then 1% per day from news database.

#### Prerequisites
- Python 2.7+
- Vagrant
- VirtualBox

#### How to Run
- Install <a href="https://www.vagrantup.com/downloads.html" tips="click redirect to installation page">Vagrant</a>

- Install <a href="https://www.virtualbox.org/wiki/Downloads" tips="click redirect to installation page">Virtualbox</a>

- Clone git project <br>
```git clone https://github.com/June17ang/logs-analysis.git```

- Change directory <br>
```cd logs-analysis```

- Download 
<a target="_blank" href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">newsdata.zip</a>

- Unzip newsdata.zip in logs-analysis directory


- Setup virtual environment <br>
```vagrant up```

- SSH into vagrant <br>
```vagrant ssh```

- Change to project directory <br>
```cd /vagrant```

- Import newsdata.sql into news database <br>
```psql -d news -f newsdata.sql```

- Check newsdb.py is in /vagrant directory <br>
```ls -lrt```

- Run newsdb.py to generate result
```python newsdb.py```

- View result <br>
```cat result.txt```