from config.finder import ValidatorFinder

class ValidationProcessor:
    
    __evaluation_parameters = None
    __source = None
    __context = None
    __existing_validations = None
    __id_column = None
    __finder = None

    def __init__(self, configuration, __existing_validations):
        
        self.__evaluation_parameters = configuration.PARAMETERS
        self.__source = configuration.SRC
        self.__context = configuration.CONTEXT
        self.__id_column = configuration.ENV['identification_column']
        self.__existing_validations = __existing_validations
        self.__finder = ValidatorFinder()

    def create_method(self, method_name):

        finder = self.__finder
        context = self.__context
        existing_validations = self.__existing_validations
        
        for validator_name in existing_validations:
            
            if method_name in existing_validations[validator_name]:
                
                # validator_class es una instancia
                validator_class = finder.get_class_by_name(validator_name)(context)
                function = getattr(validator_class, method_name)
                
                return function

        raise NameError(f"Validator method '{method_name}' does not defined.")

    def run_method_from_str(self, column, function):

        """
        Parsea el método a partir de su nombre(str), lo ejecuta (Con un solo argumento 'column')
            y retorna un diccionario con sus resultados
        """
        id_column = self.__id_column
        source = self.__source
        validation_result = {'method': function.__name__,'method_type': 'str','column': column,'records': None}
        records = tuple()

        df_boolean_result = source[column].map(lambda x : True if function(x) is False else False)                          
        records = source[df_boolean_result]

        if len(records) != 0 :
            validation_result['records'] = tuple(records[id_column])

        return validation_result

    def run_method_from_dict(self, args, function):

        """
        Parsea el método a partir de su nombre(str), lo ejecuta (con más de un argumento)
            y retorna un diccionario con sus resultados
        """
        validation_result = {'method': function.__name__, 
                   'method_type': 'dict'}
        validation_result.update(args)
        validation_result['records'] = None

        function_wrapper = lambda args: function(**args)           
        result = function_wrapper(args)
        validation_result['records'] = result
        return validation_result

    def validate(self):
        
        results_container = []
        parameters = self.__evaluation_parameters
        source = self.__source
        
        for parameter in parameters:
            
            print(parameter)
            
            for method in parameters[parameter]:
                validation_result = None
                
                if type(method) is str:
                    function = self.create_method(method)
                    validation_result = self.run_method_from_str(parameter, function)
                    print(validation_result)
                    
                if type(method) is dict:
                    
                    for key in (method.keys()):
                        args = method[key]
                        function = self.create_method(key)
                        validation_result = self.run_method_from_dict(args, function)
                        print(validation_result)
                        
                results_container.append(validation_result)
        
        return results_container