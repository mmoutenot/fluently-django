fluently
======================

Local Setup
-----------
Clone the remote repository

    git clone https://github.com/mmoutenot/fluently-django.git
    cd fluently-django

Create virtual python environment and install dependencies

    sudo easy_install pip
    sudo pip install virtualenv
    virtualenv .venv
    cp bin/.virtualenv-auto-activate.sh ~/
    echo "source ~/.virtualenv-auto-activate.sh" >> ~/.bashrc
    cd ../fluently-django

Ensure that the virtual environment is activated

    which pip

  Should display ~/.../.../fluently-django/.venv/blah/blah/pip

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
        url = https://github.com/mmoutenot/fluently-django.git
    [branch "master"]
        remote = origin
        merge = refs/heads/master
    [remote "web"]
        url = todo
        fetch = +refs/heads/*:refs/remotes/web/*

Install postgresql (I know this is scary, but trust me?)

    bash < <(curl -s http://www.solowizard.com/soloist_scripts/jiagb2.sh )


Remote Setup
------------
TODO


Developing
------------
When you're developing, run these two commands:

    sass --watch stylesheets/sass:stylesheets

and

    python manage.py runserver

The first will actively watch and convert your sass to css and the second runs the django server. The django server automatically restarts when changes are made to the .py files. If, however you add a new file, or make a change to settings.py you have to restart the server.


