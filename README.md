# Kreotive

### 1. Server Installation
#### Environment
- Ubuntu 16.04 LTS 64 bit
- MongoDB 3.2.x
- Apache Virtual Hosts (httpd)

#### Initial Setup
Apache Virtual Host:
```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
```

Open the new file in your editor with root privileges:
```
sudo nano app.wsgi
```

And configure the project's path:
```
app_dir_path = '/var/www/kreotive'
```

Create and edit project config file:
```
sudo config-template.cfg config.cfg
sudo nano config.cfg
```


#### Create New Virtual Host
Copy default virtual host config file to create new file specific to the project:
```
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/kreotive.com.conf
```

Open the new file in your editor with root privileges:
```
sudo nano /etc/apache2/sites-available/kreotive.com.conf
```

And configure it to point to the project's app.wsgi file:
```
<VirtualHost *:80>
  ServerAdmin admin@localhost
  #ServerName kreotive.com
  
  WSGIScriptAlias / /var/www/kreotive/app.wsgi
  <Directory /var/www/kreotive>
    Order allow,deny
    Allow from all
  </Directory>
    
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

#### Enable New Virtual Host
First disable the defaul one:
```
sudo a2dissite 000-default.conf
```

Then enable the new one we just created:
```
sudo a2ensite kreotive.com.conf
```

Restart the server for these changes to take effect:
```
sudo service apache2 restart
```


### 2. Local Installation (UBUNTU)


First create a folder in your desktop called dev:
```
cd ~
mkdir dev
cd dev
```

Getting the project in your local machine:
```
git clone https://github.com/Gaddea/kreotive.git
cd kreotive
```

Install and run the app:
```
bash install.sh
bash run-debug.sh
```

### 3. Create Indexes for search fields

db.organizations.createIndex({name:"text"})
db.users.createIndex({name:"text", lastname:"text"})
db.content.createIndex({title:"text", content:"text"})






