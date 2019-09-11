from rest_framework.exceptions import APIException, _get_error_details


class ShopError(APIException):
    status_code = 400
    default_detail = 'Invalid input'
    default_code = 'wrong value'


class ObjectNotFound(ShopError):
    status_code = 404
    default_detail = 'Not Found'
    default_code = 'not_found'

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        detail = {name: 'not found.'}
        self.detail = _get_error_details(detail)


class StatusError(ShopError):

    def __init__(self):
        super().__init__()
        detail = {'open': ['Invalid input. Possible values are 0 or 1']}
        self.detail = _get_error_details(detail)


class DuplicateError(ShopError):

    def __init__(self):
        super().__init__()
        detail = {'shop': ['Invalid input. Object already exists']}
        self.detail = _get_error_details(detail)


class ValidationError(ShopError):

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        detail = {name: ['This field is required.']}
        self.detail = _get_error_details(detail)
