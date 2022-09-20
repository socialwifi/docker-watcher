from schemas import dataclasses


class TestContainerDataclass:
    def test_if_display_name_is_returned(self):
        name = '/k8s_hyd-home_hyd-home-58d66f9c65-6qb8l_default_77bee0fa-1a13-11ed-ba29-7085c276966e_9'
        container = dataclasses.Container(id='', name=name, status='', error='')
        assert container.display_name == 'hyd-home'

        name = '/k8s_hyd-business-admin_hyd-business-admin-7c7ffd7ff9-wp88m_default_7c2baab9-194b-11ed-bb45-7085966e_10'
        container = dataclasses.Container(id='', name=name, status='', error='')
        assert container.display_name == 'hyd-business-admin'

    def test_if_container_serializes(self):
        name = '/k8s_hyd-home_hyd-home-58d66f9c65-6qb8l_default_77bee0fa-1a13-11ed-ba29-7085c276966e_9'
        container = dataclasses.Container(id='aaa', name=name, status='running', error='xxx')

        serialize = container.as_dict()
        assert serialize == {'id': 'aaa', 'name': 'hyd-home', 'status': 'running', 'error': 'xxx'}

    def test_if_log_row_serializes(self):
        log = dataclasses.LogRow(text='pomidor', debug='{}', type='logger')

        serialize = log.as_dict()
        assert serialize == {'text': 'pomidor', 'debug': '{}', 'type': 'logger'}

    def test_if_microservice_serializes(self):
        name = '/k8s_hyd-home_hyd-home-58d66f9c65-6qb8l_default_77bee0fa-1a13-11ed-ba29-7085c276966e_9'
        container = dataclasses.Container(id='aaa', name=name, status='running', error='xxx')
        service = dataclasses.Microservice(label='abc', containers=[container])

        serialize = service.as_dict()
        expected = {
            'label': 'abc',
            'containers': [{'id': 'aaa', 'name': 'hyd-home', 'status': 'running', 'error': 'xxx'}],
        }
        assert serialize == expected
