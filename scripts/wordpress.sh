#!/bin/bash

mysqldb="wordpress"
mysqluser="wordpress"
mysqlpass="password"

wptitle="Khiem's Blog"
wppass="241194"
wpemail="doankhiem.crazy@gmail.com"

sudo apt-get -y update
sudo apt-get -y upgrade

# install apache
sudo apt-get -y install apache2
echo 'ServerName 0.0.0.0' | sudo tee --append /etc/apache2/apache2.conf > /dev/null
sudo ufw app info "Apache Full"
sudo systemctl restart apache2

# install mysql
sudo apt-get -y install mariadb-server
sudo mysql -u root -e "use mysql; update user set plugin='' where User='root'; flush privileges;"
sudo mysql -u root -e "use mysql; update user set password=PASSWORD('sqlpassword') where User='root'; flush privileges;"

# install php
sudo apt-get -y install php libapache2-mod-php php-mcrypt php-mysql php-json
sed -i "s/index.html/index.tmp/g;s/index.php/index.html/g;s/index.tmp/index.php/g" /etc/apache2/mods-enabled/dir.conf
sudo systemctl restart apache2

# install wordpress
mysql -u root -psqlpassword -e "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci; GRANT ALL ON wordpress.* TO 'wordpressuser'@'localhost' IDENTIFIED BY 'wordpresspassword'; FLUSH PRIVILEGES;"
sudo apt-get -y install php-curl php-gd php-mbstring php-mcrypt php-xml php-xmlrpc
cat << EOF | sudo tee --append /etc/apache2/apache2.conf > /dev/null
<Directory /var/www/html/>
    AllowOverride All
</Directory>
EOF
sudo a2enmod rewrite
sudo systemctl restart apache2

cd /tmp
wget http://wordpress.org/latest.tar.gz
tar zxf /tmp/latest.tar.gz

wget -O /tmp/wp.keys https://api.wordpress.org/secret-key/1.1/salt/
sed -e "s/database_name_here/wordpress/" -e "s/username_here/wordpressuser/" -e "s/password_here/wordpresspassword/" /tmp/wordpress/wp-config-sample.php > /tmp/wordpress/wp-config.php
sed -i '/#@-/r /tmp/wp.keys' /tmp/wordpress/wp-config.php
sed -i "/#@+/,/#@-/d" /tmp/wordpress/wp-config.php

touch /tmp/wordpress/.htaccess
chmod 660 /tmp/wordpress/.htaccess
mkdir /tmp/wordpress/wp-content/upgrade
sudo cp -a /tmp/wordpress/. /var/www/html

sudo find /var/www/html -type d -exec chmod g+s {} \;
sudo chmod g+w /var/www/html/wp-content
sudo chmod -R g+w /var/www/html/wp-content/themes
sudo chmod -R g+w /var/www/html/wp-content/plugins

rm -R /tmp/wordpress
rm /tmp/latest.tar.gz
rm /tmp/wp.keys

#curl -d "weblog_title=$wptitle&user_name=$wpuser&pass1-text=$wppass&admin_password2=$wppass&admin_email=$wpemail" "http://127.0.0.1/wp-admin/install.php?step=2"