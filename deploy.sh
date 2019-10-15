#!/bin/bash
REMOTE='/root/change3cxlogo'
echo "make $REMOTE"
ssh root@cc.biukop.com.au "mkdir -p $REMOTE"
echo "copy *.png *.ico main.py"
scp *.png *.ico main.py root@cc.biukop.com.au:$REMOTE/
echo "run update for remote machine"
ssh root@cc.biukop.com.au "python $REMOTE/main.py --webroot3cx /var/lib/3cxpbx/Data/Http/wwwroot/" 
