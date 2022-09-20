import gevent.monkey
gevent.monkey.patch_all()

import eel

from use_cases import eel_cases


CONTAINERS_WITH_STREAMING = []


@eel.expose
def start_log_stream(container_name):
    print('start_log_stream', container_name)

    def start_stream():
        eel_cases.stream_logs_for_container(container_name)

    if container_name not in CONTAINERS_WITH_STREAMING:
        print('start_log_stream', container_name)
        CONTAINERS_WITH_STREAMING.append(container_name)
        eel.spawn(start_stream)
    else:
        print('Already streaming', container_name)


eel.init('web')
eel.sleep(1)
eel.start('index.html', block=False)
eel.sleep(1)
eel.push_microservices(eel_cases.get_serialized_services())


while True:
    print("I'm a main loop")
    eel.sleep(1)
