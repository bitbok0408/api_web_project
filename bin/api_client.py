from requests.sessions import Session as Requests_session
from helpers.authorization import get_auth_token_with_headers
from .logger import logger


class Session(Requests_session):

    """
    Reinitialize requests.Session with Company auth token.
    Иннициализация сессия проиходит в .bin.__init__
    Если отправить запрос с собственными headers, то будет использована новая(одноразовая) Сессия
    """

    def __init__(self):
        super(Session, self).__init__()
        self.headers = get_auth_token_with_headers()
        self.logger = logger

    def choose_request_method(self, method, url, **kwargs):
        """
        Если headers переданы создам "одноразовую" сессию, в противном случае используем старую сессию
        :param method:
        :param url:
        :param id_to_url:
        :param kwargs:
        :return:
        """

        if "headers" not in kwargs:
            return self.request(method=method, url=url, **kwargs)

        with Requests_session() as session:
            return session.request(method=method, url=url, **kwargs)

    def send_request(self, method, url, **kwargs):
        return self.choose_request_method(method=method, url=url,  **kwargs)

