django-fluentd allows you to use django's logging framework to log directly to a fluentd server of your choice.

Please consider the package as unstable and don't use it for production, yet.

== Installation ==

= Using pip & PyPi =
pip install django-fluentd

= Using setup.py ==
git clone #Todo add clone url
cd django-fluentd
python setup.py install

== Configuration ==

Add the following to your settings.py:

DJANGO_FLUENTD_SERVER = "10.10.10.10"
DJANGO_FLUENTD_PORT = 24224 #no string
DJANGO_FLUENTD_TAG = "your_fluentd_tag"

Add the fluentd handler to your LOGGING dict in your settings.py and add this handler to one of your loggers

LOGGING = {
    ...

    'handlers':{
        'fluentd': {
            'level': 'DEBUG',
            'class': 'django_fluentd.handler.FluentdHandler',
        },
    }

    ...

    'loggers': {
        'django': {
            'handlers': ['fluentd',],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

If you want to capture all logging messages using fluentd, you can add a root handler

LOGGING = {
  ...

  'root': {
        'level': 'DEBUG',
        'handlers': ['fluentd'],
    },

  ...
}

Further information on how to use django's logging framework can be found here: https://docs.djangoproject.com/en/dev/topics/logging/

== Fluentd Server Setup ==

Your Fluentd Server should listen on the ip and the port you specified in DJANGO_FLUENTD_SERVER and DJANGO_FLUENTD_PORT:

<source>
 type forward
 port 24224
 bind 10.10.10.10
</source>

Please not that you currently can't use fluentd's secure_forward. If you want to send encrypted or authenticated messages
to another fluentd server on the net, you'll have to add a local fluentd server that accepts unencrypted messages and forwards
them using secure_forward:

<source>
 type forward
 port 24224
 bind 10.10.10.10
</source>

<match **>
  type secure_forward
  shared_key foobar
  self_hostname example.org
  send_timeout 60s
  recover_wait 10s
  heartbeat_interval 1s
  phi_threshold 8
  hard_timeout 60s

  <server>
    name remote_server_name
    host 10.10.10.11
    port 24224
    username your_username
    password your_password
  </server>

</match>

Further information on how to use fluentd can be found here: http://fluentd.org/


