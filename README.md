# QLang
Ql Programming Language written in Python

SERVER:


![server.png](./screenshots/server.png)


EXAMPLE:


![hello.png](./screenshots/hello.png)

Implementation
  Default: [Python](https://python.org)


> ### NEW
>  1. added [setup.py](./setup.py) to install additional modules and the python script itself.
>  2. added [log.py](./scripts/log.py) - used for pretty printing error's, warning's and to print msg.
>  3. added [shop.py](./scripts/shop.py) - used to run shell commands in python and used in [setup.py](./setup.py). 
>  4. added [git.py](./scripts/git.py) - used to add more git integration to ql.
>  5. fixes the server functions to work properly
>  6. Successfully Implemented First git integration 



```ql
* Cloning the repo
GIT::CLONE "git, gitlab..." "user/repo"

```


## Disclaimer
> you need to be on the directory, where the server will be for ql to gen files on that dir only
