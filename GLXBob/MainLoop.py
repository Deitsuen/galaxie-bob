#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa@rtnp.org> all rights reserved


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

    def run(self):
        """
        Runs a MainLoop until quit() is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.
        """
        self._set_is_running(True)
        logging.info('Starting ' + self.__class__.__name__)
        self._run()

    # Internal Method's
    def _set_is_running(self, boolean):
        """
        Set the is_running attribute

        :param boolean: 0 or True
        :type boolean: Boolean
        """
        self._is_running = bool(boolean)

    def _run(self):
        pass
