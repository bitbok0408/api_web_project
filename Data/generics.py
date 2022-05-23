import random
import datetime
from enum import Enum
from mimesis import Person
from mimesis import Generic
from mimesis import Text
from mimesis import Food
from mimesis import Numbers
from mimesis import Cryptographic
from mimesis import Datetime
from mimesis import Internet
from mimesis.schema import Field, Schema
from mimesis import BaseProvider
from helpers.utils import make_user_group_roles
from helpers.product_utils import user_params
from collections import defaultdict


class Generator:
    def __init__(self, lang):
        self.lang = lang
        self._person = Person(self.lang)
        self._generic = Generic(self.lang)
        self._string = Text(self.lang)
        self._manager = Manager(self.lang)
        self._number = Numbers()
        self._food = Food(self.lang)
        self.generic.add_provider(CompanyProvider)
        self._cryptographic = Cryptographic(self.lang)
        self._date = Datetime()
        self._call = CallDataBuilder()

    @property
    def person(self):
        return self._person

    @property
    def generic(self):
        return self._generic

    @property
    def unique_name(self):
        """
        Use this when need name with 3+ characters unique word
        :return:
        """
        return f"{self._food.drink()}_{random.randint(1, 1000)}"

    @property
    def political_views(self):
        return f"{self._person.political_views()}_{random.randint(1, 20)}"

    @property
    def string(self):
        return self._string

    @property
    def number(self):
        return self._number

    @property
    def manager(self):
        return self._manager

    @property
    def uuid(self):
        return self._cryptographic.uuid()

    @property
    def datetime(self):
        return self._date

    @property
    def call(self):
        return self._call


class CompanyProvider(BaseProvider):
    class Meta:
        name = "company"

    @staticmethod
    def xrefci():
        internet = Internet()
        crypto = Cryptographic()
        return f"{crypto.uuid()}@{internet.ip_v4()}"

    @staticmethod
    def phone():
        """
        Only integers without '(-' characters - it's phone format in company
        :return:
        """
        return str(random.randint(1, 999999999999999))

    @staticmethod
    def login():
        """
        Login always must be in English
        :return:
        """
        _ = Text('en')
        return f'{_.word()}_{str(random.randint(1, 99999))}'

    @staticmethod
    def password():
        """
        Replace " in password for json.loads
        :return:
        """
        g = Person()
        return g.password().replace("\\", "\\\\")


class Manager:

    def __init__(self, lang):
        self.lang = lang

    def user(self, count=1):

        _ = Field(self.lang, providers=[CompanyProvider])
        description = (
            lambda: {"$login": _('company.login'),
                     "$fname": _('person.name'),
                     "$lname": _('person.last_name'),
                     "$agentId": _('text.word') + f'_{str(random.randint(1, 99999))}',
                     "$ADlogin": _('text.word') + f'_{str(random.randint(1, 99999))}',
                     "$pname": _('person.name'),
                     "$password": _('company.password'),
                     "$email": _('person.email'),
                     "$phone": _('company.phone'),
                     "$fax": _('person.telephone'),
                     "$deleted": False
                     }
        )
        schema = Schema(schema=description)
        users = schema.create(iterations=count)
        return users if len(users) > 1 else users[0]

    @staticmethod
    def _make_user_group_roles(group, role):
        if not group:
            group = user_params.root_group_id
        if not role:
            role = user_params.root_role_id
        return make_user_group_roles({group: role})


