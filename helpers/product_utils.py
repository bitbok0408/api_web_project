from bin.project import send
from Data.url import mgr


class UserParams:
    def __init__(self):
        self.root_group_id = self._get_root_group_id()
        self.root_role_id = self._get_root_role_id()
        self.root_user_id = self._get_root_user_id()

    @staticmethod
    def _get_root_group_id():
        response = send.get(mgr.groups)
        if "ROOT" in response.json()[0]["name"]:
            return response.json()[0]["groupId"]

    @staticmethod
    def _get_root_role_id():
        response = send.get(mgr.roles)
        for role in response.json():
            if role['name'] == "ROOT":
                return role['roleId']

    @staticmethod
    def get_role_id_by_name(role_name):
        response = send.get(mgr.roles)
        for role in response.json():
            if role['name'] == role_name:
                return role['roleId']

    @staticmethod
    def _get_root_user_id():
        data = {
            "$criteria_name": "userLogin",
            "$criteria_operator": "equal",
            "$criteria_values": "root"
        }
        response = send.post(mgr.users_search, data)
        return response.json()['data'][0]["userId"]


user_params = UserParams()




