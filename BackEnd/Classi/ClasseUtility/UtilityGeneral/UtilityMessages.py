class UtilityMessages:
    """Class for the messages"""

    # Empty Constructor
    def __init__(self) -> None:
        pass

    # Static methods
    @staticmethod
    def wrongKeysErrorMessage():
        """
        :description: Static method that returns a string 'Wrong keys!'
        :return: Literal['Wrong keys!']
        """
        return 'Wrong keys!'
    
    @staticmethod
    def existsErrorMessage(resource_name:str, parameter_name:str, search_parameter):
        """
        :description: Static method that concatenate a string passing 3 parameters.
        Used when the resource already exists with that search_parameter
        :args: resource:name:str, parameter_name:str, search_parameter
        :return: a message of already exist resource
        """
        return f'{resource_name} already exists with {parameter_name}: {search_parameter}!'
    
    @staticmethod
    def deleteMessage(resource_name:str, parameter_name:str, search_parameter):
        """
        :description: Static method that concatenate a string passing 3 parameters.
        Used when the resource is deleted with that search_parameter
        :args: resource:name:str, parameter_name:str, search_parameter
        :return: a message of deleted resource
        """
        return f'Deleted {resource_name} for this {parameter_name}: {search_parameter}'
    
    @staticmethod
    def notFoundErrorMessage(resource_name:str, parameter_name:str, search_parameter):
        """
        :description: Static method that concatenate a string passing 3 parameters.
        Used when not found resource with that search_parameter
        :args: resource:name:str, parameter_name:str, search_parameter
        :return: a message of resource not found
        """
        return f'{resource_name} not found for this {parameter_name}: {search_parameter}'