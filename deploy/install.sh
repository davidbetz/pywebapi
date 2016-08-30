# Security

yum install setroubleshoot -y

cat > /var/tmp/allow_nginx_socket.te << EOF
module allow_nginx_socket 1.0;

require {
        type httpd_t;
        type httpd_sys_content_t;
        class sock_file write;
}

#============= httpd_t ==============
allow httpd_t httpd_sys_content_t:sock_file write;
EOF

semanage fcontext -at httpd_sys_content_t "/srv(/.*)?"
checkmodule -M -m -o /var/tmp/allow_nginx_socket.mod /var/tmp/allow_nginx_socket.te
semodule_package -o /var/tmp/allow_nginx_socket.pp -m /var/tmp/allow_nginx_socket.mod
semodule -i /var/tmp/allow_nginx_socket.pp

systemctl start firewalld
systemctl enable firewalld
firewall-cmd --permanent --zone=public --add-interface=eth0
firewall-cmd --reload
firewall-cmd --permanent --add-service=http --zone=public
firewall-cmd --reload

# Just for testing...

cat > /srv/robots.txt << EOF
User-agent: ia_archiver
Disallow: /
EOF

# App

yum install epel-release -y
yum install python34 python-pip -y
pip install --upgrade pip
pip install --upgrade virtualenv
cd /srv
virtualenv -p python3 webapi
cd webapi
source bin/activate
yum install git -y
git clone https://github.com/davidbetz/webapipy content
cd content
pip install -r requirements.txt
deactivate

# UWSGI

yum install uwsgi uwsgi-plugin-python3 -y

cat > /etc/uwsgi.d/webapi.ini << EOF
[uwsgi]
project = content
base = /srv/webapi/content
virtualenv = /srv/webapi

chdir = %(base)
home = %(virtualenv)
module = app:webapi_start

master = true
processes = 5

socket = %(base)/%(project).sock
chmod-socket = 666
uid = uwsgi
gid = uwsgi
vacuum = true

plugins = python3
EOF

chown -R uwsgi:uwsgi /etc/uwsgi.d/webapi.ini
chown -R uwsgi:uwsgi /srv

restorecon -R -v /srv

systemctl restart uwsgi

#Nginx

cat > /etc/yum.repos.d/nginx.repo << EOF
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/mainline/centos/\$releasever/\$basearch/
gpgcheck=0
enabled=1
EOF

yum install -y nginx

export PUBLIC_IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')

mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.disabled
cat > /etc/nginx/conf.d/webapi.conf << EOF
server {
    listen $PUBLIC_IP:80;

    location /robots.txt {
        alias /srv/robots.txt;
    }

    location / {
        include            uwsgi_params;
        uwsgi_pass         unix:/srv/webapi/content/content.sock;

        proxy_redirect     off;
        proxy_set_header   Host \$host;
        proxy_set_header   X-Real-IP \$remote_addr;
        proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Host \$server_name;
    }
}
EOF

systemctl restart nginx

# Test

curl $PUBLIC_IP/robots.txt
curl $PUBLIC_IP/item/1

