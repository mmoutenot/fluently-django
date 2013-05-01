fluently
======================

Local Setup
-----------
Clone the remote repository

    git clone https://github.com/mmoutenot/fluently-django.git
    cd fluently-django

Create virtual python environment and install dependencies

    sudo easy_install pip
    virtualenv
    virtualenv .venv
    cp tools/.virtualenv-auto-activate.sh ~/
    echo "source ~/.virtualenv-auto-activate.sh" >> ~/.bashrc
    cd ../fluently

Ensure that the virtual environment is activated

    which pip

  Should display ~/.../.../fluently/.venv/blah/blah/pip

    pip install -r requirements.txt

Modify your .gitconfig to be:

    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
    [remote "origin"]
        fetch = +refs/heads/*:refs/remotes/origin/*
        url = https://github.com/mmoutenot/pinhack-django.git
    [branch "master"]
        remote = origin
        merge = refs/heads/master
    [remote "web"]
        url = todo
        fetch = +refs/heads/*:refs/remotes/web/*

Install Redis:

    curl -O http://redis.googlecode.com/files/redis-2.6.8.tar.gz
    tar xzf redis-2.6.8.tar.gz
    cd redis-2.6.8
    make

Copy Redis init scripts:

    sudo cp src/redis-server /usr/local/bin/
    sudo cp src/redis-cli /usr/local/bin/


Remote Setup
------------
TODO
