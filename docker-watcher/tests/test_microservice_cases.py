from unittest import mock

from schemas import dataclasses
from use_cases import microservices_cases


class TestDockerCases:
    def test_if_containers_are_grouped(self):
        name = '/k8s_hyd-message_hyd-message-5c686966-8sxr4_default_997929db-1efd-11ed-81e0-7085c276966e_8'
        container_message1 = dataclasses.Container(id='a', name=name, status='', error='')
        name = '/k8s_hyd-message-automation-worker_hyd-message-automation-worker-5c686966-8sxr4_def'
        container_message2 = dataclasses.Container(id='b', name=name, status='', error='')
        name = '/k8s_sw-mailer-mass-mailing-celery_sw-mailer-mass-mailing-celery-7dccccfbd7-qmlx4_default_835bfc1d-e7dd'
        container_mailer = dataclasses.Container(id='c', name=name, status='', error='')
        containers_list = [container_mailer, container_message1, container_message2]

        with mock.patch('settings.MICROSERVICES_LABELS', ['sw-mailer', 'hyd-message']):
            result = list(microservices_cases.group_containers_by_microservice(containers_list))
        assert len(result) == 2

        assert result[0].label == 'sw-mailer'
        assert len(result[0].containers) == 1

        assert result[1].label == 'hyd-message'
        assert len(result[1].containers) == 2
