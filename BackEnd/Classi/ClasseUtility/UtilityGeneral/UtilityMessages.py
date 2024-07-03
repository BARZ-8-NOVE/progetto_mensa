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
    
    @staticmethod
    def forbiddenPasswordIncorrectError(username:str):
        """
        :description: Static method that concatenate a string passing 1 parameter.
        Used when the password is incorrect for that username
        :args: username:str
        :return: a message of password incorrect
        """
        return f'The password is incorrect for this username: {username}'
    
    @staticmethod
    def forbiddenUtenteAlreadyLoggedInError(username:str, in_or_out:str):
        """
        :description: Static method that concatenate a string passing 2 parameters.
        Used when the utente is already logged in or already logged out for that username
        :args: username:str
        :return: a message of utente already logged in or already logged out
        """
        return f'Utente: {username} is already logged {in_or_out}!'
    
    @staticmethod
    def unauthorizedErrorToken(description:str):
        """
        :description: Static method that concatenate a string passing 1 parameter.
        Used when there is an error with a token
        :args: description:str
        :return: a message: Token is {description}
        """
        return f'Token is {description}'