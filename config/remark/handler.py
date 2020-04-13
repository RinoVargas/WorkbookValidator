from config.finder import ValidatorFinder
import json

class RemarkerConfigurator:
    
    __comments = None
    __finder = ValidatorFinder()
    
    def __init__(self):
        self.__comments = self.load_comments()
        

    def load_comments(self):
        comments = None
        
        with open("config/commets.json","r") as file:
            comments = json.load(file)
        return comments
    
    def list_validator_handlers(self):
        handlers = tuple(filter(lambda x: x.startswith('handle_'), dir(self)))
        
        return handlers
        
    def handler_wrapper(self, remark):
        methodname = remark['method']
        vf = self.__finder
        vclass = vf.get_classname_by_methodname(methodname)
        handlers = self.list_validator_handlers()
        
        for handler in handlers:
            if vclass == handler.strip("handle_"):
                handle_func = getattr(self,handler)
                return handle_func(remark)
        
        raise ValueError(f"Handler for Validator Object '{vclass}' not found.")

    def handle_CellValidator(self, remark):
        method_name = remark['method']
        commets = self.__comments
        mname = self.__finder.get_classname_by_methodname(method_name)
        
        if mname == 'CellValidator':
            references = commets[mname]['columns_reference']
            columns_reference = [ remark[column] for column in references ]
            comment_configuration = commets[mname]['methods'][method_name]
            
            parameters = {'method_name': method_name, 
                          'columns_reference': columns_reference, 
                          'show': comment_configuration['show'],
                          'message': comment_configuration['message'],
                          'configuration': {}}
            
            return parameters
        return None
    
    def handle_DuplicateValidator(self, remark):
        method_name = remark['method']
        commets = self.__comments
        mname = self.__finder.get_classname_by_methodname(method_name)
        
        if mname == 'DuplicateValidator':
            references = commets[mname]['columns_reference']
            columns_reference = [ remark[column] for column in references if column in remark ]
            comment_configuration = commets[mname]['methods']
            
            parameters = {'method_name': None, 
                          'columns_reference': columns_reference,
                          'show': None,
                          'message': None, 
                          'configuration': {}}
            
            for method in comment_configuration:
                method_type = None
                            
                if method == 'check_duplicates':
                    parameters['method_name'] = method
                    method_type  = 'single_column' if 'target' not in remark else 'double_column'
                    
                    type_cfg = comment_configuration['check_duplicates'][method_type]
                    parameters['show'] = type_cfg['show']
                    parameters['message'] = type_cfg['message']
                    parameters['configuration']['method_type'] = method_type
                
                else:
                    raise ValueError(f"DuplicateValidator class don't include '{method}' method")
                        
                    
                return(parameters)