#!/usr/bin/python
#assume pythong 2.7
import os,fnmatch,hashlib,base64,subprocess
from shutil import copyfile
# Global Variable  Config
w3root = "/var/lib/3cxpbx/Data/Http/wwwroot/" #for real action
w3root = "./wwwroot/"  #for local test
newlogo = "./newlogo.png"
newBackground = "./newbackground.png"
oldlogo = "./3cxlogo.png"
oldBackground = "./3cxbackground.png"
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
        s = f.read().replace('\n','')
        return s

def installBkLogo(path,newlogo):
    files = find("logo*.png",path)
    for f in files:
        print newlogo , "->", f
        copyfile(newlogo, f)

def replaceTxt(fname,old,new):
    with open(fname) as f:
        s = f.read().replace(old,new)
    with open(fname, "w") as f: 
        f.write(s)
####### main logic ###############3
if w3root == "./wwwroot/":
    print "w3root is development root" , w3root 
#
# Convert to base 64
#
b64OldLogo = "data:image/png;base64," + base64.b64encode(open(oldlogo,"rb").read())
b64OldBackground = "data:image/png;base64," + base64.b64encode(open(oldBackground,"rb").read())
b64NewLogo = "data:image/png;base64," + base64.b64encode(open(newlogo,"rb").read())
b64NewBackground = "data:image/png;base64," + base64.b64encode(open(newBackground,"rb").read())
word_dict = dict()
word_dict["Welcome to the 3CX Web Client"] = "SMS,Chat,Video Service Login"
word_dict["\"http://www.3cx.com\""]="\"http://biukop.com.au/\""
word_dict["Welcome to the 3CX Management Console"]="Authorized user Login"
#step 1. overwrite logo pictures
installBkLogo(w3root, newlogo)


#step 2. overwrite logo src base64
for root,dirs,files in os.walk(w3root):
    for f in files:       
        fname = os.path.join(root,f)
#       step3 replace 3cx text to biukop welcome,before gzip
        for key in word_dict:
            if key in open(fname).read():
                print key,"->",word_dict[key]," in ", fname
                replaceTxt(fname,key,word_dict[key])

        if b64OldLogo in open(fname).read():
            print "logo :", fname
            replaceTxt(fname, b64OldLogo, b64NewLogo)
            subprocess.call(["gzip","-fk",fname]); 

        if b64OldBackground in open(fname).read():
            print "bg  :",fname 
            replaceTxt(fname, b64OldBackground, b64NewBackground)
            subprocess.call(["gzip","-fk",fname]); 


