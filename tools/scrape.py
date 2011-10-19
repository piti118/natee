from httplib import HTTPConnection
import urllib
import datetime
import time
import os
import os.path
import sys

def date2fname(date):
    fname = 'rawhtml/'+str(date.year+543)+'-'+str(date.month)+'-'+str(date.day)+'.html'
    return fname

def loadegat(conn,date):
    #format the date
    date_str = str(date.day)+'/'+str(date.month)+'/'+str(date.year+543) 
    fname = date2fname(date)
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({'r_date':date_str})
        
    conn.request("POST","",params,headers)
    response = conn.getresponse()
    print ' ',date_str,response.status,response.reason
    sys.stdout.flush()
    if response.status==200:
        data = response.read()
        f = file(fname,'w')
        f.write(data)
        f.close()

def main():
    print "Delete this line if you are really sure you want to run this. This might crash egat web."
    sys.exit(1)
    if not os.path.exists('rawhtml'):
        os.makedirs('rawhtml')
    conn = HTTPConnection('ichpp.egat.co.th')
    numdays = 7000 #change this number
    sleep_interval = 3
    today = datetime.datetime.today()
    datelist = (today - datetime.timedelta(days=x) for x in xrange(numdays))
    for i,date in enumerate(datelist):
        print str(i)+'/'+str(numdays),
        loadegat(conn,date)
        time.sleep(sleep_interval)#don't crash their web
    conn.close()
    
    #writing list of files
    datelist = (today - datetime.timedelta(days=x) for x in xrange(numdays))
    f = open('rawhtml/filelist.txt','w')
    for date in datelist:
        f.write(date2fname(date)+'\n')
    f.close()

if __name__ == '__main__':
    main()