### Project Name: project.py
This project will create and run a web application that will enable viewers to view and item catalog and the items listed in the item catalog. Logged in users will be able to create, read, edit and delete different items and catalogs from the web application. Users will be able to login to the web application by using their google account.

#### Requirements:
- Python3 Python3 can be downloaded from https://www.python.org/ for installation on whichever operating system the user is using.
- Vagrant virtual environment, which can be downloaded at: https://www.vagrantup.com/
- Virtualbox Virtualbox can be downloaded from https://www.virtualbox.org/
- Clone or download the fullstack-nanodegree-vm from https://github.com/udacity/fullstack-nanodegree-vm
- Clone or download the application files from the github repository https://github.com/helluva-87/catalog2

### Using The Program:
After installing Vagrant and Virtualbox, navigate to the folder in which you have
cloned/downloaded the fullstack-nanodegree-vm files and folders from https://github.com/udacity/fullstack-nanodegree-vm and open the vagrant folder. Using this folder location or path, launch a terminal and type the command:
      "vagrant up"
The Vagrant virtual environment will load, and once it is completed loading you will have access to the terminal commands again. When vagrant is done initializing, type the command:
      "vagrant ssh"
You will then be connected to the virtual machine and there will be a message that your files are located at the "/vagrant" location.
Change the directory to the vagrant folder by typing:
      "cd /vagrant"
Once you are in the /vagrant folder of the virtual environment, you can type the command:
      "python project.py"
This will launch the application and there will be a notification that the application is "Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)". You can then open a web browser and type in: "http://localhost:5000". This will take you to the homepage of the web application where you will be able to view the item catalogs and then be able to click on a particular catalog to view items for that catalog.
If you click the links to create, edit or delete a catalog or item, you will be redirected to the login page where you will be able to sign in to the web application by using your google account.
### License:
Logs_analysis is a public domain work, dedicated using CC0 1.0. Feel free
to do whatever you want with it.
