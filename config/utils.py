from pandas import Series
import numpy as np

class Utils:
    
    @staticmethod
    def update_dtype(column, dtype):
        
        if type(column) is not Series:
            raise TypeError("Column argument must be a Pandas Series Object.")
        
        if dtype == 'int':
            c = column.astype(np.int64)
        
        elif dtype == 'float':
            c = column.astype(np.float32)
        
        else:
            c = column.astype(np.str)
            
        if dtype != 'str':
            c = c.astype(np.str)
            
        return c
        