#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time, sleep


class Timer:
    def __init__(self, fps=25, max_fps=60, min_fps=1, fps_increment=0.1, min_fps_increment=0.1, max_fps_increment=1.0):
        self.__fps = fps
        self.__min_fps = min_fps
        self.__max_fps = max_fps
        self.__fps_increment = fps_increment
        self.__max_fps_increment = max_fps_increment
        self.__min_fps_increment = min_fps_increment
        self.__frame = 0
        self.__start = None

    def tick(self):
        if self.__fps > self.__max_fps:
            self.__fps = float(self.__max_fps)
        if self.__start is None:
            self.__start = time()
        self.__frame += 1
        target = self.__frame / self.__fps
        passed = time() - self.__start
        differ = target - passed
        if differ < 0:
            # raise ValueError('cannot maintain desired FPS rate')
            self.set_fps(self.get_fps() - self.get_fps_increment())
            return True

        self.set_fps(self.get_fps() + self.get_fps_increment())
        sleep(differ)
        return False

    def set_fps(self, value):
        self.__fps = value

    def get_fps(self):
        return self.__fps

    def get_fps_increment(self):
        return self.__fps_increment

