class UtilityMessages:

    # Empty Constructor
    def __init__(self) -> None:
        pass

    @staticmethod
    def wrongKeysErrorMessage():
        return 'Wrong keys!'
    
    @staticmethod
    def existsErrorMessage(resource_name:str, parameter_name:str, search_parameter):
        return f'{resource_name} already exists with {parameter_name}: {search_parameter}!'
    
    @staticmethod
    def deleteMessage(resource_name:str, parameter_name:str, search_parameter):
        return f'Deleted {resource_name} for this {parameter_name}: {search_parameter}'
    
    @staticmethod
    def notFoundErrorMessage(resource_name:str, parameter_name:str, search_parameter):
        return f'{resource_name} not found for this {parameter_name}: {search_parameter}'