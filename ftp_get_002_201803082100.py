#
# PPS Python ftp script
#
# Usage:  python <script name>
#

import os, sys, re, hashlib
from getpass import getpass
from ftplib import FTP

downloadCount=0
skipCount=0

def hashfile(filename, blocksize=65536):
    hasher = hashlib.sha1()
    localfile=open(filename, 'rb')
    buf = localfile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = localfile.read(blocksize)
    localfile.close()
    return hasher.hexdigest()

def getFile(filepath,cksum=None):
    global downloadCount,skipCount
    path,filename=os.path.split(filepath)
    connection.cwd(path)
    download=True
    ftpSize=connection.size (filename)
    # determine if file exists in local directory
    if (os.path.exists(filename)):
        # check size and cksum
        if (cksum):
            sha = hashfile(filename)
            if (cksum == sha):
                download=False
        else:
            filesize=os.path.getsize(filename)
            if (ftpSize==filesize):
                download=False

    if (download):
        # if not exists or file checks do not match, get file.
        downloadCount+=1
        sys.stdout.write( str(downloadCount)+') Downloading '+filename+'   '+str(ftpSize)+' bytes  ')
        sys.stdout.flush()
        localfile=open(filename, 'wb')
        connection.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

        if (cksum):
            sys.stdout.write('cksum ')
            sys.stdout.flush()
            sha = hashfile(filename)
            if (cksum == sha):
                print ('Pass')
            else:
                print ('FAIL')
        else:
            print ('Done')
    else:
            print ('Already downloaded '+filename)
            skipCount+=1


if __name__ == '__main__':
    userinfo=('diegoprieto199796@gmail.com','diegoprieto199796@gmail.com')
    print ('Connecting to PPS')
    connection = FTP('arthurhou.pps.eosdis.nasa.gov')
    print (connection.getwelcome())
    connection.login(*userinfo)
    connection.sendcmd('TYPE i')

#
# The following is the list of PPS files to transfer:
#
    getFile('/gpmuser/diegoprieto199796@gmail.com/pgs/3A-DAY-12.GPM.GMI.GRID2017R1.20180306-S000000-E235959.065.V05A.HDF5','7cbdcbd5e168d8bf501fb7dbf7f9c82f2ab7a454')
#
# Transfer complete; close connection
#
    connection.quit()
    print ('Number of files downloaded: '+str(downloadCount))
    if (skipCount>0):
        print ('Number of files already downloaded: '+str(skipCount))
