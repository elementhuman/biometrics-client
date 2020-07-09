"""

    Test Client
    ~~~~~~~~~~~

"""
import responses
from urllib.parse import urljoin
from biometrics_client import client
from tests import TEST_VIDEO_PATH, DUMMY_ACCESS_KEY, DUMMY_SECRET_KEY

FAKE_TASK_ID: str = "fake-task-id"
PING_PAYLOAD = dict(response="PONG", version="99")
APPLY_PAYLOAD = dict(response=dict(task_id=FAKE_TASK_ID), version="99")
RESULTS_PAYLOAD = dict(response=dict(frames={}, summary={}), version="99")


def test_credentials(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    assert dummy_ehb_client.credentials == {
        "x-access-key": DUMMY_ACCESS_KEY,
        "x-secret-key": DUMMY_SECRET_KEY,
    }


@responses.activate
def test_ping(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    responses.add(
        responses.GET,
        url=urljoin(dummy_ehb_client.url, "ping"),
        json=PING_PAYLOAD,
        status=200,
    )
    assert dummy_ehb_client.ping() == PING_PAYLOAD


@responses.activate
def test_apply(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    responses.add(
        responses.POST,
        url=urljoin(dummy_ehb_client.url, "apply"),
        json=APPLY_PAYLOAD,
        status=202,
    )
    assert dummy_ehb_client.apply(TEST_VIDEO_PATH) == APPLY_PAYLOAD


@responses.activate
def test_results(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    responses.add(
        responses.GET,
        url=urljoin(dummy_ehb_client.url, f"results/{FAKE_TASK_ID}"),
        json=RESULTS_PAYLOAD,
        status=200,
    )
    assert dummy_ehb_client.results(FAKE_TASK_ID) == RESULTS_PAYLOAD


@responses.activate
def test_apply_and_wait(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    responses.add(
        responses.POST,
        url=urljoin(dummy_ehb_client.url, "apply"),
        json=APPLY_PAYLOAD,
        status=202,
    )
    responses.add(
        responses.GET,
        url=urljoin(dummy_ehb_client.url, f"results/{FAKE_TASK_ID}"),
        json=RESULTS_PAYLOAD,
        status=200,
    )
    assert dummy_ehb_client.apply_and_wait(TEST_VIDEO_PATH) == (
        FAKE_TASK_ID,
        RESULTS_PAYLOAD,
    )
