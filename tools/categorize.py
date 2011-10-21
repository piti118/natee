# -*- coding: utf-8 -*-
import codecs
import datetime
from daminfo import dam_code
def main():
    f = codecs.open('data/data.csv','rb','utf-8')
    #f = open('data.csv','r','utf-8')
    first = True
    header = []
    reduced_data = {}
    
    for key,dc in dam_code.items(): reduced_data[dc]=[]
    
    for line in f:
        if first:
            first = False #ignore header line
            continue
        data = line.strip().split(u',')
        #print data[1]
        dc = dam_code[data[1]]
        data[1] = dc
        d,m,y = data[0].split('/')
        thisdate = datetime.date(int(y)-543,int(m),int(d)) #build date from data[0]
        #only date, dam code, incoming water, and historical data for amount of water
        reduced_data[dc].append( (thisdate,[data[0],data[1],data[6],data[14]]) )
    
    #now all the data is in. sort them by date
    for key in reduced_data.keys():
        reduced_data[key].sort(key=lambda x: x[0])
        
    #now get rid of x's
    #cut off all the header X
    for key in reduced_data.keys():
        data = reduced_data[key]
        while data[0][1][3]=='X':
            #print 'pop head',key
            data.pop(0)
    
    #now take care of x in between
    for key in reduced_data.keys():
        data = reduced_data[key]
        for i,item in enumerate(data):
            if item[1][2]=='X': item[1][2] = data[i-1][1][2]
            if item[1][3]=='X': item[1][3] = data[i-1][1][3]
    
    #sanity check that there is no missing hole
    print 'Checking'
    for key in reduced_data.keys():
        data = reduced_data[key]
        for i,item in enumerate(data):
            if item[1][2]=='X' or item[1][3]=='X': print 'bad', i, item[0]
    #write sort data to key    
    print 'Done'
    for key in reduced_data.keys():
        out = open('data/'+key+'.csv','w')
        for date,val in reduced_data[key]:
            out.write(u','.join(val)+'\n')
            out.flush()
        out.close()
      
    f.close()
    
if __name__ == '__main__':
    main()
