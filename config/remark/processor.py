from openpyxl import Workbook
from config.remark.handler import  RemarkerConfigurator
from config.remark.writer import RemarkWriter

class RemarkerProcessor:
    
    __results_container = None
    __rconfigurator = RemarkerConfigurator()
    __configuration = None
    
    def __init__(self, configuration, results_container):
        self.__results_container = results_container
        self.__configuration = configuration
        
    def remark_source(self):
        rconfigurator = self.__rconfigurator
        results_container = self.__results_container
        configuration = self.__configuration
        
        writer = RemarkWriter(configuration)
        
        for validation_result in results_container:
            
            if validation_result['records'] is None:
                continue
            
            method_name = validation_result['method']
            invalided = validation_result['records']
            
            # Writer Configuration
            write_config = rconfigurator.handler_wrapper(validation_result)
            columns_reference = write_config['columns_reference']
            
            print(write_config)
            writer.write_worksheet(write_config, validation_result)
            
        writer.export_to_excel()