#!/usr/bin/python
# -*- coding: utf-8 -*-
#assume pythong 2.7
import os,fnmatch,hashlib,base64,subprocess,argparse
from shutil import copyfile
#
# Global Variable  Config
#

#where 3cx html files are located
w3root = "/var/lib/3cxpbx/Data/Http/wwwroot/" #for real action
w3root = "./wwwroot/"  #for local test

#old new logo and background image in png format
newlogo = "./newlogo.png"
newBackground = "./newbackground.png"
oldlogo = "./3cxlogo.png"
oldBackground = "./3cxbackground.png"

#strings needs to be changed within the html
word_dict ={
    "Welcome to the 3CX Web Client" : "SMS,Chat,Video Service Login",
    "http://www.3cx.com":"http://biukop.com.au",
    "https://www.3cx.com":"https://biukop.com.au",
    "欢迎访问3CX控制面板":"欢迎访问控制台",
    "Welcome to the 3CX Management Console":"Authorized user Login",
    "3CX Phone System Management Console": "Biukop Phone Console",
    "3CX Phone System Webclient" : "Biukop Conference WebClient",
    "3CX Webclient" : "Biukop Webclient"
}

#fav.ico old and new
newico = "./biukop-letterB.ico"
oldico = "favicon.ico"
#
#
#
#
#
#
#
#
# programs below should not be edited unless you know the logic
#
#
#
#
#
#
########  functions ############
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def loadLogo(fname):
    with open (fname, 'r') as f: 
        s = f.read()
        return s

def installBkLogo(path,newlogo):
    files = find("logo*.png",path)
    for f in files:
        print newlogo , "->", f
        copyfile(newlogo, f)

def changeFavIco(path, newIco):
    files = find("favicon.ico", path)
    for f in files:
        print newico , "->", f
        copyfile(newico,f)

def replaceTxt(fname,old,new):
    with open(fname) as f:
        s = f.read().replace(old,new)
    with open(fname, "w") as f: 
        f.write(s)

def getw3root():
    global w3root
    parser = argparse.ArgumentParser(description='Get customized w3root')
    parser.add_argument('-w','--webroot3cx', nargs='?',dest='webroot3cx',help="specify webroot of 3cx, default /var/lib/3cxpbx/Data/Http/wwwroot/", action='store', required=False, const=str)
    args = parser.parse_args()
    if args.webroot3cx is not None :
        w3root = args.webroot3cx
####### main logic ###############
getw3root()
print "3cxwebroot is set to" , w3root
if (not os.path.isdir(w3root)):
    print "the directory does not exist"
    exit()
curdir = os.path.dirname(os.path.realpath(__file__))
print "change to working directory", curdir
os.chdir(curdir)
#
# Convert to base 64
#
b64OldLogo = base64.b64encode(loadLogo(oldlogo))
b64OldBackground = base64.b64encode(loadLogo(oldBackground))
b64NewLogo = base64.b64encode(loadLogo(newlogo))
b64NewBackground =base64.b64encode(loadLogo(newBackground))

#txtBg = loadLogo("bg.txt")
#if b64OldBackground != txtBg:
#    print "suck it is not equal"
#    with open("oldbg.txt", "w") as f:
#        f.write(b64OldBackground)
#    with open("txtbg.txt", "w") as f:
#        f.write(txtBg)
#    exit()
#
#step 1. overwrite logo pictures
installBkLogo(w3root, newlogo)


#step 2. overwrite logo src base64
for root,dirs,files in os.walk(w3root):
    for f in files:       
        changed = False
        fname = os.path.join(root,f)
        fcontent = open(fname,"rb").read()

#       step3 replace 3cx text to biukop welcome,before gzip
        for key in word_dict:
            if key in fcontent:
                print key,"->",word_dict[key]," in ", fname
                fcontent = fcontent.replace(key,word_dict[key])
                changed = True

        if b64OldLogo in fcontent:
            print "logo :", fname
            fcontent = fcontent.replace(b64OldLogo, b64NewLogo)
            changed = True

        if b64OldBackground in open(fname).read():
            print "bg  :",fname 
            fcontent = fcontent.replace(b64OldBackground, b64NewBackground)
            changed = True
        if changed :
            with open(fname, "wb") as f:
                f.write(fcontent)

        #compress js to gz and preserve js file
        if fname.endswith('.js') or fname.endswith('.css') :
            subprocess.call(["gzip","-fk",fname]); 

        if f == oldico:
            print newico, "->", fname
            copyfile(newico,fname)


#step4 change fav.ico

