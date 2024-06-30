class HttpCodes:

    # Empty Constructor
    def __init__(self) -> None:
        pass

    # Constants
    #200
    __OK = 200
    __CREATED = 201
    __ACCEPTED = 202
    #400
    __BAD_REQUEST = 400
    __UNAUTHORIZED = 401
    __FORBIDDEN = 403
    __NOT_FOUND = 404
    __METHOD_NOT_ALLOWED = 405
    __REQUEST_TIMEOUT = 408
    __UNPROCESSABLE_ENTITY = 422
    #500
    __INTERNAL_SERVER_ERROR = 500

    #Getters
    @property
    def OK(self):
        """
        :description: The request is OK
        :return: 200
        """
        return self.__OK
    @property
    def CREATED(self):
        """
        :description: New resource created, used for POST requests
        :return: 201
        """
        return self.__CREATED
    @property
    def ACCEPTED(self):
        """
        :description: Request accepted but still in progress
        :return: 202
        """
        return self.__ACCEPTED
    
    @property
    def BAD_REQUEST(self):
        """
        :description: The server cannot process the request due to client error
        :return: 400
        """
        return self.__BAD_REQUEST
    @property
    def UNAUTHORIZED(self):
        """
        :description: The user must login to get the request
        :return: 401
        """
        return self.__UNAUTHORIZED
    @property
    def FORBIDDEN(self):
        """
        :description: The user doesn't have the required permission
        :return: 403
        """
        return self.__FORBIDDEN
    @property
    def NOT_FOUND(self):
        """
        :description: The resource does not exist
        :return: 404
        """
        return self.__NOT_FOUND
    @property
    def METHOD_NOT_ALLOWED(self):
        """
        :description: The request is not allowed for that specific resource
        :return: 405
        """
        return self.__METHOD_NOT_ALLOWED
    @property
    def REQUEST_TIMEOUT(self):
        """
        :description: The maximum duration a client is willing to wait for a response from the server
                    after a successful connection has been established
        :return: 408
        """
        return self.__REQUEST_TIMEOUT
    @property
    def UNPROCESSABLE_ENTITY(self):
        """
        :description: Indicates that the action could not be processed properly due to invalid data provided
        :return: 422
        """
        return self.__UNPROCESSABLE_ENTITY

    @property
    def INTERNAL_SERVER_ERROR(self):
        """
        :description: The server encountered an unexpected condition that prevented it from fulfilling the request
        :return: 500
        """
        return self.__INTERNAL_SERVER_ERROR
    
