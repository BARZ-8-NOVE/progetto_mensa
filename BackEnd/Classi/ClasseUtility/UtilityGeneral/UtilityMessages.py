class UtilityMessages:

    # Empty Constructor
    def __init__(self) -> None:
        pass

    @staticmethod
    def messageWrongKeys():
        return 'Wrong keys!'
    
    @staticmethod
    def existsStringError(search_name:str, parameter_name:str, search_parameter):
        return f'{search_name} already exists with {parameter_name}: {search_parameter}!'