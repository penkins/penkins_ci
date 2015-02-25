PENKINS
=======

WTF is Penkins?!
----------------

Penkins is a very small and easy to use continuous integration (CI) tool,
like Jenkins =), but Jenkins written in Java and Penkins in Python.

Penkins created special for small PHP or Python projects. For big projects use Jenkins better.

![Mr. Penkins](https://avatars1.githubusercontent.com/u/7437554?v=2&s=500)


Installation
------------

```
# apt-get install supervisor
# apt-get install python-pip
# apt-get install python-git
# apt-get install python-yaml
# pip install mercurial
```

```
# wget https://github.com/vanzhiganov/penkins/archive/master.zip
# unzip master.zip
# cp -r penkins-master/ /var/lib/penkins
# cd /var/lib/penkins/
# cp extra/supervisor.conf /etc/supervisor/conf.d/penkins.conf
# supervisorctl reload
```


Configuration
-------------

## Example configuration

```
work: update
vcs: git
repository: git@github.com:vanzhiganov/penka.git
before: [echo 'before']
after: [echo 'after']
build_count: 4
path: build/test/4
```

Description

`vcs`: `git` or `mercurial`

`repository`: url or path to repository

`before`: CLI command executed before repository updated

`after`: CLI command executed after repository updated

`build_count`: auto incremental counter

`path`: path to repository cloning. if using `work: build` then path build automatically like `build/test/4`. if using `work: update` then path stay not changed `build`.

## Supervisor configuration

```
[program:penkins]
directory=/var/lib/penkins
autostart=true
autorestart=true
startsecs=1
startretries=777
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=1
user=www-data
group=www-data
command=manage.py
redirect_stderr=false

stdout_logfile=/var/log/penkins_out.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=10
stdout_capture_maxbytes=10MB

stderr_logfile=/var/log/penkins_err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=10MB
```


## Configuration for work with Mercurial

Create `.hgrc` file in home directory. For example under user `root`:

`touch /root/.hgrc`

and put

```
[auth]
bb.prefix = https://bitbucket.org
bb.username = {username}
bb.password = {password}
```

or

```
[auth]
bb1.prefix = https://bitbucket.org/foo/
bb1.username = foo
bb1.password = foo_passwd

bb2.prefix = https://bitbucket.org/bar/
bb2.username = bar
bb2.password = bar_passwd
```

or

```
[auth]
bb.prefix = bitbucket.org
bb.username = foo
bb.password = foo_passwd
bb.schemes = http https
```

