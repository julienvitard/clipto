#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Clipto main script and Plugin sample
"""

from __future__ import print_function

import sys


class StopProcess(Exception):
    pass


try:
    import tkinter
    from tkinter import messagebox
except ImportError:
    import Tkinter as tkinter
    import tkMessageBox as messagebox


class CliptoPlugin(object):
    """CliptoPlugin
    """
    name = None

    def process(self, content):
        raise NotImplemented


class EchoPlugin(CliptoPlugin):
    """Echo clipboard content as an introduction plugin
    """
    name = "Echo"

    def process(self, content):
        if content:
            print(content)


class Clipboard:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.withdraw()
        self.last_content = ''
        self.registry = []

    def watch(self):
        try:
            content = self.tk.clipboard_get()
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
        self.tk.after(100, self.watch)

    def run(self):
        try:
            self.tk.after(100, self.watch)
            self.tk.mainloop()
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
