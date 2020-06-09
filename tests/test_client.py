"""

    Test Client
    ~~~~~~~~~~~

"""
import responses
from urllib.parse import urljoin
from biometrics_client import client
from tests import TEST_VIDEO_PATH

FAKE_TASK_ID: str = "fake-task-id"
APPLY_PAYLOAD = dict(response=dict(task_id=FAKE_TASK_ID), version="99")
RESULTS_PAYLOAD = dict(response=dict(frames={}, summary={}), version="99")


@responses.activate
def test_ping(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    payload = dict(response="PONG", version="99")
    responses.add(
        responses.GET,
        url=urljoin(dummy_ehb_client.url, "ping"),
        json=payload,
        status=200,
    )
    assert dummy_ehb_client.ping() == payload


@responses.activate
def test_apply(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    responses.add(
        responses.POST,
        url=urljoin(dummy_ehb_client.url, "apply"),
        json=APPLY_PAYLOAD,
        status=200,
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
        status=200,
    )
    responses.add(
        responses.GET,
        url=urljoin(dummy_ehb_client.url, f"results/{FAKE_TASK_ID}"),
        json=RESULTS_PAYLOAD,
        status=200,
    )
    assert dummy_ehb_client.apply_and_wait(TEST_VIDEO_PATH) == (FAKE_TASK_ID, RESULTS_PAYLOAD)
