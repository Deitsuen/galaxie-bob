#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import time, sleep, localtime
import os
import psutil

import math


# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved


class Signal(Exception):
    """Generic exception for Galaxie-BoB"""

    def __init__(self, msg, original_exception, callback=None):
        super(Signal, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception

        # Quit Message
        if msg == 'QUIT':
            print('original_exception: ' + str(self.original_exception))
            if callback is None:
                return
            else:
                callback()


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class MainLoop(object):
    """
    ********
    MainLoop
    ********

    The MainLoop is something close to a infinity loop with a start() and stop() method

    The main loop make work and sleep the necessary time for impose a Frame Rate. Default 25
    """

    # __metaclass__ = Singleton

    def __init__(self):
        """
        Initialize the mainloop and all attributes
        """
        self.event_buffer = list()
        self._is_running = False

        # context_list
        self.context_list = list()
        self.default_context = None
        self._Signal__excepthook_ = None

        # Time Strech
        self.step_size = 25
        self.max_step_size = 60
        self.min_step_size = 1

    def get_max_period_time(self):
        """
        If duration between frames is greater than this value, timeout will be consider.

        :return: the max period in second
        :rtype: float
        """
        return 1.0 / self.min_step_size

    def set_step_size(self, value=25):
        """
        Set the tps attribute, number of milliseconds between each step

        :param value:
        :raise ValueError: If parameter value is not a float or a int
        """
        if type(value) == int or type(value) == float:
            self.step_size = value
        else:
            raise ValueError('value must be a float or a int type')

    def get_step_size(self):
        """
        Get the
        :return:
        """
        return self.step_size

    def get_step_period_time(self):
        """
        Get the period time in second

        :return: Return a second divided by the number of Tick Per Second
        """
        return 1.0 / self.get_step_size()

    def get_time(self):
        """
        Return the time in seconds since the epoch as a floating point number.

        :return: time in seconds since the epoch
        :rtype: float
        """
        return time()

    def is_running(self):
        """
        Checks to see if the MainLoop is currently being run via run().

        :return: TRUE if the mainloop is currently being run.
        :rtype: Boolean
        """
        return self._is_running

    def run(self):
        """
        Runs a MainLoop until quit() is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.
        """
        self._set_is_running(True)
        logging.info('Starting ' + self.__class__.__name__)
        self._run()

    def quit(self, *args, **kw):
        """
        Stops a MainLoop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A MainLoop quit() call will certainly cause the end of you programme
        """
        self._set_is_running(False)
        # raise Exception("end of time")
        logging.info('Stopping ' + self.__class__.__name__)

    # Internal Method's
    def _set_is_running(self, boolean):
        """
        Set the is_running attribute

        :param boolean: 0 or True
        :type boolean: Boolean
        """
        self._is_running = bool(boolean)

    def _run(self):
        self.running = True

        while self.is_running:
            try:
                starting_time = self.get_time()
                # ... do stuff that might take significant time here

                # sleep the necessary time
                time_to_sleep = max(self.get_step_period_time() - (self.get_time() - starting_time), 0)
                print('{0}: calm down for {1} sec'.format(self.__class__.__name__, time_to_sleep))
                logging.info('{0}: calm down for {1} sec'.format(self.__class__.__name__, time_to_sleep))
                sleep(time_to_sleep)
            except KeyboardInterrupt:
                Signal("QUIT", KeyboardInterrupt, self.quit)
                break
        raise quit('All operation is stop')
