#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep
import logging

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Tuux <tuxa at rtnp dot org> all rights reserved


# Reference Document: http://code.activestate.com/recipes/579053-high-precision-fps/
class Timer(object):
    """
    :Description:

    The :class:`Timer <GLXBob.Timer.Timer>` object contain a self-correcting timing algorithms.

    That self-correcting timing algorithms have associated property's it permit to control the
    :class:`Timer <GLXBob.Timer.Timer>` object.

    The power saving happen that because the loop try to use the minimum
    The :class:`Timer <GLXBob.Timer.Timer>` object update value itself and can be requested, via internal method's.
    """
    def __init__(self,
                 fps=60.0,
                 fps_max=float("inf"),
                 fps_min=1.0,
                 fps_increment=0.1,
                 fps_min_increment=0.1,
                 fps_max_increment=10.0
                 ):
        """
        :param fps: how many time 1 second is divided
        :param fps_max: maximum fps allowed before apply a hard limit rate
        :param fps_min: minimum fps where the power saving should stop to decrease fps
        :param fps_increment:
        :param fps_min_increment: the lower allowed increment value
        :param fps_max_increment: the upper allowed increment value
        :type fps: float
        :type fps_max: float
        :type fps_min: float
        :type fps_increment: float
        :type fps_min_increment: float
        :type fps_max_increment: float

        :Property's Details:

        .. py:data:: fps

           The number of Frames per second. (in **fps**)

           Note that not correspond exactly to a true movies or game FPS, it's similar but it's not.

           For the :class:`Timer <GLXBob.Timer.Timer>` Class, it correspond more about how many time **1 second**
           is divided.

           The ``value`` passed as argument to
           :func:`Timer.set_fps() <GLXBob.Timer.Timer.set_fps()>` method is clamped
           to lie between :py:data:`fps_min` and :py:data:`fps_max`
           property's.

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 25.0                          |
              +---------------+-------------------------------+

        .. py:data:: fps_min

           The min Frames number per second allowed before the :class:`Timer <GLXBob.Timer.Timer>` stop to apply
           a rate limit to the :py:data:`fps` property. (in **fps**)

           It can be considered as the min value of the CLAMP process

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 2.0                           |
              +---------------+-------------------------------+

        .. py:data:: fps_max

           The maximum Frames number per second allowed before the :class:`Timer <GLXBob.Timer.Timer>` start to rate
           limit the :py:data:`fps` property.

           It can be considered as the max value of the CLAMP process.

           By default it have no limit fps_max = float("inf")

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | float("inf")                  |
              +---------------+-------------------------------+

        .. py:data:: fps_increment

           The self-correcting timing algorithms will try to increase or decrease :py:data:`fps` property
           with the :py:data:`fps_increment` property value.

           Note: the :py:data:`fps_increment` property will be not clamped

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:data:: fps_min_increment

           :py:data:`fps_min_increment` is the lower allowed increment value

           The self-correcting timing will try to adjust :py:data:`fps` property
           in range of :py:data:`fps_min_increment` to :py:data:`fps_max_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:data:: fps_max_increment

           :py:data:`fps_max_increment` is the upper allowed increment value

           The self-correcting timing will try to adjust :py:data:`fps` property
           in range of :py:data:`fps_min_increment` to :py:data:`fps_max_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        """
        self.__fps = fps
        self.__fps_increment = fps_increment
        self.__fps_min = fps_min
        self.__fps_min_increment = fps_min_increment
        self.__fps_max = fps_max
        self.__fps_max_increment = fps_max_increment

        # Internal
        self.__fps_memory = None
        self.__frame = 0
        self.__frame_max = 8
        self.__time_departure = None
        self.__be_fast = False
        self.__be_fast_multiplicator = 10

    def tick(self):
        """
        Return :py:obj:`True` or :py:obj:`False` "when necessary" , that mean according with all the self-correcting
        timing algorithms and they configuration property's


        .. code-block:: python

           timer = Timer()
           while True:
               # Do stuff that might take significant time here

               if timer.tick():
                   print('Hello World!')

        :return: :py:obj:`True` when it's time or :py:obj:`False` if a adjustment job of :py:data:`fps` property
                 should be done
        :rtype: bool
        """
        if self._get_time_departure() is None:
            self._set_time_departure(self.get_time())

        # Increase Frame
        self._set_frame(self._get_frame() + 1)

        # The algho
        try:
            target = self._get_frame() / self.get_fps()
        except ZeroDivisionError:
            target = self._get_frame()

        passed = self.get_time() - self._get_time_departure()
        differ = target - passed

        # Reset time reference due to time variation
        # Should never be remove or for a true system if compensate time variation
        if self._get_frame() > self._get_frame_max():
            self._set_time_departure(self.get_time())
            self._set_frame(0)

            # Determine a increment factor for fast convergence
            half_sum = sum(self._get_fps_memory()[:len(self._get_fps_memory()) / 2])
            rest_sum = sum(self._get_fps_memory()[len(self._get_fps_memory()) / 2:])

            # It's time to analyze the result
            if int(half_sum) == int(rest_sum):
                self._set_be_fast_multiplicator(0)
                self._set_be_fast(False)
                logging.info("{0}:[GOAL]-> Increment {1} fps, {2} fps".format(
                    self.__class__.__name__,
                    self.get_fps_increment(),
                    self.get_fps()
                ))
                print("[GOAL]-> Increment {0} fps, {1} fps".format(
                    self.get_fps_increment(),
                    self.get_fps()
                ))
            else:
                if half_sum < rest_sum:
                    if self._get_be_fast():
                        self._set_be_fast_multiplicator(self._get_be_fast_multiplicator() - 10)
                        print("[DOWN]-> Increment {0} fps, {1} fps".format(
                            self._get_fps_accelerated(),
                            self.get_fps()
                        ))
                    else:
                        self._set_be_fast_multiplicator(10)
                        print("[DOWN]-> Increment {0} fps, {1} fps".format(
                            self.get_fps_increment(),
                            self.get_fps()
                        ))
                    self._set_be_fast(False)

                elif half_sum > rest_sum:
                    if self._get_be_fast():
                        self._set_be_fast_multiplicator(self._get_be_fast_multiplicator() + 10)
                        print("[ UP ]-> Increment {0} fps, {1} fps".format(
                            self._get_fps_accelerated(),
                            self.get_fps()
                        ))
                    else:
                        self._set_be_fast_multiplicator(10)
                        print("[ UP ]-> Increment {0} fps, {1} fps".format(
                            self.get_fps_increment(),
                            self.get_fps()
                        ))
                    self._set_be_fast(True)

        # Monitor the frame rate
        self._push_fps_memory(self.get_fps())

        # Now we know how many time differ from the ideal Frame Rate
        if differ <= 0:
            # raise ValueError('cannot maintain desired FPS rate')
            if self._get_be_fast():
                self.set_fps(self.get_fps() - (self.get_fps_max_increment() * self._get_be_fast_multiplicator() / 100))
            else:
                self.set_fps(self.get_fps() - self.get_fps_increment())
            # Return False that because we haven't respect the ideal frame rate
            return False
        else:
            if self._get_be_fast():
                self.set_fps(self.get_fps() + (self.get_fps_max_increment() * self._get_be_fast_multiplicator() / 100))
            else:
                self.set_fps(self.get_fps() + self.get_fps_increment())

            # Everything is fine , we have spare time then we can sleep for the rest of the frame time
            sleep(differ)
            # Return True that because we have respect the ideal frame rate
            return True

    def _get_fps_accelerated(self):
        return (self.get_fps_max_increment() * self._get_be_fast_multiplicator()) / 100

    @staticmethod
    def get_time():
        """
        Time should be take as a serious thing, you should try to impose only one time source in you program, then the
        :class:`Timer <GLXBob.Timer.Timer>` Class provide it own method for get the time by it self.

        :return: Unix time
        :rtype: int
        """
        return time()

    def set_fps(self, fps=25.00):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps` property.

        :param fps: Frames number per second. (in **fps**)
        :type fps: float
        :raise TypeError: if ``fps`` parameter is not a :py:data:`float` type
        """
        if type(fps) == float:
            # CLAMP to the absolute value
            if self.get_fps_max():
                clamped_value = abs(max(min(self.get_fps_max(), fps), self.get_fps_min()))
            else:
                if self.get_fps_min() > fps:
                    clamped_value = abs(fps)
                else:
                    clamped_value = self.get_fps_min()

            # Round to two digit
            clamped_value = round(clamped_value, 2)

            if self.get_fps() != clamped_value:
                self.__fps = clamped_value
        else:
            raise TypeError(u'>fps< parameter must be a float')

    def get_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps` property value.

        :return: :py:data:`fps` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps

    def set_fps_min(self, fps_min=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_min` property value.

        It correspond to a imposed minimal amount of frame rate

        :return: :py:data:`fps_min` property value. (in **fps**)
        :rtype: float
        :raise TypeError: if ``fps_min`` parameter is not a :py:data:`float` type
        """
        if type(fps_min) == float:
            if self.get_fps_min() != fps_min:
                self.__fps_min = fps_min
        else:
            raise TypeError(u'min_fps parameter must be a float')

    def get_fps_min(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_min` property value.

        :return: :py:data:`fps_min` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_min

    def set_fps_max(self, max_fps=None):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_max` property value.

        It correspond to a imposed max amount of frame rate used during acceleration phase

        :param max_fps: :py:attr:`fps_max` property value. (in **fps**)
        :type max_fps: :py:obj:`float` or :py:obj:`None`
        :raise TypeError: if ``max_fps`` parameter is not a :py:data:`float` type
        """
        if max_fps is None:
            max_fps = float("inf")
        if type(max_fps) == float:
            if self.get_fps_max() != max_fps:
                self.__fps_max = max_fps
        else:
            raise TypeError(u'>max_fps< parameter must be a float')

    def get_fps_max(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_max` property value.

        :return: :py:attr:`fps_max` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_max

    def set_fps_increment(self, fps_increment=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_increment` property.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps_increment` property
        with it step increment.

        :param fps_increment: Frames number per second. (in **fps**)
        :type fps_increment: float
        :raise TypeError: if ``fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_increment) == float:
            if self.get_fps_increment() != fps_increment:
                self.__fps_increment = fps_increment
        else:
            raise TypeError(u'>fps< parameter must be a float')

    def get_fps_increment(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_increment` property value.

        :return: :py:data:`fps_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_increment

    def set_fps_min_increment(self, fps_min_increment=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_min_increment` increment.

        The algorithms will try to increase or decrease :py:data:`fps` property with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <GLXBob.Timer.Timer>` can use :py:data:`fps_min_increment`
        and :py:data:`fps_max_increment` property for make a gap in contain in a range, where
        :py:data:`fps_min_increment` will force a minimal amount of increment and
        :py:data:`fps_max_increment` will force a maximal amount of increment.

        :param fps_min_increment: Frames number per second. (in **fps**)
        :type fps_min_increment: float
        :raise TypeError: if ``fps_min_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_min_increment) == float:
            if self.get_fps_min_increment() != fps_min_increment:
                self.__fps_min_increment = fps_min_increment
        else:
            raise TypeError(u'fps_min_increment parameter must be a float type')

    def get_fps_min_increment(self):
        """
        Get the smaller of step increment

        The :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_min_increment` property value.

        See :func:`Timer.set_fps_min_increment() <GLXBob.Timer.Timer.set_fps_min_increment()>` for more information's

        :return: :py:data:`fps_min_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_min_increment

    def set_fps_max_increment(self, fps_max_increment=1.0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_max_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:data:`fps` property with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <GLXBob.Timer.Timer>` can use :py:data:`fps_min_increment`
        and :py:data:`fps_max_increment` for make gap in a increment range, where :py:data:`fps_max_increment` will
        fixe the limit .

        :param fps_max_increment: Frames number per second. (in **fps**)
        :type fps_max_increment: float
        :raise TypeError: if ``fps_max_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_max_increment) == float:
            if self.get_fps_max_increment() != fps_max_increment:
                self.__fps_max_increment = fps_max_increment
        else:
            raise TypeError(u'>max_fps_increment< parameter must be a float')

    def get_fps_max_increment(self):
        """
        Get the bigger of step increment

        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:data:`fps_max_increment` property value.

        :return: :py:data:`fps_max_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_max_increment

    ###
    # Internal method's
    def _set_time_departure(self, time_value):
        """
        Store a :func:`Timer.get_time() <GLXBob.Timer.Timer.get_time()>` return value inside
        :py:data:`departure_time` property.

        :param time_value: return value inside :py:data:`departure_time` property.
        :type time_value: a :func:`Timer.get_time() <GLXBob.Timer.Timer.get_time()>` return
        """
        if self._get_time_departure() != time_value:
            self.__time_departure = time_value

    def _get_time_departure(self):
        """
        Return the value set by a :func:`Timer._set_departure_time() <GLXBob.Timer.Timer._set_departure_time()>`

        :return: return :py:data:`departure_time` property.
        :rtype: Unix time
        """
        return self.__time_departure

    def _set_fps_memory(self, fps_memory=None):
        """
        Store a :py:obj:`list` inside :py:data:`fps_memory` property

        :param fps_memory: :py:obj:`list` or :py:obj:`None` if want to reset the list
        :type fps_memory: :py:obj:`list` or :py:obj:`None`
        :raise TypeError: if ``fps_memory`` parameter is not a :py:data:`list` or :py:obj:`None` type
        """
        if type(fps_memory) == list or fps_memory is None:
            if fps_memory is None:
                fps_memory = list()
            if self._get_fps_memory() != fps_memory:
                self.__fps_memory = fps_memory
        else:
            raise TypeError(u'>fps_memory< parameter must be a list or None')

    def _get_fps_memory(self):
        """
        Get the :py:data:`fps_memory` property value

        :return: :py:data:`fps_memory` property value
        :rtype: list
        """
        return self.__fps_memory

    def _push_fps_memory(self, value):
        # check if the list is None
        if self._get_fps_memory() is None:
            self._set_fps_memory(None)
        if len(self._get_fps_memory()) > 0:
            self._get_fps_memory().insert(0, value)
            if len(self._get_fps_memory()) > self._get_frame_max():
                del self._get_fps_memory()[-1]
        else:
            self._get_fps_memory().insert(0, value)

    def _set_frame(self, frame=0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame` property.

        It will be use a maximum size of a list it contain :py:data:`fps` property memory

        It must start to int(0), and will be increase by the :class:`Timer <GLXBob.Timer.Timer>`

        :param frame: correspond to the cursor inside memory fps list
        :type frame: int
        :raise TypeError: if ``frame`` parameter is not a :py:data:`int` type
        """
        if type(frame) == int:
            if self._get_frame() != frame:
                self.__frame = frame
        else:
            raise TypeError(u'>frame< parameter must be a int')

    def _get_frame(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame` property.

        You can set :py:attr:`__frame` property with
        :func:`Timer._set_frame() <GLXBob.Timer.Timer._set_frame()>` method.

        :return: ``__frame`` property value
        :rtype: int
        """
        return self.__frame

    def _set_frame_max(self, frame_max=8):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame_max` property.

        It will be use a maximum size of a list it contain :py:data:`fps` property memory

        :param frame_max: correspond to the buffer size
        :type frame_max: int
        :raise TypeError: if ``max_frame`` parameter is not a :py:data:`int` type
        """
        if type(frame_max) == int:
            if self._get_frame_max() != frame_max:
                self.__frame_max = frame_max
        else:
            raise TypeError(u'>frame_max< parameter must be a int')

    def _get_frame_max(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame_max` property.

        You can set :py:attr:`__frame_max` property with
        :func:`Timer._set_frame_max() <GLXBob.Timer.Timer._set_frame_max()>` method.

        :return: ``__frame_max`` property value
        :rtype: int
        """
        return self.__frame_max

    def _set_be_fast(self, be_fast):
        """
        Set the __be_fast property after have check if teh value is different and if type is a bollean value like:
        True, False, O, 1

        That value will be use for fast convergence, when the Timer seach for the best Frame rate

        :param be_fast:
        :type be_fast: bool
        :raise TypeError: if ``be_fast`` parameter is not a :py:data:`bool` type
        """
        if type(be_fast) == bool:
            if self._get_be_fast() is not be_fast:
                self.__be_fast = be_fast
        else:
            raise TypeError(u'>be_fast< parameter must be a bool')

    def _get_be_fast(self):
        """
        Return the value set by :func:`Timer._set_be_fast() <GLXBob.Timer.Timer._set_be_fast()>` method.

        You can set :py:attr:`__be_fast` property with

        :func:`Timer._set_be_fast() <GLXBob.Timer.Timer._set_be_fast()>` method.
        :return: :py:attr:`__be_fast` property
        :rtype: bool
        """
        return self.__be_fast

    def _set_be_fast_multiplicator(self, be_fast_multiplicator):
        """
        Set the :py:attr:`__be_fast_multiplicator` property

        That value will be use for fast convergence, when the Timer seach for the best Frame rate

        :param be_fast_multiplicator:
        :type be_fast_multiplicator: int
        :raise TypeError: if ``be_fast_multiplicator`` parameter is not a :py:data:`int` type
        """
        if type(be_fast_multiplicator) == int:
            if self._get_be_fast_multiplicator() != be_fast_multiplicator:
                self.__be_fast_multiplicator = be_fast_multiplicator
        else:
            raise TypeError(u'>be_fast< parameter must be a bool')

    def _get_be_fast_multiplicator(self):
        """
        Return the value set by
        :func:`Timer._set_be_fast_multiplicator() <GLXBob.Timer.Timer._set_be_fast_multiplicator()>` method.

        :return: :py:attr:`__be_fast_multiplicator` property
        :rtype: int
        """
        return self.__be_fast_multiplicator