# TODO: Добавить юзера, добавить Messages
class CallDataBuilder:
    CONTENT_TYPE = ["AUDIO", "CHAT", ]
    FINISH_STATE = ["STARTED", "CONVERTED", "CONVERTING_CORRUPTED", "ENDED", "CLEANED", "UNDEFINED", "RECOVERED"]
    MESSENGER_TYPE = ["TELEGRAM", "VIBER", "FACEBOOK", "SKYPE", ]
    CALL_PARTICIPANT_TYPE = ["INNER", "OUTER", ]
    DIRECTION = ["DIRECTION_IN", "DIRECTION_OUT", "DIRECTION_UNKNOWN", ]
    CALL_TYPE = ["UNDEFINED", "NORMAL", "CONSULT"]
    LICENSED = ["LICENSED", "NOT_LICENSED", ]
    PARTICIPANT_PARTICIPANT_TYPE = ["CLIENT", "AGENT", ]
    RECOGNIZE_STATE = ["RECOGNIZED", "RE_RECOGNIZE", "NOT_RECOGNIZED", "ERROR"]
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self.call_statistic_id = None
        self.call_duration = 0
        self.call_id = 0
        self.call_part_id = 0
        self.call_part_number = 1

    def make_call_with(self, records_count=1, parts_count=1, content_type=None, recognize_state=None):
        """
        :param records_count: int
        :param parts_count: int
        :param content_type: str (CHAT|AUDIO)
        :param recognize_state: list (["RECOGNIZED", "RE_RECOGNIZE", "NOT_RECOGNIZED", "ERROR"])
        :return: {"call_statistic": [], "call":[], "call_part":[], "call_participant":[]}
        """
        call_data = defaultdict(list)
        for i in range(records_count):
            call_data['call_statistic'] += self._call_statistic(parts_count)
            call_data['call'] += self._call(content_type, recognize_state)
            for j in range(parts_count):
                call_data['call_part'] += self._call_part()
                call_data['call_participant'] += self._call_participant()
        return call_data

    def _call_statistic(self, parts_count=1):
        _ = Field()
        holds_count = parts_count - 1
        description = (
            lambda: {"@CALL_STATISTIC_ID": _("numbers.between", maximum=9999999999),
                     "@HOLDS_COUNT": holds_count,
                     "@HOLDS_DURATION": _("numbers.between", maximum=99999),
                     "@PARTS_COUNT": parts_count,
                     "@AGENT_MESS_COUNT": _("numbers.between", maximum=9999),
                     "@CUSTOMER_MESS_COUNT": _("numbers.between", maximum=9999),
                     "@RECOGNIZE_CONFIDENCE": _("numbers.between", minimum=0, maximum=100)
                     }
        )
        schema = Schema(schema=description)
        call_statistic = schema.create(iterations=1)
        self.call_statistic_id = call_statistic[0]["@CALL_STATISTIC_ID"]
        return call_statistic

    def _call(self, content_type, recognize_state):
        date_time = Datetime('en')
        number = Numbers('en')
        call_start_date = date_time.datetime(start=2010, end=2019)
        self.call_duration = number.between(maximum=100000)
        call_finish_date = call_start_date + datetime.timedelta(milliseconds=self.call_duration)
        _ = Field()
        description = (
            lambda: {"@CALL_ID": _("numbers.between", maximum=9999999999),
                     "@CALL_UUID": _("cryptographic.uuid"),
                     "@CONTENT_TYPE": random.choice(self.CONTENT_TYPE) if not content_type else content_type,
                     "@CRM_CALL_ID": _("cryptographic.uuid"),
                     "@CALL_START_DATE": call_start_date.strftime(self.DATE_FORMAT),
                     "@CALL_REG_DATE": call_start_date.strftime(self.DATE_FORMAT),
                     "@CALL_FINISH_DATE": call_finish_date.strftime(self.DATE_FORMAT),
                     "@DIRECTION": random.choice(self.DIRECTION),
                     "@CALL_DURATION": self.call_duration,
                     "@CALL_FINISH_STATE": random.choice(self.FINISH_STATE),
                     "@LICENSE_NUMBER": _("numbers.between", maximum=99),
                     "@LICENSED": random.choice(self.LICENSED),
                     "@IS_MAPPED": False,
                     "@IS_MS_REMOVED": True,
                     "@MS_SESSION_ID": _("numbers.between", maximum=9999999999999999),
                     "@TRACK_PATH": "/tomcat/call_storage/test_calls/call_track_path.mp3",
                     "@CALL_STATISTIC_ID": self.call_statistic_id,
                     "@RECOGNIZE_STATE": random.choice(self.RECOGNIZE_STATE) if not recognize_state else random.choice(
                         recognize_state),
                     "@IS_COMMENTED": False,
                     "@CALL_PARTICIPANT_TYPE": random.choice(self.CALL_PARTICIPANT_TYPE)
                     }
        )

        schema = Schema(schema=description)
        call = schema.create(iterations=1)
        self.call_id = call[0]["@CALL_ID"]
        return call

    def _call_participant(self):
        _ = Field(providers=[CompanyProvider])
        description = (
            lambda: {"@CALL_PARTICIPANT_ID": _("numbers.between", maximum=9999999999),
                     "@CALL_PARTICIPANT_UUID": _("cryptographic.uuid"),
                     "@CALL_PARTICIPANT_AGENT_ID": None,
                     "@CALL_PARTICIPANT_TALKING_DATE": _("datetime.datetime", start=2010, end=2019).strftime(
                         self.DATE_FORMAT),
                     "@CALL_PARTICIPANT_DURATION": _("numbers.between", maximum=9999),
                     "@CALL_PARTICIPANT_FINISH_STATE": random.choice(self.FINISH_STATE),
                     "@CALL_PARTICIPANT_TYPE": random.choice(self.PARTICIPANT_PARTICIPANT_TYPE),
                     "@CALL_PARTICIPANT_PHONE": _("company.phone"),
                     "@CALL_PARTICIPANT_RECORDER": _("internet.ip_v4"),
                     "@CALL_PARTICIPANT_TRACK_PATH": "/tomcat/call_storage/test_calls/call_part_track_path.mp3",
                     "@CALL_PARTICIPANT_XREFCI": _('company.xrefci'),
                     "@CALL_ID": self.call_id,
                     "@CALL_PART_ID": self.call_part_id,
                     "@CALL_PARTICIPANT_USER_ID": None,
                     "@CALL_PARTICIPANT_MESSENGER_TYPE": random.choice(self.MESSENGER_TYPE)
                     }
        )

        schema = Schema(schema=description)
        call_participant = schema.create(iterations=random.randint(1, 4))
        return call_participant

    def _call_part(self):
        _ = Field(providers=[CompanyProvider])
        description = (
            lambda: {"@CALL_PART_ID": _("numbers.between", maximum=9999999999),
                     "@CALL_PART_UUID": _("cryptographic.uuid"),
                     "@CALL_TYPE": random.choice(self.CALL_TYPE),
                     "@CALL_PART_START_TIME": _("datetime.datetime", start=2010, end=2019).strftime(self.DATE_FORMAT),
                     "@CALL_PART_DURATION": _("numbers.between", maximum=9999),
                     "@CALL_PART_FINISH_STATE": random.choice(self.FINISH_STATE),
                     "@PART": self.call_part_number,
                     "@TRACK_PATH": "/tomcat/call_storage/test_calls/call_part_track_path.mp3",
                     "@STREAM_PATH1": "/tomcat/call_storage/test_calls/call_part_stream_path1.mp3",
                     "@CALL_ID": self.call_id,
                     "@STREAM_PATH2": "/tomcat/call_storage/test_calls/call_part_stream_path2.mp3",
                     }
        )
        schema = Schema(schema=description)
        call_part = schema.create(iterations=1)
        self.call_part_id = call_part[0]["@CALL_PART_ID"]
        return call_part


class DictionaryBuilder:
    pass


class ClientRequestBuilder:
    DATA_TYPE = ["STRING", "DATETIME", "DATE", "TIME", "INTEGER", "FLOAT", "TEXT", "DICTIONARY"]
    FIELD_TYPE = ["SYSTEM", "FIXED", "ADDED", "JOINED"]

    json = {"$cmGroupRid": None,
            "data_type": None,
            "fieldtype": "ADDED",
            "field_name": "test_str_name",
            "fromDictionary": None,
            "relation_all": None,
            "defaultValue": None,
            "inputType": "EDIT",
            "showType": "MAIN",
            "isUnique": 0,
            "useForFilter": 0,
            "table_name": "CLIENTS",
            "title": "test_str_title",
            "fieldSize": 1,
            "inputFullSize": 0,
            "useInGroupBy": False}



english = Generator('en')
russian = Generator('ru')
ukrainian = Generator('uk')
