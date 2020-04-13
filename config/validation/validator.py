import pandas
import datetime
import re
import numpy as np
from config.utils import Utils as u

class ValidatorContext:
   
    id_column = None
    source = None
    _validations = dict()
    
    
    def __init__(self, id_column, source):
        self.id_column = id_column
        self.source = source

class CellValidator(ValidatorContext):
    
    def __init__(self, vobject):
        
        super().__init__(vobject.id_column, 
                         vobject.source)
    
    def is_dni(self,value, empty=""):

        str_value = str(value)
        regex = "^\d{8}$"
        regex = regex + "|^$" if empty == "ignore" else regex
        result = re.match(regex, str_value)
        
        return True if result else False
    
    def is_not_empty(self,value):
        
        str_value = str(value)

        return True if len(str_value) != 0 else False
    
    def is_orcid(self,value, empty=""):
        
        str_value = str(value)
        regex = "^\w{4}-\w{4}-\w{4}-\w{4}$"
        regex = regex + "|^$" if empty == "ignore" else regex
        result = re.match(regex, str_value)
        
        return True if result else False
    
    def is_gender(self,value, empty=""):
        
        str_value = str(value)
        regex = "^[ufm]$"
        regex = regex + "|^$" if empty == "ignore" else regex
        result = re.match(regex, str_value)
        
        return True if result else False
    
    def is_date(self,value):
        try:
            if datetime.datetime.strptime(value, '%d-%m-%Y'):
                return True
        except:
            return False
    
    def is_email(self, value, empty=""):
        
        str_value = str(value)
        regex = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
        regex = regex + "|^$" if empty == "ignore" else regex
        result = re.match(regex, str_value)
        
        return True if result else False
    
class DuplicateValidator(ValidatorContext):
    
    def __init__(self, vobject):
        super().__init__(vobject.id_column, vobject.source)
        
        
    def check_duplicates(self, column ,column_dtype="str", 
                                  target=None, target_dtype=None,
                                  target_spliter=None):
        # Definiciones
        src = self.source
        results_container = []
        
        # SRC - column
        src = src[src[column] != '']
        
        ## Check duplicates in current column
        if target is None :
            src = src.filter([ self.id_column, column])
            src[column] = u.update_dtype(src[column],column_dtype)
            src = src.reset_index(drop=True)
        
            groups = src.groupby(column).groups
            keys = groups.keys()
            
            for key in keys:
                records = groups[key].get_values()
                if len(records) > 1:
                    result_validation = dict(value = key, 
                                  records = [src.iloc[r][self.id_column] for r in records])
                    results_container.append(result_validation)
            return results_container

        
        ## Compare 'column' value to 'target' value
        if target is not None:
            
            # SRC
            src = src.filter([ self.id_column, column, target ])
            
            # SRC - column
            src[column] = u.update_dtype(src[column],column_dtype)
            
            # SRC - target
            src = src[src[target] != '']
            src[target] = u.update_dtype(src[target],target_dtype)
        
            if target_dtype is not 'str':
                src[column] = src[column].astype(np.str)
            
            if target_spliter is None:
                
                r = src[src[column] == src[target]]
                r = r.reset_index(drop=True)
                rlen = len(r)
                
                for x in range(0, rlen):
                    i = r.at[x,self.id_column]
                    v = r.at[x,column]
                    result_validation = { 'record': i, 'value': v}
                    results_container.append(result_validation)
                    
                return results_container
                
            
        ## Check 'column' value in 'target' spliting list
        if target is not None and target_spliter is not None:
            
            # Exception
            if type(target) is not str:
                raise TypeError("Target parameter must be string type")
                
            if type(target_spliter) is not str:
                raise TypeError("Separator parameter must be string type")
                
            src[target] = src[target].apply(lambda x : x.split("|||"))
            # Reset Index
            src = src.reset_index(drop=True)
            src_len = len(src)
        
            for index in range(0,src_len):
                c = src.at[index, column]
                t = src.at[index, target]
                i = src.at[index,self.id_column]
            
                if c in t:
                    results_container.append({'record' : i , 'value' :  c})
                
            return results_container