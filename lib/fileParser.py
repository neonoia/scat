import csv
import pandas

class fileParser(object):

    def read_sku_file(self, filename):
        '''Creates a keyword named "Read SKU File"
        This keyword takes one argument as a path to the csv file.
        and returns a list of rows containing product ids to be compared 
        with the data inside couchbase' bucket
        '''
        if '.csv' in filename:
            data = pandas.read_csv(filename)
            return(data.SKU.tolist())
        else:
            res = []
            data = pandas.read_excel(filename)
            for datas in data.SKU:
                stripped = datas.encode("utf-8")
                res.append(stripped)
            return(res)