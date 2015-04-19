#!/usr/bin/env python
# dtimg2dtb
# Copyright 2015 wuxianlin
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Extract dtb from dt.img
from sys import argv, exc_info
import struct,shutil,os

__NAME__ = "dtimg2dtb"
__VERSION__ = "1.1"

def usage():
    print "Usage: %s [dt_image] [path]" % __NAME__

def carvedt(dt_file, offset, size, name):

    #print "offset:%#08x size:%#08x" %(offset,size)
    print "Carving to: \'%s\'" % name

    try:
        out_file = open(name, 'wb')

        dt_file.seek(offset)
        out_file.write(dt_file.read(size))
        out_file.close()
    except(IOError, OSError) as e:
        print "[ERROR] Unable to open output file!"
        return -2

    return 0

def processDt(dt_image_name,path):

    rtn = 0

    print "Processing \'%s\'" % dt_image_name
    try:
        f = open(dt_image_name, 'r')

        try:
            magic=struct.unpack('i', f.read(4))[0]
            version=struct.unpack('i', f.read(4))[0]
            num=struct.unpack('i', f.read(4))[0]
            if magic!=0x54444351 :
                print "dt magic QCDT not found"
                exit(1)
            print "dt version:%s" % version
            print "dtb nums:%s" % num
            if version==3:
                print "platform_id variant_id  subtype_id  soc_rev     pmic0       pmic1       pmic2       pmic3       offset      size      filename"
            elif version==2:
                print "platform_id variant_id  subtype_id  soc_rev     offset      size      filename"
            elif version==1:
                print "platform_id variant_id  soc_rev     offset      size      filename"
            else :
                print "not support your dt version"
                exit(1)
            dt= []
            for i in range(0,num):
		platform_id=struct.unpack('i', f.read(4))[0]
		variant_id=struct.unpack('i', f.read(4))[0]
		if version>1:
		    subtype_id=struct.unpack('i', f.read(4))[0]
		soc_rev=struct.unpack('i', f.read(4))[0]
		if version>2:
		    pmic0=struct.unpack('i', f.read(4))[0]
		    pmic1=struct.unpack('i', f.read(4))[0]
		    pmic2=struct.unpack('i', f.read(4))[0]
		    pmic3=struct.unpack('i', f.read(4))[0]
		offset=struct.unpack('i', f.read(4))[0]
		size=struct.unpack('i', f.read(4))[0]
		name=os.path.join(path+'/'+str(len(dt))+'.dtb')
		dtbexist=0
		for i in range(0,len(dt)):
		    if dt[i][0]==offset:
		        dtbexist=1
		        name=dt[i][2]
		        break
		if dtbexist==0:
		    dt.append([offset,size,name])
		if version==3:
		    print "%#08x    %#08x    %#08x    %#08x    %#08x    %#08x    %#08x    %#08x    %#08x    %#08x    %s" %(platform_id,variant_id,subtype_id,soc_rev,pmic0,pmic1,pmic2,pmic3,offset,size,name)
		elif version==2:
		    print "%#08x    %#08x    %#08x    %#08x    %#08x    %#08x    %s" %(platform_id,variant_id,subtype_id,soc_rev,offset,size,name)
                elif version==1:
		    print "%#08x    %#08x    %#08x    %#08x    %#08x    %s" %(platform_id,variant_id,soc_rev,offset,size,name)
            #print dt
            for i in range(0,len(dt)):
		print "offset:%#08x size:%#08x" %(dt[i][0],dt[i][1])
		if version>2:
		    f.seek(dt[i][0]+0x7c)
		    info1=f.read(0x28)
		    f.seek(dt[i][0]+0xb4)
		    info2=f.read(0x28)
		else:
		    f.seek(dt[i][0]+0x6c)
		    info1=f.read(0x28)
		    f.seek(dt[i][0]+0xa0)
		    info2=f.read(0x28)
		print "model:%s \ncompatible:%s" %(info1,info2)
		carvedt(f,dt[i][0],dt[i][1],dt[i][2])
        finally:
            f.close()

    except (IOError, OSError) as e:
        print "[ERROR] Unable to open file \'%s\'" % dt_image_name

        return -1

    return rtn

def main(image,path):
    
    rtn = 0
    if os.access(path, os.F_OK | os.X_OK) is True:
        shutil.rmtree(path)
    os.mkdir(path)
    if os.access(path, os.F_OK | os.X_OK) is True:
        rtn = processDt(image,path)

    return rtn

if __name__ == "__main__":

    if len(argv) < 2:
        print "[Error] You must specify dt image file."
        exit(usage())
    if len(argv) > 2:
        path=argv[2]
    else:
        path=argv[1]+"-dtb"
    exit(main(argv[1],path))
