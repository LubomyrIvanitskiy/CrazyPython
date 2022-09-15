import dataclasses

from arguments_readwrite import Read, control_access, AccessGuard


@dataclasses.dataclass
class Response:
    msg: str


class Callback(metaclass=AccessGuard):

    @control_access
    def on_success(self, result: Read[Response]):
        pass


class API:
    def __init__(self, callback: Callback):
        assert isinstance(callback, Callback)
        self.callback = callback

    def _save_to_db(self, response):
        ...

    def make_request(self):
        ...
        self.on_success(Response("Success"))

    def on_success(self, response):
        self.callback.on_success(response)
        self._save_to_db(response)


class UserCallback(Callback):

    def on_success(self, result):
        # result.msg = "Fake message"
        print(result)


api = API(UserCallback())
api.make_request()
