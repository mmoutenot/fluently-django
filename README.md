fluently
======================

Local Setup
-----------
Clone the remote repository

    git clone https://github.com/mmoutenot/fluently-django.git
    cd fluently-django

Create virtual python environment and install dependencies. You want to pipe that echo line into whatever shell config you use.

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

Modify your .git/config to be:

    [core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
        ignorecase = true
        precomposeunicode = false
    [remote "origin"]
        url = https://github.com/mmoutenot/fluently-django.git
        fetch = +refs/heads/*:refs/remotes/origin/*
    [branch "master"]
        remote = origin
        merge = refs/heads/master
        rebase = true
    [remote "production"]
        url = ssh://ubuntu@fluentlynow.com:22/home/ubuntu/fluently-django.git

Install postgresql (I know this is scary, but trust me?). You need brew installed (simple google).

    bash < <(curl -s http://www.solowizard.com/soloist_scripts/jiagb2.sh )

Alternatively you can just use sqlite by modifying the databse section in /settings.py to be the following:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'fluently.db',            # Or path to database file if using sqlite3.
            'USER': '',            # Not used with sqlite3.
            'PASSWORD': '',          # Not used with sqlite3.
            'HOST': '',            # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',            # Set to empty string for default. Not used with sqlite3.
        }
    }

Developing
------------
When you're developing, run these two commands:

    sass --watch stylesheets/sass:stylesheets

and

    python manage.py runserver_socketio

The first will actively watch and convert your sass to css and the second runs the django server. The django server automatically restarts when changes are made to the .py files. If, however you add a new file, or make a change to settings.py you have to restart the server.

The latter is the only one needed to just view the site. You can see it at http://localhost:9000
