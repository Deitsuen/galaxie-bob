#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep
import unittest
from random import randint, sample
import sys

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Jérôme ORNECH alias "Tuux" <tuxa at rtnp dot org> all rights reserved

# Reference Document: http://code.activestate.com/recipes/579053-high-precision-fps/
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
        :param fps: how many time 1 second is divided
        :param max_fps: maximum fps allowed before apply a hard limit rate
        :param min_fps: minimum fps where the power saving should stop to decrease fps
        :param fps_increment:
        :param min_fps_increment: the lower allowed increment value
        :param max_fps_increment: the upper allowed increment value
        :type fps: float
        :type max_fps: float
        :type min_fps: float
        :type fps_increment: float
        :type min_fps_increment: float
        :type max_fps_increment: float

        :Attributes Details:

        .. py:attribute:: fps

           The number of Frames per second. (in **fps**)

           Note that not correspond exactly to a true movies or game FPS, it's similar but it's not.

           For the :class:`Timer <GLXBob.Timer.Timer>` class, it correspond more about how many time **1 second**
           is divided.

           The ``value`` passed as argument to
           :func:`Timer.set_fps() <GLXBob.Timer.Timer.set_fps()>` method is clamped
           to lie between :py:attr:`min_fps` and :py:attr:`max_fps`
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

        .. py:attribute:: min_fps_increment

           :py:attr:`min_fps_increment` is the lower allowed increment value

           The self-correcting timing will try to adjust :py:attr:`fps` attribute
           in range of :py:attr:`min_fps_increment` to :py:attr:`max_fps_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        .. py:attribute:: max_fps_increment

           :py:attr:`max_fps_increment` is the upper allowed increment value

           The self-correcting timing will try to adjust :py:attr:`fps` attribute
           in range of :py:attr:`min_fps_increment` to :py:attr:`max_fps_increment`

              +---------------+-------------------------------+
              | Type          | :py:data:`float`              |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0.1                           |
              +---------------+-------------------------------+

        """
        self.__fps = fps
        self.__min_fps = min_fps
        self.__max_fps = max_fps
        self.__fps_increment = fps_increment
        self.__max_fps_increment = max_fps_increment
        self.__min_fps_increment = min_fps_increment

        # Internal
        self.__fps_memory = [25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0]
        self.__frame = 0
        self.__max_frame = 8
        self.__departure_time = None

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
        if self._get_departure_time() is None:
            self._set_departure_time(self.get_time())

        # Increase Frame
        self._set_frame(self._get_frame() + 1)

        # The algho
        try:
            target = self._get_frame() / self.get_fps()
        except ZeroDivisionError:
            target = self._get_frame()

        passed = self.get_time() - self._get_departure_time()
        differ = target - passed

        # Reset time reference due to time variation
        if self._get_frame() > self._get_max_frame():
            self._set_departure_time(self.get_time())
            self._set_frame(0)

        self._get_fps_memory()[self._get_frame()] = self.get_fps()

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

    def set_fps(self, fps=25.0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps` attribute.

        :param fps: Frames number per second. (in **fps**)
        :type fps: float
        :raise TypeError: if ``fps`` parameter is not a :py:data:`float` type
        """
        if type(fps) == float:
            # CLAMP to the abosolut value
            calmped_value = abs(max(min(self.get_max_fps(), fps), self.get_min_fps()))
            if self.get_fps() != calmped_value:
                self.__fps = calmped_value
        else:
            raise TypeError(u'>fps< argument must be a float')

    def get_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`fps` attribute value.

        :return: :py:attr:`fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__fps

    def set_min_fps(self, min_fps=0.1):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps` attribute value.

        It correspond to a imposed minimal amount of frame rate

        :return: :py:attr:`min_fps` attribute value. (in **fps**)
        :rtype: float
        :raise TypeError: if ``min_fps`` parameter is not a :py:data:`float` type
        """
        if type(min_fps) == float:
            if self.get_min_fps() != min_fps:
                self.__min_fps = min_fps
        else:
            raise TypeError(u'>min_fps< argument must be a float')

    def get_min_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps` attribute value.

        :return: :py:attr:`min_fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__min_fps

    def set_max_fps(self, max_fps=60.0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps` attribute value.

        It correspond to a imposed minimal amount of frame rate

        :return: :py:attr:`max_fps` attribute value. (in **fps**)
        :rtype: float
        :raise TypeError: if ``max_fps`` parameter is not a :py:data:`float` type
        """
        if type(max_fps) == float:
            if self.get_max_fps() != max_fps:
                self.__max_fps = max_fps
        else:
            raise TypeError(u'>max_fps< argument must be a float')

    def get_max_fps(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps` attribute value.

        :return: :py:attr:`max_fps` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__max_fps

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

    def set_min_fps_increment(self, min_fps_increment=0.1):
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
            if self.get_min_fps_increment() != min_fps_increment:
                self.__min_fps_increment = min_fps_increment
        else:
            raise TypeError(u'>min_fps_increment< argument must be a float')

    def get_min_fps_increment(self):
        """
        Get the smaller of step increment

        The :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`min_fps_increment` attribute value.

        See :func:`Timer.set_min_fps_increment() <GLXBob.Timer.Timer.set_min_fps_increment()>` for more information's

        :return: :py:attr:`min_fps_increment` attribute value. (in **fps**)
        :rtype: float
        """
        return self.__min_fps_increment

    def set_max_fps_increment(self, max_fps_increment=1.0):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`max_fps_increment` increment.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps` attribute with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <GLXBob.Timer.Timer>` can use :py:attr:`min_fps_increment`
        and :py:attr:`max_fps_increment` for make gap in a increment range, where :py:attr:`max_fps_increment` will
        fixe the limit .

        :param max_fps_increment: Frames number per second. (in **fps**)
        :type max_fps_increment: float
        :raise TypeError: if ``max_fps_increment`` parameter is not a :py:data:`float` type
        """
        if type(max_fps_increment) == float:
            if self.get_max_fps_increment() != max_fps_increment:
                self.__max_fps_increment = max_fps_increment
        else:
            raise TypeError(u'>max_fps_increment< argument must be a float')

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
    def _set_departure_time(self, time_value):
        """
        Store a :func:`Timer.get_time() <GLXBob.Timer.Timer.get_time()>` return value inside
        :py:attr:`__departure_time` attribute.

        :param time_value: return value inside :py:attr:`__departure_time` attribute.
        :type time_value: a :func:`Timer.get_time() <GLXBob.Timer.Timer.get_time()>` return
        """
        if self._get_departure_time() != time_value:
            self.__departure_time = time_value

    def _get_departure_time(self):
        """
        Return the value set by a :func:`Timer._set_departure_time() <GLXBob.Timer.Timer._set_departure_time()>`

        :return: return :py:attr:`__departure_time` attribute.
        :rtype: :func:`time.time() <time.time()>`
        """
        return self.__departure_time

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

    def _set_max_frame(self, max_frame=8):
        """
        Set the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame_max` attribute.

        It will be use a maximum size of a list it contain :py:attr:`fps` attribute memory

        :param max_frame: correspond to the buffer size
        :type max_frame: int
        :raise TypeError: if ``max_frame`` parameter is not a :py:data:`int` type
        """
        if type(max_frame) == int:
            if self._get_max_frame() != max_frame:
                self.__max_frame = max_frame
        else:
            raise TypeError(u'>frame_max< argument must be a int')

    def _get_max_frame(self):
        """
        Get the :class:`Timer <GLXBob.Timer.Timer>` :py:attr:`__frame_max` attribute.

        You can set :py:attr:`__frame_max` attribute with
        :func:`Timer._set_frame_max() <GLXBob.Timer.Timer._set_frame_max()>` method.

        :return: ``__frame_max`` attribute value
        :rtype: int
        """
        return self.__max_frame


# Unittest
class TestTimer(unittest.TestCase):

    def setUp(self):
        # Before the test start
        print ('')

    def tearDown(self):
        # When the test is finish
        print(str(self.shortDescription()) + ' ... OK')

    # Test "fps" attribute
    def test_get_set_fps(self):
        """Test fps attribute with set_fps() and get_fps() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer.set_max_fps(float(random_value))
        timer.set_fps(float(random_value))
        self.assertEqual(float(random_value), timer.get_fps())

    def test_raise_typeerror_set_fps(self):
        """Test raise TypeError when set fps with worng type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer.set_fps, int(random_value))

    # Test "min_fps" attribute
    def test_get_set_min_fps(self):
        """Test min_fps attribute with set_min_fps() and get_min_fps() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer.set_min_fps(float(random_value))
        self.assertEqual(timer.get_min_fps(), float(random_value))

    def test_raise_typeerror_set_min_fps(self):
        """Test raise TypeError when set min_fps with worng type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer.set_min_fps, int(random_value))

    # Test "max_fps" attribute
    def test_get_set_max_fps(self):
        """Test max_fps attribute with set_max_fps() and get_max_fps() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer.set_max_fps(float(random_value))
        self.assertEqual(timer.get_max_fps(), float(random_value))

    def test_raise_typeerror_set_max_fps(self):
        """Test raise TypeError when set max_fps with worng type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer.set_max_fps, int(random_value))

    # Test "fps_increment" attribute
    def test_get_set_fps_increment(self):
        """Test fps_increment attribute with set_fps_increment() and get_fps_increment() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer.set_fps_increment(float(random_value))
        self.assertEqual(timer.get_fps_increment(), float(random_value))

    def test_raise_typeerror_set_fps_increment(self):
        """Test raise TypeError when set fps_increment with worng type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer.set_fps_increment, int(random_value))

    # Test "min_fps_increment" attribute
    def test_get_set_min_fps_increment(self):
        """Test min_fps_increment attribute with set_min_fps_increment() and get_min_fps_increment() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer.set_min_fps_increment(float(random_value))
        self.assertEqual(timer.get_min_fps_increment(), float(random_value))

    def test_raise_typeerror_set_min_fps_increment(self):
        """Test raise TypeError when set min_fps_increment with worng type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer.set_min_fps_increment, int(random_value))

    # Test "max_fps_increment" attribute
    def test_get_set_max_fps_increment(self):
        """Test max_fps_increment attribute with set_max_fps_increment() and get_min_fps_increment() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer.set_max_fps_increment(float(random_value))
        self.assertEqual(timer.get_max_fps_increment(), float(random_value))

    def test_raise_typeerror_set_max_fps_increment(self):
        """Test raise TypeError when set max_fps_increment with worng type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer.set_max_fps_increment, int(random_value))

    # Test get_time()
    def test_get_time_return(self):
        """Test get_time() method"""
        timer = Timer()
        returned_value_1 = timer.get_time()
        returned_value_2 = timer.get_time()
        self.assertLessEqual(returned_value_1, returned_value_2)

    ########################
    # Test internal method #
    ########################
    # Test "max_frame" attribute
    def test_get_set__max_frame(self):
        """Test max_frame attribute with _set_frame_max() and _get_frame_max() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer._set_max_frame(int(random_value))
        self.assertEqual(timer._get_max_frame(), float(random_value))

    def test_raise_typeerror_set__max_frame(self):
        """Test if _set_frame_max() raise TypeError when use a wrong type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer._set_max_frame, float(random_value))

    # Test "frame" attribute
    def test_get_set__frame(self):
        """Test frame attribute with _set_frame() and _get_frame() method's"""
        timer = Timer()
        random_value = randint(1, 250)
        timer._set_frame(int(random_value))
        self.assertEqual(timer._get_frame(), float(random_value))

    def test_raise_typeerror_set__frame(self):
        """Test if _set_frame() raise TypeError when use a wrong type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer._set_frame, float(random_value))

    # Test "departure_time" attribute
    def test_get_set__departure_time(self):
        """Test __departure_time attribute with _set_departure_time() and _get_departure_time() method's"""
        timer = Timer()
        tested_value = time()
        timer._set_departure_time(tested_value)
        self.assertEqual(timer._get_departure_time(), tested_value)

    # Test "fps_memory" attribute
    def test_get_set__fps_memory(self):
        """Test fps_memory attribute with _set_fps_memory() and _get_fps_memory() method's"""
        timer = Timer()
        value_list = sample(range(30), 4)
        timer._set_fps_memory(value_list)
        self.assertEqual(timer._get_fps_memory(), value_list)

    def test_raise_typeerror__set_fps_memory(self):
        """Test if _set_fps_memory() raise TypeError when use a wrong type"""
        timer = Timer()
        random_value = randint(1, 250)
        self.assertRaises(TypeError, timer._set_fps_memory, float(random_value))

# Run test if call directly
if __name__ == '__main__':
    unittest.main()
