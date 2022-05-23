import pytest
import os
from collections import deque
from helpers.product_utils import user_params
from bin.project import send
from Data.url import mgr
from definition import ROOT_DIR
from selene.support.shared import browser, config
from Data.generics import english


@pytest.fixture(scope="module")
def immutable_group_with_child():
    """
    :return: {}
    """
    groups_id = deque([], maxlen=5)
    data = {"$name": english.unique_name,
            "$parentGroupId": user_params.root_group_id}
    response_parent = send.post(mgr.groups, data)
    groups_id.appendleft(response_parent.json()['groupId'])
    data_child = {"$name": english.unique_name,
                  "$parentGroupId": groups_id[0]}
    response_child = send.post(mgr.groups, data_child)
    groups_id.appendleft(response_child.json()['groupId'])
    response = send.get(mgr.groups, id_to_url=groups_id[1])
    yield response.json()
    for i in groups_id:
        send.delete(mgr.groups, id_to_url=i + 's')


def session_finish(session):
    try:
        file_dir = os.environ['test_results_dir']
    except KeyError:
        file_dir = ROOT_DIR
    reporter = session.config.pluginmanager.get_plugin('terminalreporter')
    with open(os.path.join(file_dir, "test_results.txt"), 'w') as f:
        if 'failed' in reporter.stats:
            f.write("FAILED: {}\n".format(len(reporter.stats['failed'])))
        else:
            f.write("FAILED: 0\n")
        if 'passed' in reporter.stats:
            f.write("PASSED: {}\n".format(len(reporter.stats['passed'])))
        else:
            f.write("PASSED: 0\n")


@pytest.fixture(scope='function', autouse=True)
def setup_driver(request):
    # browser = Browser(Config(
    #     driver=Chrome(),
    #     window_height=1000,
    #     window_width=1920,
    #     timeout=10))
    opened_browser = False
    if request.module.__name__.endswith('web'):
        config.timeout = 10
        config.browser_name = 'chrome'
        config.window_height = 1000
        config.window_width = 1920
        config.hold_browser_open = True
        opened_browser = True
    yield
    if opened_browser:
        browser.quit()
