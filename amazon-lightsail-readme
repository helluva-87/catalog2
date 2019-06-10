Hello! This web application for the item catalog should be accessible at
54.184.75.80 on ssh port 22 (Amazon Lightsail would not allow custom SSH ports),
using the username of "grader". The password for the user "grader" is "grader".

So the login from the command line would be:

"ssh -i [location of grader ssh key] grader@54.184.75.80"

Then there should be a prompt for the password of "grader" as an extra security
precaution. Grader does have sudo capabilities.

There is a firewall (UFW) that is active and by running the command
"sudo ufw status" the user will receive the following output:

Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123/udp                    ALLOW       Anywhere
5000/tcp                   ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123/udp (v6)               ALLOW       Anywhere (v6)
5000/tcp (v6)              ALLOW       Anywhere (v6)


There is no way to login to the server as root. Also, the option to use a
password for login has been disabled and the only way to login to the server
would be to use a SSH key.



In the virtual environments used, the user will have to install the following
dependencies:

python3
postgresql
sqlite
oauth2client
sqlalchemy
libapache2-mod-wsgi-py3
requests


The following resources were used in researching for deployment of the web
application:

https://www.digitalocean.com/community/tutorials/how-to-configure-the-apache-web-server-on-an-ubuntu-or-debian-vps
http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/
