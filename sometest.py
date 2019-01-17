#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 01:10:04 2019

@author: kruszylo
"""
import unittest
import tkinter, _tkinter
from mainwindow import Application
from mainwindow import is_tool

class TKinterTestCase(unittest.TestCase):
    """These methods are going to be the same for every GUI test,
    so refactored them into a separate class
    """
    def setUp(self):
        self.root=tkinter.Tk()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
            pass

class TestViewAskText(TKinterTestCase):
    def test_enter(self):
        app = Application(None) 
        self.pump_events()
        app.inputFileVar.set(u'inputFileVar')
        self.pump_events()
        self.assertEqual(app.inputFileTxt.get(),u'inputFileVar')
        
    def test_is_ffmpeg_installed(self):
        self.assertEqual(is_tool('ffmpeg'),True)
        
    def test_is_is_tool_works(self):
        self.assertEqual(is_tool('somethingthatcantbeinstalled'),False)
        
if __name__ == '__main__':
    import unittest
    unittest.main()