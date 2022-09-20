import eel

from use_cases import docker_cases
from use_cases import microservices_cases


def get_serialized_services():
    containers = docker_cases.DockerClientCases().get_microservices_containers()
    services = microservices_cases.group_containers_by_microservice(containers)
    return [service.as_dict() for service in services]


def stream_logs_for_container(container_name):
    container_id = docker_cases.DockerClientCases().get_current_container_id_for_name(container_name)
    if container_id:
        logs = docker_cases.DockerClientCases().stream_container_logs(container_id)
        for log in logs:
            eel.push_container_log(container_name, log.as_dict())
            print('- push_container_log', container_name)
            eel.sleep(0.05)
    else:
        eel.sleep(2)

    stream_logs_for_container(container_name)
