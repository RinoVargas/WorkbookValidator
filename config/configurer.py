import json
from pandas import read_excel
from javaproperties import loads
from config.validation.validator import ValidatorContext
from os.path import exists

class ConfigurationLoader:
    
    __ENV_FILE = 'env.properties'
    PARAMETERS = None
    SRC = None
    CONTEXT = None
    ENV = None
    
    def __init__(self):
        
        self.ENV = self.__get_environment()
        self.PARAMETERS = self.__load_evaluation_parameters()
        self.SRC = self.__get_source()
        self.CONTEXT = ValidatorContext(self.ENV['identification_column'], self.SRC)

    def __get_environment(self):
        
        settings = None

        with open(self.__ENV_FILE,"r") as file:
            settings = file.read()
            file.close()

        return loads(settings)        
        
    def __load_evaluation_parameters(self):
        
        config = None
        
        with open(self.ENV['evaluation_parameters'], "r") as f:
            config = json.load(f)
            f.close()
        
        return config
    
    def __get_source(self):
        
        file_path = self.ENV['input_dir'] + "/" + self.ENV['source_file']
        
        if 'sheet_name' in self.ENV:
            sheet_name = self.ENV['sheet_name']
            source = read_excel(file_path, sheet_name).fillna("").astype(object)
            
            return source
        
        source = read_excel(file_path).fillna("").astype(object)
        
        return source
        