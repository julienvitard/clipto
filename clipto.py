#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Clipto main script and Plugin sample
"""

from __future__ import print_function

import sys

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


class StopProcess(Exception):
    """Exception to stop execution process
    """


class CliptoPlugin:
    """CliptoPlugin interface
    """
    name = None

    def process(self, content):
        """Process content of clipboard

        :params any content: clipboard content
        :rtype: NoneType
        :return: None
        :raises StopProcess: to break the process execution list
        """
        raise NotImplementedError


class EchoPlugin(CliptoPlugin):
    """Echo clipboard content as an introduction plugin
    """
    name = "Echo"

    def process(self, content):
        """Echoes the content of clipboard
        """
        if content:
            print(content)


class Clipboard:
    """Clipboard main class
    """
    def __init__(self):
        self.tkinter = tkinter.Tk()
        self.tkinter.withdraw()
        self.last_content = ''
        self.registry = []

    def watch(self):
        """Watch clipboard content
        """
        try:
            content = self.tkinter.clipboard_get()
            if content != self.last_content:
                self.last_content = content
                for plugin in self.registry:
                    try:
                        plugin().process(content)
                    except StopProcess:
                        break
                    except Exception:
                        pass

        except KeyboardInterrupt:
            print("\b\bBye ;-)")
            sys.exit()
        except tkinter.TclError:
            pass
        self.tkinter.after(100, self.watch)

    def run(self):
        """Exexcute main loop
        """
        try:
            self.tkinter.after(100, self.watch)
            self.tkinter.mainloop()
        except KeyboardInterrupt:
            print("\b\bBye ;-)")
        except Exception:
            pass


if __name__ == '__main__':
    clipto = Clipboard()
    clipto.registry = [
        EchoPlugin
    ]
    clipto.run()
