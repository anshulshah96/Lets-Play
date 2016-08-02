Lets-Play
==========

  * [Introduction](#Introduction)
  * [Scan Module](#Scan-Module)
  * [Preview](#Preview)
  * [Setup](#Setup)
  * [License](#license)
  
Introduction
=============

It is a django based website which displays the Counter-Strike servers which are running within the LAN.

Different domains/frameworks which I used within the project are:

- Valve Protocols
- Python Sockets
- Python Concurrency
- Django
- Bootstrap
- JSON encoding

Scan Module
==============

This is the core part of my App which handles the Server Queries over different IPs. 

All running game servers can be queried using UDP/IP packets. The packet format and protocols are described [here](https://developer.valvesoftware.com/wiki/Server_queries). 
I used [python struct](https://docs.python.org/2/library/struct.html) for parsing the binary data obtained over UDP.

1. To initialise a connection, we have to send a *A2S_INFO* query packet to the listening port(27015).
2. The server replies with details like Map Name, Game, Players, Max Players, Password Protection ...
3. For obtaining the details of each player, we have to send a *A2S_PLAYER* query packet again. It will reply with score, time and name of each player.
4. *A2S_RULES* is another query type for obtaining more information but has a lot of issues.

- All the bot names and with some predefined suffix. The list is available [here](http://counterstrike.wikia.com/wiki/Bot). I implemented this check to ensure that no game with a BOT has a contribution to the LeaderBoard.
- To prevent regenerating the exact same web-page I have used cache_page redirective in [django](https://docs.djangoproject.com/en/1.9/topics/cache/)

The scan module is also available as a **stand-alone python library** in PYPI [here](https://pypi.python.org/pypi/valve-range-query/1.0.4).
You can create your own python library/app by following this easy to understand [blog](http://peterdowns.com/posts/first-time-with-pypi.html).

Preview
==========

- List of Servers
![test_image](https://cloud.githubusercontent.com/assets/10174820/17330032/d0b1687e-58e2-11e6-9c48-bf5ef3a47def.png)


- Server Details
![test_image2](https://cloud.githubusercontent.com/assets/10174820/17330045/dccae504-58e2-11e6-888b-ebb0decd928a.png)

Setup
=========
1. Install Python2, Django==1.7.8 and mysql-python (preferably in a virtual env).
2. Create a new DB in mysql and a new user having full access to that DB.
3. Copy LPapp/configuration.py.sample to LPapp/configuration.py provide the DB and user details.
4. Run ./manage.py migrate.
5. Run ./manage.py runserver
6. Run by using python manage.py runserver --noreload --insecure ip:port

License
=========
[MIT License](https://anshul.mit-license.org/)
