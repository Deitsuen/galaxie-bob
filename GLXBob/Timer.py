#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa at rtnp dot org> all rights reserved


# Reference Document: http://code.activestate.com/recipes/579053-high-precision-fps/
class Timer(object):
    """
    :Description:

    The :class:`Timer <GLXBob.Timer.Timer>` object contain a self-correcting timing algorithms.

    That self-correcting timing algorithms have associated attribute's it permit to control the
    :class:`Timer <GLXBob.Timer.Timer>` object.

    The power saving happen that because the loop try to use the minimum
    The :class:`Timer <GLXBob.Timer.Timer>` object update value itself and can be requested, via internal method's.
    """
    def __init__(self,
                 fps=10.0,
                 fps_max=60.0,
                 fps_min=1.0,
                 fps_increment=0.1,
                 fps_min_increment=0.1,
                 fps_max_increment=1.0
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

        :Attributes Details:

        .. py:attribute:: __fps

           The number of Frames per second. (in **fps**)

           Note that not correspond exactly to a true movies or game FPS, it's similar but it's not.

           For the :class:`Timer <GLXBob.Timer.Timer>` class, it correspond more about how many time **1 second**
           is divided.

           The ``value`` passed as argument to
           :func:`Timer.set_fps() <GLXBob.Timer.Timer.set_fps()>` method is clamped
           to lie between :py:attr:`__fps_min` and :py:attr:`__fps_max`
           attributes.

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 25.0                          |
              +---------------+-------------------------------+

        .. py:attribute:: __fps_min

           The min Frames number per second allowed before the :class:`Timer <GLXBob.Timer.Timer>` stop to apply
           a rate limit to the :py:attr:`__fps` attribute. (in **fps**)

           It can be considered as the min value of the CLAMP process

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 2.0                           |
              +---------------+-------------------------------+

        .. py:attribute:: __fps_max

           The maximum Frames number per second allowed before the :class:`Timer <GLXBob.Timer.Timer>` start to rate
           limit the :py:attr:`__fps` attribute.

           It can be considered as the max value of the CLAMP process

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 60.0                          |
              +---------------+-------------------------------+

        .. py:attribute:: __fps_increment

           The self-correcting timing algorithms will try to increase or decrease :py:attr:`__fps` attribute
           with the :py:attr:`__fps_increment` attribute value.

           Note: the ``__fps_increment`` parameter is not clamp

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:attribute:: __fps_min_increment

           :py:attr:`__fps_min_increment` is the lower allowed increment value

           The self-correcting timing will try to adjust :py:attr:`fps` attribute
           in range of :py:attr:`__fps_min_increment` to :py:attr:`__fps_max_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:attribute:: __fps_max_increment

           :py:attr:`__fps_max_increment` is the upper allowed increment value

           The self-correcting timing will try to adjust :py:attr:`fps` attribute
           in range of :py:attr:`__fps_min_increment` to :py:attr:`__fps_max_increment`

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
        self.__fps_memory = list()
        self.__frame = 0
        self.__frame_max = 8
        self.__time_departure = None

    def tick(self):
        """
        Emit True "when necessary" , that mean according with all the self-correcting timing algorithms and they
        configuration attribute's


        .. code-block:: python

           timer = Timer()
           while True:
               # Do stuff that might take significant time here

               if timer.tick():
                   print('Hello World!')

        :return: :py:obj:`True` when it's time or :py:obj:`False` if the job adjustment of fps should be done
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
        if self._get_frame() > self._get_frame_max():
            self._set_time_departure(self.get_time())
            self._set_frame(0)

            # Determine a increment multiplicator for have fast convergence
            ref = self._get_fps_memory()[len(self._get_fps_memory()) / 2]
            half = self._get_fps_memory()[:len(self._get_fps_memory()) / 2]
            rest = self._get_fps_memory()[len(self._get_fps_memory()) / 2:]
            half_sum = sum(half)
            rest_sum = sum(rest)

            if rest_sum > half_sum:
                print('DOWN')
            elif rest_sum == half_sum:
                print('STABILIZE')
            else:
                print('UP')

        # Monitor the frame rate
        self._push_fps_memory(self.get_fps())

        if differ <= 0:
            # raise ValueError('cannot maintain desired FPS rate')
            self.set_fps(self.get_fps() - self.get_fps_increment())
            return False
        else:
            self.set_fps(self.get_fps() + (self.get_fps_increment()))
            sleep(differ)
            return True

    def get_time(self):
        """
        Time should be take as a serious thing, you should try to impose only one time source in you program, then the
        :class:`Timer <GLXBob.Timer.Timer>` class provide it own method for get the time by it self.

        :return: Unix time
        :rtype: int
        """
        return time()

    def set_fps(self, fps=25.00):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps` attribute.

        :param fps: Frames number per second. (in **fps**)
        :type fps: float
        :raise TypeError: if ``fps`` parameter is not a :py:data:`float` type
        """
        if type(fps) == float:
            # CLAMP to the abosolut value
            clamped_value = abs(max(min(self.get_fps_max(), fps), self.get_fps_min()))
            # Round to two digit
            clamped_value = round(clamped_value, 2)

            if self.get_fps() != clamped_value:
                self.__fps = clamped_value
        else:
            raise TypeError(u'>fps< argument must be a float')

    def get_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps` attribute value.

        :return: :py:attr:`fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps

    def set_fps_min(self, min_fps=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps` attribute value.

        It correspond to a imposed minimal amount of frame rate

        :return: :py:attr:`min_fps` attribute value. (in **fps**)
        :rtype: float
        :raise TypeError: if ``min_fps`` parameter is not a :py:data:`float` type
        """
        if type(min_fps) == float:
            if self.get_fps_min() != min_fps:
                self.__fps_min = min_fps
        else:
            raise TypeError(u'>min_fps< argument must be a float')

    def get_fps_min(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_min` attribute value.

        :return: :py:attr:`min_fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps_min

    def set_fps_max(self, max_fps=60.0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps` attribute value.

        It correspond to a imposed minimal amount of frame rate

        :return: :py:attr:`max_fps` attribute value. (in **fps**)
        :rtype: float
        :raise TypeError: if ``max_fps`` parameter is not a :py:data:`float` type
        """
        if type(max_fps) == float:
            if self.get_fps_max() != max_fps:
                self.__fps_max = max_fps
        else:
            raise TypeError(u'>max_fps< argument must be a float')

    def get_fps_max(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps` attribute value.

        :return: :py:attr:`max_fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps_max

    def set_fps_increment(self, fps_increment=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps_increment` attribute
        with it step increment.

        :param fps_increment: Frames number per second. (in **fps**)
        :type fps_increment: float
        :raise TypeError: if ``fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_increment) == float:
            if self.get_fps_increment() != fps_increment:
                self.__fps_increment = fps_increment
        else:
            raise TypeError(u'>fps< argument must be a float')

    def get_fps_increment(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_increment` attribute value.

        :return: :py:attr:`fps_increment` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps_increment

    def set_fps_min_increment(self, fps_min_increment=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps` attribute with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <GLXBob.Timer.Timer>` can use :py:attr:`min_fps_increment`
        and :py:attr:`max_fps_increment` can make gap in a increment range, where :py:attr:`min_fps_increment` will
        force a minimal amount of increment.

        :param fps_min_increment: Frames number per second. (in **fps**)
        :type fps_min_increment: float
        :raise TypeError: if ``min_fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_min_increment) == float:
            if self.get_fps_min_increment() != fps_min_increment:
                self.__fps_min_increment = fps_min_increment
        else:
            raise TypeError(u'>min_fps_increment< argument must be a float')

    def get_fps_min_increment(self):
        """
        Get the smaller of step increment

        The :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps_increment` attribute value.

        See :func:`Timer.set_min_fps_increment() <GLXBob.Timer.Timer.set_min_fps_increment()>` for more information's

        :return: :py:attr:`min_fps_increment` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps_min_increment

    def set_fps_max_increment(self, fps_max_increment=1.0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps` attribute with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <GLXBob.Timer.Timer>` can use :py:attr:`min_fps_increment`
        and :py:attr:`max_fps_increment` for make gap in a increment range, where :py:attr:`max_fps_increment` will
        fixe the limit .

        :param fps_max_increment: Frames number per second. (in **fps**)
        :type fps_max_increment: float
        :raise TypeError: if ``max_fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_max_increment) == float:
            if self.get_fps_max_increment() != fps_max_increment:
                self.__fps_max_increment = fps_max_increment
        else:
            raise TypeError(u'>max_fps_increment< argument must be a float')

    def get_fps_max_increment(self):
        """
        Get the bigger of step increment

        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps_increment` attribute value.

        :return: :py:attr:`max_fps_increment` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps_max_increment

    ###
    # Internal method's
    def _set_time_departure(self, time_value):
        """
        Store a :func:`Timer.get_time() <GLXBob.Timer.Timer.get_time()>` return value inside
        :py:attr:`__departure_time` attribute.

        :param time_value: return value inside :py:attr:`__departure_time` attribute.
        :type time_value: a :func:`Timer.get_time() <GLXBob.Timer.Timer.get_time()>` return
        """
        if self._get_time_departure() != time_value:
            self.__time_departure = time_value

    def _get_time_departure(self):
        """
        Return the value set by a :func:`Timer._set_departure_time() <GLXBob.Timer.Timer._set_departure_time()>`

        :return: return :py:attr:`__departure_time` attribute.
        :rtype: :func:`time.time() <time.time()>`
        """
        return self.__time_departure

    def _set_fps_memory(self, fps_memory=None):
        """
        Store a :py:obj:`list` inside :py:attr:`__fps_memory` attribute

        :param fps_memory: :py:obj:`list` or :py:obj:`None` if want to reset the list
        :type fps_memory: :py:obj:`list` or :py:obj:`None`
        """
        if type(fps_memory) == list or fps_memory is None:
            if fps_memory is None:
                fps_memory = [25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0]
            if self._get_fps_memory() != fps_memory:
                self.__fps_memory = fps_memory
        else:
            raise TypeError(u'>fps_memory< argument must be a list or None')

    def _get_fps_memory(self):
        """
        Get the :py:attr:`__fps_memory` attribute value

        :return: :py:attr:`__fps_memory` attribute value
        :rtype: list
        """
        return self.__fps_memory

    def _push_fps_memory(self, value):
        if len(self._get_fps_memory()) > 0:
            self._get_fps_memory().insert(0, value)
            if len(self._get_fps_memory()) > self._get_frame_max():
                del self._get_fps_memory()[-1]
        else:
            self._get_fps_memory().insert(0, value)

    def _set_frame(self, frame=0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame` attribute.

        It will be use a maximum size of a list it contain :py:attr:`fps` attribute memory

        It must start to int(0), and will be increase by the :class:`Timer <GLXBob.Timer.Timer>`

        :param frame: correspond to the cursor inside memory fps list
        :type frame: int
        :raise TypeError: if ``frame`` parameter is not a :py:data:`int` type
        """
        if type(frame) == int:
            if self._get_frame() != frame:
                self.__frame = frame
        else:
            raise TypeError(u'>frame< argument must be a int')

    def _get_frame(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame` attribute.

        You can set :py:attr:`__frame` attribute with
        :func:`Timer._set_frame() <GLXBob.Timer.Timer._set_frame()>` method.

        :return: ``__frame`` attribute value
        :rtype: int
        """
        return self.__frame

    def _set_frame_max(self, frame_max=8):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame_max` attribute.

        It will be use a maximum size of a list it contain :py:attr:`fps` attribute memory

        :param frame_max: correspond to the buffer size
        :type frame_max: int
        :raise TypeError: if ``max_frame`` parameter is not a :py:data:`int` type
        """
        if type(frame_max) == int:
            if self._get_frame_max() != frame_max:
                self.__frame_max = frame_max
        else:
            raise TypeError(u'>frame_max< argument must be a int')

    def _get_frame_max(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame_max` attribute.

        You can set :py:attr:`__frame_max` attribute with
        :func:`Timer._set_frame_max() <GLXBob.Timer.Timer._set_frame_max()>` method.

        :return: ``__frame_max`` attribute value
        :rtype: int
        """
        return self.__frame_max

