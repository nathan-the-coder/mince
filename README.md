<p align="center">
  <a href="https://github.com/paradise-theme/paradise/stargazers"><img src="https://img.shields.io/github/stars/nathan-the-coder/QLang?colorA=151515&colorB=B66467&style=for-the-badge&logo=starship"></a>
  <a href="https://github.com/paradise-theme/paradise/issues"><img src="https://img.shields.io/github/issues/nathan-the-coder/QLang?colorA=151515&colorB=8C977D&style=for-the-badge&logo=bugatti"></a>
  <a href="https://github.com/paradise-theme/paradise/network/members"><img src="https://img.shields.io/github/forks/nathan-the-coder/QLang?colorA=151515&colorB=D9BC8C&style=for-the-badge&logo=github"></a>
</p>

Ql Programming Language written in Python

### Examples
```
* hello.ql

* TODO: BETTER SYNTAX
DEFINE MAIN % 
  PRINT "Hello World\n" 
%

* run the function main
RUN MAIN 

foo = 0
bar = 1 

test = 1
IF test == 1 %
  PRINT "Yes\n"
% ELSE %
  PRINT "No\n"
%
```

#### More examples in 
[examples](./examples/)

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
