from config.configurer import ConfigurationLoader
from config.finder import ValidatorFinder
from config.remark.processor import RemarkerProcessor
from config.validation.processor import ValidationProcessor

# Main

def main():
    configuration = ConfigurationLoader()
    existing_validations = ValidatorFinder().list_methods()

    processor = ValidationProcessor(configuration, existing_validations)
    results_container = processor.validate()
    wrmk = RemarkerProcessor(configuration, results_container)
    wrmk.remark_source()


if __name__ == '__main__':
    main()