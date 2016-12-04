#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nose.tools import *
from ddt import ddt, data, unpack

import messageparser


@ddt
class TestsMessageParser(object):
    @data(
        'user1 > user2: ok :)',
        'user1 >> user2: ok :)'
    )
    def test_when_message_contains_two_or_one_less_than_symbols_in_second_column_is_directed_should_return_true(self,
                                                                                                                message):
        output = messageparser.is_directed(message)
        assert_true(output)

    def test_when_message_contains_two_less_than_symbols_in_second_column_is_private_directed_should_return_true(self):
        output = messageparser.is_directed_private('user1 >> user2: ok :)')
        assert_true(output)

    @data(
        'user1 > user2: nie ok :(',
        'abc',
        'Bla bla blaaa',
        '',
    )
    def test_when_message_not_contains_two_less_than_symbols_in_second_column_is_private_directed_should_return_false(
            self, message):
        output = messageparser.is_directed_private(message)
        assert_false(output)

    @data(
        ('user1 > user2: nie ok :(', 'user1'),
        ('user1 >> user2: nie ok :(', 'user1')
    )
    @unpack
    def test_get_sender_from_should_return_sender_from_directed_message(self, message, expected_sender):
        sender = messageparser.get_sender_from(message)
        assert_equal(sender, expected_sender)

    @data(('user1 > user2: ok :) | http://link.to.message', 'ok :)'),
          ('user1 >> user2: nie ok :( | http://link.to.message', 'nie ok :('),
          ('user1 >> user2: : aaaaa ::: bbbb : | http://link.to.message', ': aaaaa ::: bbbb :'),
          ('user1 >> user2: : hello! | http://link.to.message', ': hello!'),
          ('user1 >> user2: ||| hello! | http://link.to.message', '||| hello!')
          )
    @unpack
    def test_get_content_from_should_return_contents_from_directed_message(self, message, expected_content):
        content = messageparser.get_content_from(message)
        assert_equal(content, expected_content)

    def test_when_message_has_add_command_has_add_command_metod_should_return_true(self):
        message = 'someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny'

        output = messageparser.has_add_command(message)

        assert_true(output)

    def test_when_message_has_add_command_has_not_add_command_metod_should_return_false(self):
        message = 'someuser >> bot: Jan Kowalski, Winogronowa 123/3, Pcim Dolny'

        output = messageparser.has_add_command(message)

        assert_false(output)

    @data(
        ('someuser >> bot: dodaj Jan Kowalski, Winogronowa 123/3, Pcim Dolny',
         'Jan Kowalski, Winogronowa 123/3, Pcim Dolny'),
        ('someuser >> bot: dodaj Świnka Peppa Bekonu 3 12-345 Warszawa', 'Świnka Peppa Bekonu 3 12-345 Warszawa'),
        ('someuser >> bot: dodaj Agnieszka Kowalska Juztutajniemieszka 123 11-111 Brzydgoszcz',
         'Agnieszka Kowalska Juztutajniemieszka 123 11-111 Brzydgoszcz')
    )
    @unpack
    def test_when_message_has_add_command_get_user_data_from_method_should_extract_user_data(self, message,
                                                                                             expected_user_data):
        user_data = messageparser.get_user_data_from(message)

        assert_equal(expected_user_data, user_data)

    def test_when_message_content_is_not_empty_get_command_from_should_return_first_word_from_message_content(self):
        message_content = 'rule the world!'
        expected_command = 'rule'

        command = messageparser.get_command_from(message_content)

        assert_equal(command, expected_command)

    def test_when_message_content_is_empty_get_command_from_should_return_none(self):
        message_content = ''

        command = messageparser.get_command_from(message_content)

        assert_equal(command, None)

    def test_when_message_content_is_not_empty_remove_command_from_should_return_message_content_without_first_word(self):
        message_content = 'rule the world!'
        expected_content = 'the world!'

        content_without_command = messageparser.remove_command_from(message_content)

        assert_equal(content_without_command, expected_content)

    def test_when_message_content_is_empty_remove_command_from_should_return_none(self):
        message_content = ''

        command = messageparser.remove_command_from(message_content)

        assert_equal(command, None)
