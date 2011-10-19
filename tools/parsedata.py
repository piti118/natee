from BeautifulSoup import BeautifulSoup
import codecs
import glob
import csv

def parser(fname):
  f = codecs.open(fname,'r','cp874')
  bs = BeautifulSoup(f.read())
  f.close()
  #print bs.prettify()
  date = bs.find('input',attrs={"name" : "r_date"})['value']
  print date
  datatable = bs.find('table',id='mytable')
  tablerows = datatable.findAll('tr')
  header = tablerows.pop(0)#docking of the header row
  
  #building header
  headertd = header.findAll('td')
  headerarray = [x.contents[0].string for x in headertd]
  
  #now the contents
  dataarray = []
  for row in tablerows:
    alltd = row.findAll('td')
  
    rowcontent = []
    for x in alltd:
      depth = 0
      j = x.contents[0]
      while j.string is None: #navigate through all fonts and blink and what not
        j = j.contents[0]
        depth +=1
        assert(depth < 5)
      rowcontent.append(j.string)
    dataarray.append(rowcontent)
  del bs
  m = {}
  m['date'] = date
  m['header'] = headerarray
  m['data'] = dataarray

  return m
  
def main():
  allf = glob.glob('rawhtml/*.html')
  result = {}
  first = True
  f = codecs.open('data.csv','w','utf-8')
  for fname in allf:
    m = parser(fname)
    if first:
      first = False
      headerline = u','.join(['date']+m['header'])
      f.write(headerline+'\n')
    for row in m['data']:
      #print row
      dataline = u','.join([m['date']]+row)
      f.write(dataline+'\n')
    f.flush()
  f.close()
      
    
if __name__ == '__main__':
  main()