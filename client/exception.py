class IoFogException(Exception):
    def __init__(self, *args, **kwargs):
        super(IoFogException, self).__init__(*args, **kwargs)


class IoFogHttpException(IoFogException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'Error code: {}, reason: {}'.format(self.code, self.message)






