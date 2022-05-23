from bin.common import MyEnum


class mgr(MyEnum):
    current_user = "/CompanyManager/adm/management/users/current"
    groups = "/CompanyManager/adm/management/groups"
    roles = "/CompanyManager/adm/management/roles"
    users = "/CompanyManager/adm/management/users"
    users_search = "/CompanyManager/adm/management/users/search"
    AD_search = "/CompanyManager/adm/management/import/active-directory/users/search"
    domains = "/CompanyManager/adm/admin/active-directory/domains"
    import_users = "/CompanyManager/adm/management/import/users"
    ad_users_sources = "/CompanyManager/adm/admin/active-directory/ad-users-sources"
    recover = "/CompanyManager/adm/management/users/$userId/recover"
    account = "/CompanyManager/adm/management/users/current/account"
    names = "/CompanyManager/adm/admin/active-directory/domains/names"
    user_group_roles = "CompanyManager/adm/management/users/$userId/user-group-roles"
    user_role = "/CompanyManager/adm/management/users/$userId/roles"


class qm(MyEnum):
    blanks = "/QualityManagement/qm/blanks"
    sections = "/QualityManagement/qm/blanks/$id/sections"
    criteria = "/QualityManagement/qm/blank/criteria-groups"
    scales = "/QualityManagement/qm/scales"


class rec(MyEnum):
    calls_search = "/CompanyRecording-CallProvider/smr/call-provider/calls/search"
    tag_to_call = "/CompanyRecording-CallProvider/smr/call-provider/crm/tag-to-call"
    tag_from_call = "/CompanyRecording-CallProvider/smr/call-provider/crm/tag-from-call"
    tags = "/CompanyRecording-CallProvider/smr/call-provider/tags"
    comment = "/CompanyRecording-CallProvider/smr/call-provider/calls/$callId/comments"
    chat_history = "/CompanyRecording-CallProvider/smr/call-provider/calls/$callId/chat-history"
    chat_histories = "/CompanyRecording-CallProvider/smr/call-provider/calls/$callId/call-parts/$callPartId/chat-histories"
    tags_search = "/CompanyRecording-CallProvider/smr/call-provider/tags/search"
    calls = "/CompanyRecording-CallProvider/smr/call-provider/calls"
    confidence_settings = "/CompanyRecording-CallProvider/smr/speech-recognizer/confidence-settings"
    re_recognize = "/CompanyRecording-CallProvider/smr/call-provider/calls/re-recognize"
    recognizer_settings = "/CompanyRecording-CallProvider/smr/speech-recognizer/settings"
    recognizer_settings_activate = "/CompanyRecording-CallProvider/smr/speech-recognizer/settings/$speechRecognizerSettingsRid/activate"


class AuthServer(MyEnum):
    token = "/CompanyAuthorizationServer/sas/token"
    auth = "/CompanyAuthorizationServer/sas/auth"


class smc(MyEnum):
    connectors = "/MessengerGateway/smc/connectors"
    accounts = "/MessengerGateway/smc/accounts"


class TRUM(MyEnum):
    clients = "/TRUM/trum/clients"
    profiles = "/Trum/trum/profiles"


class scm(MyEnum):
    groups = "/ContactManager-ClientCards/groups"
    groups_search = "/ContactManager-ClientCards/groups/search"
    clients = "/groups/$groupRid/clients"
    clients_search = "/groups/$groupRid/clients/search"
    requests = "/groups/$groupRid/requests"
    requests_search = "/groups/$groupRid/requests/search"
    dictionaries = "/ContactManager-Admin/dictionaries"
    dictionaries_search = "/ContactManager-Admin/dictionaries/search"
    dictionaries_tree = "/ContactManager-Admin/dictionaries/tree"
    dictionaries_text = "/ContactManager-Admin/dictionaries/text"
    dictionaries_related = "/ContactManager-Admin/dictionaries/related"
    clients_fields = "/ContactManager-Admin/groups/$groupId/fields"
    request_fields = "/ContactManager-Admin/groups/$groupId/fields"
    group_fields_search = "/ContactManager-Admin/groups/$group_id/fields/search"
    reports = "/ContactManager-Admin/groups/$group_id/reports"
