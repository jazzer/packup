## Install

This was written and tested for Ubuntu Oneiric Ocelot (11.10).
It should work **very** similar for every other recent and decent Linux distribution.

##### Requirements
Install Git and python3 if they are not available yet:

    sudo apt-get install git python3 

##### Get the Code

Change do your prefered path with cd, then run these commands:

    git clone git://github.com/jazzer/packup.git
    cd packup
    mv data-example.py data.py
    gedit data.py


## What now?

##### Add an Alias

To make running a backup as convinient as possible, you can define an alias in
~/.bash_aliases like so: 

    alias backup='sudo ~/Software/Backup/packup/packup.py' (use your own path)

After issuing

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

whilst of course replacing your username and path. Exit vi(m) by typing :wq and 
return.



## License

This work is released under the CC0 license (see http://creativecommons.org/publicdomain/zero/1.0/legalcode for details).
It means you can use this for whatever purpose seems right for you. Enjoy!

Nevertheless I'd be happy to hear from you in case you use or improve the code in real life!
