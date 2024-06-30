class NotFoundError(Exception):

    def __init__(self, message, parameter_name, search_parameter) -> None:
        self.message = f"{message} not found for {parameter_name}: {search_parameter}!"
        super().__init__(self.message)