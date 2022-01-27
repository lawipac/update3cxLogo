# update3cxLogo
update 3cx log and text to Biukop related branding

# usage on Development Machine
./deploy.sh

It will copy files to remote ```/root/change3cxlogo/```, and then execute command through ssh

# usage on Remote 3cx machine
under ```/root/change3cxlogo/```  directory 

Run following command
``` # ./localDeploy.sh ```

it's essentially the last step of remote running on development machine.

# caveats
#hardcode to cc.biukop.com.au
#

Example running scenario
```bash
root@cc:~# git clone https://github.com/lawipac/update3cxLogo.git
Cloning into 'update3cxLogo'...
remote: Enumerating objects: 76, done.
remote: Counting objects: 100% (25/25), done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 76 (delta 5), reused 24 (delta 4), pack-reused 51
Unpacking objects: 100% (76/76), done.
root@cc:~# cd update3cxLogo/
root@cc:~/update3cxLogo# dir
3cxbackground.png  biukop-letterB.ico  localDeploy.sh  newbackground.png  newlogo.svg  wwwroot.tb2
3cxlogo.png        deploy.sh           main.py         newlogo.png        README.md
root@cc:~/update3cxLogo# ls -l
total 16596
-rw-r--r-- 1 root root     8760 Jan 27 23:03 3cxbackground.png
-rw-r--r-- 1 root root     7622 Jan 27 23:03 3cxlogo.png
-rw-r--r-- 1 root root     2288 Jan 27 23:03 biukop-letterB.ico
-rwxr-xr-x 1 root root      330 Jan 27 23:03 deploy.sh
-rw-r--r-- 1 root root      103 Jan 27 23:03 localDeploy.sh
-rwxr-xr-x 1 root root     5077 Jan 27 23:03 main.py
-rw-r--r-- 1 root root    62590 Jan 27 23:03 newbackground.png
-rw-r--r-- 1 root root     9903 Jan 27 23:03 newlogo.png
-rwxr-xr-x 1 root root    10211 Jan 27 23:03 newlogo.svg
-rw-r--r-- 1 root root      201 Jan 27 23:03 README.md
-rwxr-xr-x 1 root root 16859095 Jan 27 23:03 wwwroot.tb2
root@cc:~/update3cxLogo# chmod +x localDeploy.sh
root@cc:~/update3cxLogo# ./localDeploy.sh
3cxwebroot is set to /var/lib/3cxpbx/Data/Http/wwwroot/
change to working directory /root/update3cxLogo
./newlogo.png -> /var/lib/3cxpbx/Data/Http/wwwroot/webclient/assets/img/logo.png
./newlogo.png -> /var/lib/3cxpbx/Data/Http/wwwroot/webclient/assets/img/logo152x72.png
./newlogo.svg -> /var/lib/3cxpbx/Data/Http/wwwroot/webclient/assets/manifest/3cx_logo.svg
./newlogo.svg -> /var/lib/3cxpbx/Data/Http/wwwroot/fonts/3cx_logo.9e910064.svg
./biukop-letterB.ico -> /var/lib/3cxpbx/Data/Http/wwwroot/favicon.ico
root@cc:~/update3cxLogo#
```