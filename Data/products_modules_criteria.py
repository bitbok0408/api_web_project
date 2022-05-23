from bin.common import MyEnum


class Recording(MyEnum):
    """
    {"search_param":"object_path_to_this_param"}
    """
    calls_metadata = ["callCrmCallId", "callId", "callDirection", "callState", "callContentType",
                      "hasComment", "callDate"]
    calls_duration = ["callDurationFrom", "callDurationTo", "callDuration", ]
    calls_holds_parts = ["holdsCount", "holdsDuration", "partsCount", ]

    custom_params = ["holdsCountFrom", "holdsCountTo", "holdsDurationFrom", "holdsDurationTo",
                     "partsCountFrom", "partsCountTo", "qmResultFrom", "qmResultTo", "callDateFrom", "callDateTo", ]

    calls_user = ["userId", "userLogin", "firstName", "lastName", "loginAd", "groupId", "participantPhone", ]
    call_info = ["callTags",  "callParticipantType", ]
    call_messages = ["message", ]
    call_recognition = ["recognitionText", "callKeywords", ]
    calls_qm = ["qmStatus", "qmAgent", "qmManager",  "qmFormName",
                "qmDateFrom", "qmDateTo", ]



    only_from_DB = ["callCcid", "callMsSessionId"]


class Manager(MyEnum):
    test = 'test'


class ContactManager:
    client_field_datatype = ["STRING", "DATETIME", "DATE", "TIME", "INTEGER", "FLOAT", "TEXT", "DICTIONARY"]
    client_field_field_type = ["SYSTEM", "FIXED", "ADDED", "JOINED"]



