import csv
import pandas

class fileParser(object):

    def read_file(self, filename):
        '''
        Creates a keyword named "Read SKU File"
        This keyword takes one argument as a path to the file.
        and returns a list of rows containing product ids to be compared 
        with the data inside couchbase' bucket
        '''
        if '.csv' in filename:
            data = pandas.read_csv(filename)
        else:
            data = pandas.read_excel(filename)
        return data

    def get_number_of_columns(self, filename):
        '''
        Creates a keyword named "Get Numbers of Columns"
        This keyword takes one argument as a path to the file
        and returns the number of columns inside the file.
        '''
        return(len(fileParser().get_column_names(filename)))

    def get_column_names(self, filename):
        '''
        Creates a keyword named "Get Column Names"
        This keyword takes one argument as a path to the file
        and returns a list of column names.
        '''
        data = fileParser().read_file(filename)
        return(list(data.columns.values))

    def get_number_of_rows(self, filename):
        '''
        Creates a keyword named "Get Number of Rows"
        This keyword takes one argument as a path to the file
        and returns number of rows present in the file.
        '''
        data = fileParser().read_file(filename)
        return len(data.index)

    def get_list_of_items(self, filename):
        '''
        Creates a keyword named "Get List of Items"
        This keyword takes one argument as a path to the file
        and returns list of items per row.
        '''
        data = fileParser().read_file(filename)
        return(data.values.tolist())

# k = fileParser().get_list_of_items("../files/SKU.xlsx")
# print(k)