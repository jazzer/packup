## Install

##### Requirements
    sudo apt-get install git python3 

##### Get the Code

change do your prefered path with cd, then

    git clone git://github.com/jazzer/packup.git
    cd packup
    mv data-example.py data.py
    gedit data.py


## What now?

##### Add an Alias

To make running a backup as convinient as possible, you can define an alias in
~/.bash_aliases like so: 

    alias backup='sudo ~/Software/Backup/packup/packup.py' (use your own path)

After 

    source ~/.bashrc

a backup can be run by typing

    backup

to the terminal.


##### No Password

Run

    sudo visudo

and add

    # enable password-less backup
    johannes        ALL=(ALL)NOPASSWD:/home/johannes/Software/Backup/packup/packup.py

while of course replacing your username and path. Exit vi(m) by typing :x and 
return.
