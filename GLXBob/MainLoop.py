#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from time import sleep
from random import randint
from GLXBob import Timer

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
    :Description:

    The :class:`MainLoop <GLXBob.MainLoop.MainLoop>` object is a Alderson loop , it's something close to a
    infinity loop but with a :func:`MainLoop.run() <GLXBob.MainLoop.MainLoop.run()>` and
     and :func:`MainLoop.quit() <GLXBob.MainLoop.MainLoop.quit()>` method's.

    The :class:`MainLoop <GLXBob.MainLoop.MainLoop>` make it work and take a adaptive sleep for impose a
    global Frame Rate. Default: 25

    That loop , should be a low power consumption, that was our target for the beginning.

    Feature:
       * Alderson loop with run() and quit() method
       * Don't use 100% of CPU Time
       * Frame Per Second adaptive limitation

    To Do:
       * The **Event list** size should control interact with Frame Rate Limitation
       * Limitation will be apply with a knee (percentage) it depende of the **Event list** size
    """
    # http://code.activestate.com/recipes/579053-high-precision-fps/
    __metaclass__ = Singleton

    def __init__(self):
        """
        :Attributes Details:


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
        timer = Timer(fps=30.0, max_fps=60.0)
        while self.is_running:
            try:
                # Must be the first line
                starting_time = timer.get_time()

                # Do stuff that might take significant time here

                slepp_for = 1.0 / randint(20, 75)
                sleep(slepp_for)

                # Timer control
                if timer.tick():
                    take_time = timer.get_time() - starting_time
                    print('{1} fps, iteration take {0} sec'.format(take_time, timer.get_fps()))

            except KeyboardInterrupt:
                Signal("QUIT", KeyboardInterrupt, self.quit)
                break
            except MemoryError:
                break
        raise quit('All operation is stop')
