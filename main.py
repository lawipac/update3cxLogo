#!/usr/bin/python
# -*- coding: utf-8 -*-
# assume pythong 2.7
import os, fnmatch, hashlib, base64, subprocess, argparse
from shutil import copyfile

#
# Global Variable  Config
#

# where 3cx html files are located
w3root = "/var/lib/3cxpbx/Data/Http/wwwroot/"  # for real action
w3root = "./wwwroot/"  # for local test

# old new logo and background image in png format
newlogo = "./newlogo.png"
newBackground = "./newbackground.png"
oldlogo = "./3cxlogo.png"
oldBackground = "./3cxbackground.png"

# strings needs to be changed within the html
word_dict = {
    "Welcome to the 3CX Web Client": "SMS,Chat,Video Service Login",
    "http://www.3cx.com": "http://biukop.com.au",
    "https://www.3cx.com": "https://biukop.com.au",
    "欢迎访问3CX控制面板": "欢迎访问控制台",
    "Welcome to the 3CX Management Console": "Authorized user Login",
    "3CX Phone System Management Console": "Biukop Phone Console",
    "3CX Phone System Webclient": "Biukop Conference WebClient",
    "3CX Webclient": "Biukop Webclient",
    "M17.87 20.557c1.2-.1 2.3-.4 3.3-.8s1.9-1.1 2.5-1.9c.7-.8 1-1.9 1-3.3 0-2-.7-3.6-2-4.7-1.4-1.1-2.9-1.6-4.7-1.6-2.4 0-4.3.8-5.5 2.4s-1.8 3.6-1.8 6.1h-9.2c.1-2.4.5-4.7 1.3-6.7s1.9-3.7 3.3-5.2c1.4-1.4 3.1-2.6 5.1-3.3 2-.8 4.2-1.2 6.7-1.2 1.9 0 3.8.3 5.7.9s3.6 1.4 5.1 2.6c1.5 1.1 2.8 2.5 3.7 4.1 1 1.6 1.4 3.5 1.4 5.6 0 2.3-.6 4.4-1.7 6.1-1.1 1.8-2.8 3-5 3.6v.1c2.6.6 4.7 1.9 6.2 3.8s2.2 4.3 2.2 7c0 2.5-.5 4.7-1.5 6.7s-2.3 3.6-3.9 4.9c-1.6 1.3-3.5 2.3-5.6 3s-4.4 1-6.7 1c-2.7 0-5.1-.4-7.3-1.2-2.2-.8-4.1-1.9-5.6-3.4s-2.7-3.3-3.6-5.4c-.8-2.1-1.2-4.6-1.2-7.3h9.2c0 1.3.2 2.5.6 3.6.4 1.2.9 2.2 1.6 3 .7.8 1.5 1.5 2.6 2 1 .5 2.2.7 3.6.7 2.2 0 4-.7 5.5-2s2.3-3.2 2.3-5.5c0-1.8-.4-3.2-1.1-4.1-.7-1-1.6-1.6-2.7-2.1-1.1-.4-2.3-.7-3.6-.7-1.3-.1-2.5-.1-3.7-.1v-6.8c1.2.1 2.3.1 3.5.1z": " ",
    "M63.57 6.557c5.4 0 10.7 2.2 14.6 6l1 1v-8.2l-.3-.2c-4.5-3.1-9.4-4.7-15.1-4.7-14.5 0-26.3 11.1-26.3 24.8 0 13.5 11.8 24.4 26.3 24.4 5.3 0 10.6-1.7 15.1-4.7l.3-.2v-8.1l-1 1c-4 3.8-9.3 6-14.5 6-10.5 0-19.4-8.5-19.4-18.6.1-10 8.9-18.5 19.3-18.5z": " ",
    "M79.37 15.757v19l8.3-9.9z": " ",
    "m129.67 49.357-19.6-23.9 19.6-23.8h-10.4l-14.3 17.5-14.3-17.5h-10.4l19.5 23.8-19.5 23.9h10.3l14.4-17.6 14.4 17.6zm1.3-2.7c0-1.5 1.2-2.7 2.7-2.7s2.7 1.2 2.7 2.7-1.2 2.7-2.7 2.7c-1.5 0-2.7-1.2-2.7-2.7zm4.9 0c0-1.3-1-2.3-2.3-2.3-1.2 0-2.3 1-2.3 2.3s1 2.3 2.3 2.3 2.3-1 2.3-2.3zm-1 1.4h-.5l-.9-1.3h-.5v1.3h-.4v-2.9h1.3c.5 0 1 .1 1 .8 0 .6-.4.8-.9.8l.9 1.3zm-1.3-1.7c.4 0 1 .1 1-.4 0-.3-.4-.4-.7-.4h-.8v.8h.5z": ""
}

