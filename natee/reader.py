from os.path import dirname
import util
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)
    def __str__(self):
        return str(self.__dict__)
def float_conv(x): return float(x)
def string_conv(x): return str(x)
def date_conv(x): return util.td2date(x)

def read(fname):
    f = open(fname,'r')
    #get the header
    header = f.readline().strip()
    print header
    type_conv = {'s':string_conv,'f':float_conv,'d':date_conv}
    keys = header.split(',')
    col_type = [x[-1] for x in keys]
    col_conv = [type_conv[x] for x in col_type]
    keys = [x[:-2] for x in keys] #dock off type info
    toReturn = []
    for line in f:
        row = line.split(',')
        rowdict = dict( ( key, col_conv[i](row[i]) ) for i,key in enumerate(keys) )
        s = Struct(**rowdict)
        toReturn.append(s)
        print s 
    return toReturn
def main():
    read(dirname(__file__)+'../tools/data/bb.csv')

if __name__ == '__main__':
    main()