"""

    Test Client
    ~~~~~~~~~~~

"""
import responses
from urllib.parse import urljoin
from biometrics_client import client
from tests import TEST_VIDEO_PATH


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
    payload = dict(response=dict(task_id="fake-task-id"), version="99")
    responses.add(
        responses.POST,
        url=urljoin(dummy_ehb_client.url, "apply"),
        json=payload,
        status=200,
    )
    assert dummy_ehb_client.apply(TEST_VIDEO_PATH) == payload


@responses.activate
def test_results(dummy_ehb_client: client.ElementHumanBiometrics) -> None:
    fake_task_id: str = "fake-task-id"
    payload = dict(response=dict(frames={}, summary={}), version="99")
    responses.add(
        responses.GET,
        url=urljoin(dummy_ehb_client.url, f"results/{fake_task_id}"),
        json=payload,
        status=200,
    )
    assert dummy_ehb_client.results(fake_task_id) == payload
