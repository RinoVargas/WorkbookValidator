import config.validation.validator as validator

class ValidatorFinder():
    
    
    def __init__(self):
        pass
    
    def get_class_by_name(self, classname):
        vclass = getattr(validator, classname)
        
        return vclass
    
    def get_classname_by_methodname(self, method_name):
        class_list = self.list_methods()
        
        for classname in class_list:
            
            if method_name in class_list[classname]:
                return classname
        
        return None
        
    def list_classname(self):
        vclass_list = dir(validator)
        vclass_list = tuple(filter(lambda x: x.endswith("Validator"), vclass_list))
        
        return vclass_list
    
    
    def list_methods(self):
        methods = {}
        class_list = self.list_classname()
        
        for vclass_name in class_list:            
            vclass = self.get_class_by_name(vclass_name)
            method_list = [func for func in dir(vclass) if callable(getattr(vclass, func))]
            method_list = list(filter(lambda x : not x.startswith("__"), method_list))
            
            methods[vclass_name] = method_list
        
        return methods