#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from random import randint, sample
from time import time
import sys
import os
# Require when you haven't GLXBob as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
import GLXBob


# Unittest
class TestEventBus(unittest.TestCase):
    def setUp(self):
        # Before the test start
        self.event_bus = GLXBob.EventBus()
        sys.stdout.write(str(self.shortDescription() + ' ... '))

    def tearDown(self):
        # When the test is finish
        sys.stdout.write('OK\n')
        sys.stdout.flush()

    def do_nothing(self):
        pass

    def test_get_set_data(self):
        """EventBus: Test 'data' attribute with 'EventBus.set_data()' and 'EventBus.get_data()' method's """
        value_random_1 = str(randint(8, 250))
        value_random_2 = str(randint(8, 250))
        self.event_bus.set_data(value_random_1, value_random_2)
        self.assertEqual(self.event_bus.get_data(value_random_1), value_random_2)

    def test_if_connect_increase_signal_handlers_list_size(self):
        """EventBus: Test if signal_handlers_list increase when use EventBus.connect() """
        value_tested = len(self.event_bus.signal_handlers)
        value_random = str(randint(8, 250))
        self.event_bus.connect(value_random, self.do_nothing)
        self.assertEqual(value_tested + 1, len(self.event_bus.signal_handlers))

    # def test_get_set__is_running(self):
        # handle_1 = self.event_bus.connect("coucou1", print_hello1)
        # handle_2 = self.event_bus.connect("coucou1", print_hello2)
        # handle_3 = self.event_bus.connect("coucou1", print_hello3)
        # handle_4 = self.event_bus.connect("coucou2", print_hello2)
        # handle_5 = self.event_bus.connect("coucou3", print_hello3)
        # print('Before:')
        # # for subcription in event.signal_handlers:
        # #     print(subcription)
        #
        # for detailed_signal, infos in event_bus.signal_handlers.iteritems():
        #     print(detailed_signal)
        #     for handler_id, infos2 in infos.iteritems():
        #         print(str(handler_id) + ": " + str(infos2))
        #
        # print('After:')
        # # event.disconnect(handle_1)
        #
        #
        # # handle_1 = event.connect("coucou1", print_hello1, '1', '2', '3')
        # #
        # # # Do Nothing but that cool
        # event_bus.handler_block(handle_1)
        # # event.handler_unblock(handle_1)
        # #
        # # # Do Nothing but that cool
        # event_bus.handler_block_by_func(print_hello2)
        # event_bus.handler_unblock_by_func(print_hello2)
        # #
        # for detailed_signal, infos in event_bus.signal_handlers.iteritems():
        #     print(detailed_signal)
        #     for handler_id, infos2 in infos.iteritems():
        #         print(str(handler_id) + ": " + str(infos2))
        # if event_bus.handler_is_connected(handle_1):
        #     event_bus.emit('coucou1')
        # event_bus.emit('coucou1')
        # # event.emit('coucou3', 'mais si on sait')
        # #
