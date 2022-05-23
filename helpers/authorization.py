import requests
from config.project_config import cfg
from helpers.utils import get_url
from Data.url import AuthServer


def get_auth_token_with_headers(*args):
    """
    :param args: str Login and str Password
    :return: {"Content-Type": "application/json;charset=UTF-8",
              "X-Company-Auth-Token": str: token}
    """
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    if not args:
        payload = {"principal": cfg.credentials['principal'], "credential": cfg.credentials['credential']}
    else:
        payload = {"principal": args[0], "credential": args[1]}
    response = requests.post(url=get_url(AuthServer.auth), json=payload, headers=headers, verify=False)
    assert response.status_code == 200, "AUTH SERVER PROBLEM, response_code = %d" % response.status_code
    headers['Authorization'] = f"Bearer {response.json()['token']}"
    return headers
