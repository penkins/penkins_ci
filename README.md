PENKINS
=======

WTF is Penkins?!
----------------

Penkins is a very small and easy to use continuous integration (CI) tool,
like Jenkins =), but Jenkins written in Java and Penkis in Python.

Penkins created special for small PHP or Python projects. For big projects use Jenkins better.


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

Example configuration

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