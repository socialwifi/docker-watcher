import settings

from schemas import dataclasses


def group_containers_by_microservice(containers_list):
    containers_list = list(containers_list)
    for service_name in settings.MICROSERVICES_LABELS:
        containers = list(filter(lambda container: service_name in container.name, containers_list))
        containers = list(sorted(containers, key=lambda c: c.name))
        yield dataclasses.Microservice(label=service_name, containers=containers)
