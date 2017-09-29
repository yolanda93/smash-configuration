import os
import time
# periodically check if smashbox is running

threshold = 10000000000

result = int(os.popen("du -b ./smashbox/etc/smashdir").read().split("\t")[0])

if(result>threshold):
   shutil.rmtree("./smashbox/etc/smashdir")
   # to do backup test results and update smashbox repository



os.system("python ./smashbox/bin/smash --keep-going -a /smashbox/lib/")
