import docker

import settings

from schemas import dataclasses


class DockerClientCases:
    requests = ['GET', 'POST', 'PATCH', 'DELETE']

    def __init__(self):
        self.client = docker.from_env()

    def get_microservices_containers(self):
        containers = self._get_docker_containers()
        for container in containers:
            if self._is_microservice(container.attrs['Name']):
                yield dataclasses.Container(
                    id=container.attrs['Id'],
                    name=container.attrs['Name'],
                    status=container.attrs['State']['Status'],
                    error=container.attrs['State']['Error'],
                )

    def _get_docker_containers(self):
        return self.client.containers.list()

    @staticmethod
    def _is_microservice(name):
        return any([f'k8s_{label}' in name for label in settings.MICROSERVICES_LABELS])

    def stream_container_logs(self, container_id):
        for element in self._get_raw_log_stream(container_id):
            element = element.decode('utf-8')
            if self._should_process(element):
                if self._is_http_request_log(element):
                    element = element.split('"')
                    element = element[1].strip()
                    for method in self.requests:
                        if method in element and not element.startswith(method):
                            element = element.split(method)[1]
                            element = f'{method}{element}'
                    element = element.split(' HTTP/')[0]
                    yield dataclasses.LogRow(text=element, type=dataclasses.LogTypes.HTTP, debug=None)
                else:
                    if '|' in element:
                        elements = element.split('|')
                        log_name = self._parse_log_name(elements)
                        debug = self._parse_log_debug(elements)
                        yield dataclasses.LogRow(text=log_name, type=dataclasses.LogTypes.LOGGER, debug=debug)
                    else:
                        yield dataclasses.LogRow(text=element, type=dataclasses.LogTypes.LOGGER, debug=None)

    def _get_raw_log_stream(self, container_id):
        container = self.client.containers.get(container_id)
        return container.logs(stream=True)

    @staticmethod
    def _should_process(element):
        not_health = 'GET /healthz/' not in element
        not_webpack = 'webpack.Progress' not in element
        return not_webpack and not_health

    def _is_http_request_log(self, element):
        return any([f'{method} ' in element for method in self.requests])

    @staticmethod
    def _parse_log_name(elements):
        log_name = elements[0].strip().split(' ')
        log_name.reverse()
        parts = []
        for element in log_name:
            if not element.isnumeric():
                parts.append(element)
            else:
                break
        parts.reverse()
        return ' '.join(parts)

    @staticmethod
    def _parse_log_debug(elements):
        debug = elements[1].strip().replace('extra=', '')
        if debug != '{}':
            debug = debug.replace(', ', ', \n').replace('{', '{\n').replace('}', '\n}')
        return debug

    def get_current_container_id_for_name(self, name):
        containers = self.get_microservices_containers()
        for container in containers:
            if container.display_name == name:
                return container.id
