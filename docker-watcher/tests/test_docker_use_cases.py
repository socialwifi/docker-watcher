from unittest import mock

from use_cases import docker_cases
from tests import factories


class TestDockerCases:
    @mock.patch('use_cases.docker_cases.DockerClientCases._get_docker_containers')
    def test_if_matching_container_is_returned(self, get_containers):
        name = '/k8s_hyd-message_hyd-message-5c686966-8sxr4_default_997929db-1efd-11ed-81e0-7085c276966e_8'
        container = factories.FakeContainer(name)
        get_containers.return_value = [container]

        result = list(docker_cases.DockerClientCases().get_microservices_containers())
        assert len(result) == 1
        assert result[0].name == name

    @mock.patch('use_cases.docker_cases.DockerClientCases._get_docker_containers')
    def test_if_other_container_is_not_returned(self, get_containers):
        name = '/k8s_hyd-pomidor_hyd-message-5c686966-8sxr4_default_997929db-1efd-11ed-81e0-7085c276966e_8'
        container = factories.FakeContainer(name)
        get_containers.return_value = [container]

        result = list(docker_cases.DockerClientCases().get_microservices_containers())
        assert len(result) == 0

    @mock.patch('use_cases.docker_cases.DockerClientCases._get_raw_log_stream')
    def test_if_http_logs_are_streamed(self, log_stream):
        log_stream.return_value = [
            b'INFO 2022-09-14 12:28:27,979 _internal 7 140588799993600 172.17.0.59 - - [14/Sep/2022 12:28:27] "GET '
            b'/welcome/59973754-f993-4b1a-999f-98796eb3db34/ HTTP/1.0" 200 - | extra={}',
            b'INFO 2022-09-14 12:28:28,024 _internal 7 140588799993600 172.17.0.59 - - [14/Sep/2022 12:28:28] "GET '
            b'/style/welcome_page/3e37b929-28ab-4afa-bfe9-8dd4a125b952/ HTTP/1.0" 200 - | extra={}',
        ]
        result = list(docker_cases.DockerClientCases().stream_container_logs('id1234'))
        assert len(result) == 2
        assert result[0].text == 'GET /welcome/59973754-f993-4b1a-999f-98796eb3db34/'
        assert result[0].type == 'http'
        assert result[0].debug is None
        assert result[1].text == 'GET /style/welcome_page/3e37b929-28ab-4afa-bfe9-8dd4a125b952/'

    @mock.patch('use_cases.docker_cases.DockerClientCases._get_raw_log_stream')
    def test_if_custom_logger_log_is_streamed(self, log_stream):
        log_stream.return_value = [
            b"INFO 2022-09-15 09:03:07,891 debug 7 139651046168320 RadiusCompleteDynamicRedirectView | extra="
            b"{'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0', 'referer"
            b"': 'http://logging.sw.com/', 'method': 'GET', 'request_args': ImmutableMultiDict([]), 'form': "
            b"ImmutableMultiDict([]), 'url': 'http://login.testing/radius/complete/4d81bb69-de40-4a31-ba97-5ef1079dd587"
            b"/', 'controller_id': '4d81bb69-de40-4a31-ba97-5ef1079dd587', 'user_mac': '00:01:24:80:b3:9c', 'device_mac"
            b"': '00:01:02:03:04:ff', 'venue_id': '22222222-2222-2222-2222-222222222222', 'login_method': 'autologin'}"
        ]
        result = list(docker_cases.DockerClientCases().stream_container_logs('id1234'))
        assert len(result) == 1
        assert result[0].text == 'RadiusCompleteDynamicRedirectView'
        assert 'Mozilla/5.0' in result[0].debug
        assert result[0].type == 'logger'

    @mock.patch('use_cases.docker_cases.DockerClientCases._get_raw_log_stream')
    def test_if_non_specific_logs_are_streamed(self, log_stream):
        log_stream.return_value = [
            b"ERROR 2022-09-15 08:01:46,386 consumer 1 139861207037760 consumer: Cannot connect to amqp://guest:**@dev"
            b"-rabbitmq:5672//: failed to resolve broker hostname.",
            b"INFO 2022-09-15 08:36:48,732 trace 8 139861207037760 Task live_export.get_user_export_data[2b9674eb-d065"
            b"-4e6b-9601-facabcae361c] succeeded in 0.042755537999710214s: None | extra={'data': {'id': '2b9674eb-d065-"
            b"4e6b-9601-facabcae361c', 'name': 'live_export.get_user_export_data', 'return_value': 'None', 'runtime':"
            b" 0.042755537999710214}}"
        ]
        result = list(docker_cases.DockerClientCases().stream_container_logs('id1234'))
        assert len(result) == 2
        assert 'consumer: Cannot connect to amqp' in result[0].text
        assert 'Task live_export.get_user_export_data' in result[1].text
