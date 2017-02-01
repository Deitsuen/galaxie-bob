#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Tuuux <tuxa at rtnp dot org> all rights reserved

import os
import sys
import logging

# Require when you haven't GLXBob as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
import GLXBob

if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/galaxie-bob.log',
                        level=logging.DEBUG,
                        format='%(asctime)s, %(levelname)s, %(message)s')
    logging.info('Started glxbob-demo')

    mainloop = GLXBob.MainLoop()

    # 60 FPS is not so bad ...
    mainloop.get_timer().set_fps_max(60.0)

    # The Start
    mainloop.run()
    # The End
    quit()
