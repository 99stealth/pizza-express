# Automated way to test and deploy pizza-express project
### What it does
* Runs   unit-tests,   makes   sure   they   are   passing
* Package   the   application   as   a   docker   image
* Runs   the   container   and   checks   that   service:8081   returns   HTTP
STATUS   CODE   200.
* Sends   the   docker   image   to   any   account   in   Docker   hub   and   tags
it   as   latest.
___
### What do you need to run it
In order to run automated testing and deployment you need to have installed 
* Python (version 2.7)
* Python PIP
* Decker (version 17)
After you cloned current repository and installed needed software you should install required libraries for `python`
```bash
pip install -r requirements.txt
```
___
### Run automation
If `deploy.py` is not executable run:
```bash
chmod +x deploy.py
```
Now run `deploy.py`. There are several arguments that must be provided when script is launching:
* --username (Username for docker registry)
* --password (User's password)
* --repository (Repository where container should be committed)
```
./deploy.py --username user --password U$3r$_Pa$$w0rd --repositoroy user/pizza-express
```
**Please pay attention!** Verbosity is disabled by default. If you want to see more output try to use flag **-v** or **--verbose**

For more details about `deploy.py` run:
```bash
./deploy.py --help
``` 