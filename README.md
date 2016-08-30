# WebAPI for Python

**Copyright (c) 2016 David Betz**

This allows you to create both level 2 Web API services as well as AWS Custom Skill endpoints (for use with Amazon Echo, etc) in Python (both current Python3 and legacy Python2). I've also added support for raw service development, but that's not the primary goal.

Level 2 is not REST. REST requires Hypermedia. Level 3 is REST. You've probably never seen a REST service. There's no official spec for it.

Level 1 is resources. Level 2 is HTTP Verbs.

This is a Level 2 service foundation for WSGI.

cf. [http://martinfowler.com/articles/richardsonMaturityModel.html](http://martinfowler.com/articles/richardsonMaturityModel.html)

Therefore, you will POST, PUT, GET, and DELETE to stuff like /item and /item/2.

Because resource APIs and "REST" are largely impractical in the real world, this project is currently mainly for Amazon Echo Skills.

# Usage

Using this is a matter of creating a repository for your stuff and registering the resource in the resources.py module. The rest is magic.

e.g.
    
    resources = [
        (r'item/?(?P<id>\d+)?$', ItemRepo),
        (r'image/?(?P<id>[\w]+)?$', PictureRepo),
        (r'config/?(?P<id>[!\w]+)?$', AzureItemRepo)
    ]

Using this for AWS is a matter of creating a skill class, registering your intents, and registering the skil in the resources.py module. The rest is magic.

e.g. (skill)
    
    class CalcSkill(SkillBase):
        def __init__(self):
            self.application_id = 'amzn1.echo-sdk-ams.app.0ca6438a-f5b1-4a47-89fc-12aa0393a565'
    
            self.register_intents([
                (r'AddIntent', self.add_value),
                (r'SubtractIntent', self.subtract_value),
                (r'GetValueIntent', self.get_total),
                (r'AMAZON.HelpIntent', self.get_welcome_response),
                (r'AMAZON.CancelIntent', self.handle_session_end_request),
                (r'AMAZON.StopIntent', self.handle_session_end_request),
            ])
    
        # methods here

e.g. (resources)
    
    aws_skills = [
        (r'aws/calc$', CalcSkill),
    ]

# Setup

I don't really buy into the "production" v. "development" setup stuff. Your setups should always be production-style. This means that your .NET development should be with IIS, your Python development should be with Nginx (or Apache for those who like old stuff), and your production setups should be VERY easy to debug (the primary reason I keep minification as a **runtime**, not a **deployment** feature). Thus, the following may seem overkill. I don't care.

Using **Azure** Web App? Just do git push. Everything should be setup already. Azure will see the runtime.txt and do magical things.

Using **Azure** ARM template? Niiiiice! There are deploy templates in the deploy/folder. You can run something like the following to make things happen:

    azure group create --location centralus --name lab01
    azure group deployment create --name elephant01 --template-file azuredeploy.json  --parameters-file azuredeploy-parameters.json --resource-group lab01
    
For full details on this, head over to my [Linux on Azure website](https://linux-azure.david.betz.space/_/python-uwsgi-nginx).

This will setup all the epic IAAS stuff and run install.sh to setup all the software.

Using your own hosting? Cool. Checkout [install.sh](https://linux-azure.david.betz.space/python-uwsgi-nginx/install) for full details. It's designed for **CentOS**. However, below is some commentary...

Apache directly contradicts the general philosophy of Linux where tools do few things, but do them well. In modern Python hosting, UWSGI does the Python processing and Nginx serves the HTTP content.

Here is an excellent explanation of the general setup:

 * [How to Deploy Python WSGI Applications Using uWSGI Web Server with Nginx](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-uwsgi-web-server-with-nginx)

## Nginx
    
    server {
        listen 10.1.40.10:80;
    
        location /favicon.ico {
            alias /srv/favicon.ico;
        }
    
        location / {
            include            uwsgi_params;
            uwsgi_pass         unix:/srv/api_server/content/content.sock;
    
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
    }

## uWSGI
    
    [uwsgi]
    project = content
    base = /srv/api_server/content
    virtualenv = /srv/api_server
    
    chdir = %(base)
    home = %(virtualenv)
    module = app:app
    
    master = true
    processes = 5
    
    socket = %(base)/%(project).sock
    chmod-socket = 666
    uid = dbetz
    gid = nginx
    vacuum = true
    
    plugins = python

## Python

Python is uniquitous. It's powerful enough for the most advanced scenarios and it's simple enough for "programming for kids" books. I know Node.js is still the hot stuff to talk about, and we all need to be able to handle it, but every .NET developer should also have Python in his/her toolbelt. So, that's assumed. 

Remember to create a virtual environment, *activate the environment*, and install the pip packages. This is easy to forget.
    
    $ cd /srv
    
    $ virtualenv -p python3 api_server
    $ # use 'virtualenv api_server' for legacy Python (aka Python2)
    
    $ cd api_server

    $ source bin/active
    
    $ git clone https://github.com/davidbetz/pywebapi
    
    (completely optional, it's just what I name my app)
    $ mv pywebapi content
    
    $ cd content
    
    $ pip install -r requirements.txt

## SELinux

CentOS/RedHat are for use in non-home environments. If you are a business, you will be using RedHat or CentOS. These systems have security built right into the kernel, at a level even lower than root. This is SELinux and you have to deal with it. You don't turn it off; you learn it.

There are a lot of places to learn SELinux and mandatory access control, here is one place to start:

  * [An Introduction to SELinux on CentOS 7 – Part 1: Basic Concepts](https://www.digitalocean.com/community/tutorials/an-introduction-to-selinux-on-centos-7-part-1-basic-concepts)

What follows are tips to help you setup security properly. The gist is this: service programming files (e.g. Python) should be in `/srv`. This isn't the default. You have to tell SELinux you want these files to be labeled in such a way that UWSGI/Nginx can access them. Also, you need to tell the kernel that you want Nginx to be able to serve content. This security is much tighter than a mere firewall.

Monitor the following for errors:
    
    sudo tail -f /var/log/audit/audit.log
    sudo tail -f /var/log/nginx/error.log
    sudo tail -f /var/log/messages

You will most likely have to enable nginx in selinux:
    
    sudo setsebool -P httpd_can_network_connect 1

Also, probably set SELinux file labels:
    
    sudo semanage fcontext -at httpd_sys_content_t "/srv(/.*)?"
    sudo restorecon -R -v /srv 

Also, give extra rights to Nginx in selinux:

    # these tell you what's wrong, if anything
    sudo audit2why -a
    sudo audit2allow -wa
    
    # this allows Nginx to serve content by create and adding a new module to the kernel
    cd /srv
    sudo audit2allow -a -M nginx_sock
    semodule -i nginx_sock.pp

However, install/deploy.sh showed a more production-oriented method for your security setup. In there I already know what SELinux wants; I'm not asking it for details via `audit2allow`.

# Usage

## Command Line (no server)

    # mainly just for development
    uwsgi --emperor /etc/uwsgi.d --uid dbetz --gid nginx --touch-reload app.py

## Tests
    
    # test_app.py is the core test
    
    python test_app.py
    python test_item.py
    python test_azure.py
    
    # the following is for AWS skills
    
    python test_app_aws.py

## Samples

    curl -i -X POST 'http://10.1.40.10/item/5' -d 'asdfasdf' -H 'Accept: application/json'
    curl -i -X POST 'http://10.1.40.10/item/5' -d '{ "id": 5, "name": "item5", "content": "qwerwqer5" }'
    curl -i -X POST 'http://10.1.40.10/item/4' -d '{ "id": 400, "name": "item4", "content": "after test update" }'
    curl -i -X POST 'http://10.1.40.10/item' -d '{ "id": 5, "name": "item5", "content": "qwerwqer5" }'
    
    curl -i -X PUT 'http://10.1.40.10/item/4' -d '{ "id": 400, "name": "item4", "content": "after test update" }'
    curl -i -X PUT 'http://10.1.40.10/item' -d '{ "id": 400, "name": "item4", "content": "after test update" }'
    
    curl -i -X DELETE 'http://1.1.40.10/item/3'
    
    curl -i -X GET 'http://10.1.40.10/item?pretty' -H 'Accept: application/json'
    curl -i -X GET 'http://10.1.40.10/item/40' -H 'Accept: application/json'
    curl -i -X GET 'http://10.1.40.10/item/4' -H 'Accept: application/json'
