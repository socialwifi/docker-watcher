import typing

from dataclasses import dataclass


@dataclass
class Container:
    id: str
    name: str
    status: str
    error: str

    @property
    def display_name(self):
        name = self.name.split('_default_')[0]
        name = name.replace('/k8s_', '').split('_')[0]
        return name

    def as_dict(self):
        return {'id': self.id, 'name': self.display_name, 'status': self.status, 'error': self.error}


class LogTypes:
    HTTP = 'http'
    LOGGER = 'logger'


@dataclass
class LogRow:
    text: str
    debug: [str, None]
    type: str

    def as_dict(self):
        return {'text': self.text, 'debug': self.debug, 'type': self.type}


@dataclass
class Microservice:
    label: str
    containers: typing.List[Container]

    def as_dict(self):
        return {'label': self.label, 'containers': [c.as_dict() for c in self.containers]}
