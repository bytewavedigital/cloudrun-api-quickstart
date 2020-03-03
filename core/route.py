import inspect


class Route:
    def __init__(self, *, method=None, handler=None, req_schema=None):
        self.method = method
        self.handler = handler
        self.req_schema = req_schema

    def validate(self):
        errors = []
        is_valid_method = self.is_valid_method()
        is_valid_handler = self.is_valid_handler()
        is_valid_schema = self.is_valid_schema()
        if is_valid_method is not True:
            errors.append(is_valid_method)
        if is_valid_handler is not True:
            errors.append(is_valid_handler)
        if is_valid_schema is not True:
            errors.append(is_valid_schema)
        if errors:
            return errors
        return True

    def is_valid_method(self):
        if self.method.lower() in ('get', 'post', 'put', 'delete'):
            return True
        return f"Invalid method {self.method} expecting any one of the 'get, post, put, delete'"

    def is_valid_handler(self):
        if inspect.iscoroutinefunction(self.handler):
            return True
        return f"Invalid handler {self.handler} expecting async function"

    def is_valid_schema(self):
        if not self.req_schema:
            return True
        if type(self.req_schema) is dict:
            return True
        return f"Invalid schema expecting dict"
