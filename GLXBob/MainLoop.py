#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from GLXBob import Timer
from random import randint
from time import sleep
import sys

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Tuux <tuxa at rtnp dot org> all rights reserved


class Signal(Exception):
    """
    Generic Signal exception for Galaxie-BoB

    The tips consist to use the Exception module as class parent
    """
    def __init__(self, msg, original_exception, callback=None):
        super(Signal, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception

        # Quit Message
        if msg == 'QUIT':
            try:
                sys.stdout.write('\n')
                sys.stdout.write('Exception: ' + str(self.original_exception) + '\n')
                sys.stdout.flush()
            except IOError:
                pass

            if callback is None:
                return
            else:
                callback()
        elif msg == 'KEY':
            sys.stdout.write('\n')
            sys.stdout.write('Exception: ' + str(self.original_exception) + '\n')
            sys.stdout.flush()
        elif msg == 'EVENT':
            sys.stdout.write('\n')
            sys.stdout.write('Exception: ' + str(self.original_exception) + '\n')
            sys.stdout.flush()
        elif msg == 'TIMER':
            sys.stdout.write('\n')
            sys.stdout.write('Exception: ' + str(self.original_exception) + '\n')
            sys.stdout.flush()


class Singleton(type):
    def __init__(cls, name, bases, dictionary):
        super(Singleton, cls).__init__(name, bases, dictionary)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args)
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
       * Limitation will be apply with a knee (percentage) it depend of the **Event list** size

    To Do:
       * The **Event list** size should control interact with Frame Rate Limitation
    """
    # http://code.activestate.com/recipes/579053-high-precision-fps/
    __metaclass__ = Singleton

    def __init__(self):
        """
        :Attributes Details:

        .. py:attribute:: __is_running

            It is running or not

              +---------------+-------------------------------+
              | Type          | :py:data:`bool`               |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | False                         |
              +---------------+-------------------------------+

        """
        self.__is_running = False
        self.__timer = Timer()

    def is_running(self):
        """
        Checks to see if the :class:`MainLoop <GLXBob.MainLoop.MainLoop>` is currently being run via run().

        :return: TRUE if the mainloop is currently being run.
        :rtype: bool
        """
        return self.__is_running

    def run(self):
        """
        Runs a MainLoop until quit() is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.
        """
        self._set_is_running(True)
        logging.info(self.__class__.__name__ + ': Starting ...')
        self._run()

    def quit(self):
        """
        Stops a MainLoop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A MainLoop quit() call will certainly cause the end of you programme
        """
        self._set_is_running(False)
        # raise Exception("end of time")
        logging.info(self.__class__.__name__ + ': Stopping ...')

    def set_timer(self, timer=None):
        """
        Set the __timer attribute, buy default the class initialization create automatically a Timer() object and
        store it in the __timer attribute. You can set you own Timer object with it method.

        :param timer: a GLXBob.Timer() object initialize by you self or None for a default GLXBob.Timer()
        :type timer: GLXBob.Timer()
        """
        if timer is None:
            timer = Timer()
        self.__timer = timer

    def get_timer(self):
        """
        Return the __timer attribute value

        :return: a GLXBob.Timer() Class object
        :rtype: GLXBob.Timer()
        """
        return self.__timer

    # Internal Method's

    def _set_is_running(self, boolean):
        """
        Set the __is_running attribute

        :param boolean: True or False
        :type boolean: bool
        :raise TypeError: if ``boolean`` parameter is not a :py:data:`bool` type
        """
        if type(boolean) == bool:
            if self._get_is_running() != boolean:
                self.__is_running = boolean
        else:
            raise TypeError(u'>boolean< parameter must be a bool type')

    def _get_is_running(self):
        """
        Get the __is_running attribute value

        :return: True if the MainLoop is running or False if not
        :rtype: bool
        """
        return self.__is_running

    def _run(self):
        while self.is_running():
            try:
                # Must be the first line
                starting_time = self.get_timer().get_time()

                # Do stuff that might take significant time here

                # sleep_for = 1.0 / randint(1, randint(2, 500))
                # sleep_for = 1.0 / randint(40, randint(41, 500))
                # sleep_for = 1.0 / randint(20, 75)
                # sleep_for = 1.0 / randint(50, 200)
                # sleep(sleep_for)

                # Timer control
                if self.get_timer().tick():

                    print('[ OK ]-> {1} fps, iteration take {0} sec'.format(
                        self.get_timer().get_time() - starting_time,
                        self.get_timer().get_fps()
                        ))
                else:

                    print('[    ]-> {1} fps, iteration take {0} sec'.format(
                        self.get_timer().get_time() - starting_time,
                        self.get_timer().get_fps()
                        ))

            except KeyboardInterrupt:
                Signal("QUIT", KeyboardInterrupt, self.quit)
                break
            except MemoryError:
                self._set_is_running(False)
                logging.info(self.__class__.__name__ + ': MemoryError Stopping ...')
                break
        logging.info('All operation is stop')
        raise quit('All operation is stop')
