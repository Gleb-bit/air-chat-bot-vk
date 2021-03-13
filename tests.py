import unittest
from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock

from pony.orm import db_session, rollback

from generate_ticket import generate_ticket
from settings import INTENTS, SCENARIOS, DEFAULT_ANSWER
from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new', 'object': {
        'message': {'date': 1586168893, 'from_id': 289605203, 'id': 85, 'out': 0, 'peer_id': 289605203,
                    'text': 'бот', 'conversation_message_id': 84, 'fwd_messages': [], 'important': False,
                    'random_id': 0, 'attachments': [], 'is_hidden': False},
        'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'], 'keyboard': True,
                        'inline_keyboard': True, 'lang_id': 0}}, 'group_id': 193249309,
                 'event_id': '6d59c96ac2fbc358f600b58f64125fd8858c54ba'}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    INPUTS = [
        'Привет',
        '/help',
        '/ticket',
        'интересен лос-анджелесский рейс',
        "мне нужен рейс из нью-йорка",
        '20/05/2020',
        "20-05-2020",
        "1",
        '1',
        "something",
        "да",
        "+55555555555",
        'Вениамин'
    ]
    EXPECTED_OUTPUTS = [
        DEFAULT_ANSWER,
        INTENTS[0]['answer'],
        SCENARIOS['start_scenario']['steps']['step1']['text'],
        SCENARIOS['start_scenario']['steps']['step2']['text'],
        SCENARIOS['start_scenario']['steps']['step3']['text'],
        SCENARIOS['start_scenario']['steps']['step3']['failure_text'],
        "Пожалуйста, выберите из предложенных рейсов один(введите номер): {1: '20-05-2020', 2: '21-05-2020'}",
        SCENARIOS['start_scenario']['steps']['step5']['text'],
        SCENARIOS['start_scenario']['steps']['step6']['text'],
        SCENARIOS['start_scenario']['steps']['step7']['text'].format(dep_city="Лос-Анджелес", dest_city="Нью-Йорк",
                                                                     flight=INPUTS[6], number_of_tickets=INPUTS[8],
                                                                     commentary=INPUTS[9]),
        SCENARIOS['start_scenario']['steps']['step8']['text'],
        SCENARIOS['start_scenario']['steps']['step9']['text'],
        SCENARIOS['start_scenario']['steps']['step10']['text']
    ]

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))
        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        ticket_file = generate_ticket(dep_city='Лондон', dest_city='Москва', flight='24-05-2020', fio='someone')

        with open('files/ticket_example.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file.read() == expected_bytes


if __name__ == '__main__':
    unittest.main()