# fav.ico old and new
newico = "./biukop-letterB.ico"
oldico = "favicon.ico"

# 3cx adopted svg log for version 18 and later
oldSvgLogo = "./3cxlogo.svg"
newSvgLogo = "./newlogo.svg"

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
    with open(fname, 'r') as f:
        s = f.read()
        return s


def installBkLogo(path, newlogo):
    files = find("logo*.png", path)
    for f in files:
        print newlogo, "->", f
        copyfile(newlogo, f)


def installSvgLogo(path, newLogo):
    files = find("3cx_logo*.svg", path)
    for f in files:
        print newLogo, "->", f
        copyfile(newLogo, f)


def changeFavIco(path, newIco):
    files = find("favicon.ico", path)
    for f in files:
        print newico, "->", f
        copyfile(newico, f)


def replaceTxt(fname, old, new):
    with open(fname) as f:
        s = f.read().replace(old, new)
    with open(fname, "w") as f:
        f.write(s)


def getw3root():
    global w3root
    parser = argparse.ArgumentParser(description='Get customized w3root')
    parser.add_argument('-w', '--webroot3cx', nargs='?', dest='webroot3cx',
                        help="specify webroot of 3cx, default /var/lib/3cxpbx/Data/Http/wwwroot/", action='store',
                        required=False, const=str)
    args = parser.parse_args()
    if args.webroot3cx is not None:
        w3root = args.webroot3cx


####### main logic ###############
getw3root()
print "3cxwebroot is set to", w3root
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
b64OldSvgLogo =  base64.b64encode(loadLogo(oldSvgLogo))
b64OldBackground = base64.b64encode(loadLogo(oldBackground))


b64NewLogo = base64.b64encode(loadLogo(newlogo))
b64NewSvgLogo = base64.b64encode(loadLogo(newSvgLogo))
b64NewBackground = base64.b64encode(loadLogo(newBackground))


# txtBg = loadLogo("bg.txt")
# if b64OldBackground != txtBg:
#    print "suck it is not equal"
#    with open("oldbg.txt", "w") as f:
#        f.write(b64OldBackground)
#    with open("txtbg.txt", "w") as f:
#        f.write(txtBg)
#    exit()
#
# step 1. overwrite logo pictures
installBkLogo(w3root, newlogo)
installSvgLogo(w3root, newSvgLogo)

# step 2. overwrite logo src base64
for root, dirs, files in os.walk(w3root):
    for f in files:
        changed = False
        fileName = os.path.join(root, f)
        fileContent = open(fileName, "rb").read()

        #  step3 replace 3cx text to biukop welcome,before gzip
        for key in word_dict:
            if key in fileContent:
                print key, "->", word_dict[key], " in ", fileName
                fileContent = fileContent.replace(key, word_dict[key])
                changed = True

        if b64OldLogo in fileContent:
            print "logo :", fileName
            fileContent = fileContent.replace(b64OldLogo, b64NewLogo)
            changed = True

        if b64OldBackground in open(fileName).read():
            print "bg  :", fileName
            fileContent = fileContent.replace(b64OldBackground, b64NewBackground)
            changed = True

        if b64OldSvgLogo in fileContent:
            print "logo :", fileName
            fileContent = fileContent.replace(b64OldSvgLogo, b64NewSvgLogo)
            changed = True

        if changed:
            with open(fileName, "wb") as f:
                f.write(fileContent)

        # compress js to gz and preserve js file
        if fileName.endswith('.js') or fileName.endswith('.css'):
            subprocess.call(["gzip", "-fk", fileName]);

        if f == oldico:
            print newico, "->", fileName
            copyfile(newico, fileName)

# step4 change fav.ico
