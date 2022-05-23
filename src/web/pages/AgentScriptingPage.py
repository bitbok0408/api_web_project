from .LoginPage import LoginPage
from selene.api import ss, s, be


class AgentScripting(LoginPage):

    def __init__(self):
        super().__init__()
        if not self.menu.is_present():
            self.login_with_root_credentials()
            self.menu.is_loaded()
        self.menu.agent_scripting.go()



