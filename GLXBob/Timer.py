#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep


class Timer:
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
                 max_fps=60.0,
                 min_fps=1.0,
                 fps_increment=0.1,
                 min_fps_increment=0.1,
                 max_fps_increment=1.0
                 ):
        """
        :Attributes Details:

        .. py:attribute:: fps

           The Frames number per second. (in **fps**)

           Note that not correspond to the true movies or game FPS, it's apparented but it's not.
           Fo the the :class:`Timer <GLXBob.Timer.Timer>` class, that correspond to how many time **1sec** is divided.

           The ``value`` passed as argument is clamped to lie between :py:attr:`min_fps` and :py:attr:`max_fps`
           attributes.

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 25.0                          |
              +---------------+-------------------------------+

        .. py:attribute:: min_fps

           The min Frames number per second allowed before the :class:`Timer <GLXBob.Timer.Timer>` stop to apply
           a rate limit to the :py:attr:`fps` attribute. (in **fps**)

           It can be considered as the min value of the CLAMP process

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 2.0                           |
              +---------------+-------------------------------+

        .. py:attribute:: max_fps

           The maximum Frames number per second allowed before the :class:`Timer <GLXBob.Timer.Timer>` start to rate
           limit the :py:attr:`fps` attribute.

           It can be considered as the max value of the CLAMP process

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 60.0                          |
              +---------------+-------------------------------+

        .. py:attribute:: fps_increment

           The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps` attribute
           with the :py:attr:`fps_increment` attribute value.

           Note: the ``fps_increment`` parameter is not clamp

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        :param fps: how many time 1 second is divided
        :param max_fps: maximum fps allowed before apply a hard limit rate
        :param min_fps: minimum fps where the power saving should stop to decrease fps
        :param fps_increment:
        :param min_fps_increment:
        :param max_fps_increment:
        """
        self.__fps = fps
        self.__min_fps = min_fps
        self.__max_fps = max_fps
        self.__fps_increment = fps_increment
        self.__max_fps_increment = max_fps_increment
        self.__min_fps_increment = min_fps_increment
        self.__frame = 0
        self.__departure_time = None

    def tick(self):
        """
        Emit True "when necessary" , that mean according with all the self-correcting timing algorithms and they
        configuration attribute's

        :return: True if
        """
        if self.__get_departure_time() is None:
            self.__set_departure_time(self.get_time())

        self.__frame += 1

        try:
            target = self.__frame / self.get_fps()
        except ZeroDivisionError:
            target = self.__frame

        passed = self.get_time() - self.__get_departure_time()
        differ = target - passed

        # Reset time reference due to time variation
        if self.__frame == 8:
            self.__set_departure_time(self.get_time())
            self.__frame = 0

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

    def set_fps(self, fps):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps` attribute.

        :param fps: Frames number per second. (in **fps**)
        :type fps: float
        :raise TypeError: if ``fps`` parameter is not a :py:data:`float` type
        """
        if type(fps) == float:
            # CLAMP to the abosolut value
            self.__fps = abs(max(min(self.get_max_fps(), fps), self.get_min_fps()))
        else:
            raise TypeError(u'>fps< argument must be a float')

    def get_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps` attribute value.

        :return: :py:attr:`fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps

    def get_min_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps` attribute value.

        :return: :py:attr:`min_fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__min_fps

    def get_max_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps` attribute value.

        :return: :py:attr:`max_fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__max_fps

    def set_fps_increment(self, fps_increment):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps_increment` attribute
        with it step increment.

        :param fps_increment: Frames number per second. (in **fps**)
        :type fps_increment: float
        :raise TypeError: if ``fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(fps_increment) == float:
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

    def set_min_fps_increment(self, min_fps_increment):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps` attribute with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <GLXBob.Timer.Timer>` can use :py:attr:`min_fps_increment`
        and :py:attr:`max_fps_increment` can make gap in a increment range, where :py:attr:`min_fps_increment` will
        force a minimal amount of increment.

        :param min_fps_increment: Frames number per second. (in **fps**)
        :type min_fps_increment: float
        :raise TypeError: if ``min_fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(min_fps_increment) == float:
            self.__fps_increment = min_fps_increment
        else:
            raise TypeError(u'>min_fps_increment< argument must be a float')

    def get_min_fps_increment(self):
        """
        Get the smaller of step increment

        The :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps_increment` attribute value.

        :return: :py:attr:`min_fps_increment` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__min_fps_increment

    def get_max_fps_increment(self):
        """
        Get the bigger of step increment

        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps_increment` attribute value.

        :return: :py:attr:`max_fps_increment` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__max_fps_increment

    ###
    # Internal method's
    def __set_departure_time(self, time_value):
        self.__departure_time = time_value

    def __get_departure_time(self):
        return self.__departure_time


