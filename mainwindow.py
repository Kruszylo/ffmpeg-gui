#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import tkinter
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
#from filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import subprocess
import fcntl
import select
import os
import re
import threading
import time
from settings import Settings
from tkinter.constants import END, LEFT, BOTH

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

class Application(tkinter.Tk):

    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        if is_tool('ffmpeg') == False:
            messagebox.showwarning(
                u"FFMPEG not found!", 
                u"You must install ffmpeg on you computer before using this GUI")
        self.presets = {
            'H.264 720p': {
                'vcodec':        'libx264',
                'vb':            '3500k',
                'width':         1280,
                'height':        720,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'aac',
                'ar':            44100,
                'ab':            '128k',
                'format':        'mp4',
                'extraOptions':  '-movflags faststart'
            },
            'H.264 576p': {
                'vcodec':        'libx264',
                'vb':            '2000k',
                'width':         1024,
                'height':        576,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'aac',
                'ar':            44100,
                'ab':            '128k',
                'format':        'mp4',
                'extraOptions':  '-movflags faststart'
            },
            'H.264 360p': {
                'vcodec':        'libx264',
                'vb':            '1000k',
                'width':         640,
                'height':        360,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'aac',
                'ar':            44100,
                'ab':            '128k',
                'format':        'mp4',
                'extraOptions':  '-movflags faststart -maxrate 1500k -bufsize 3000k'
            },
            'WebM 720p': {
                'vcodec':        'libvpx',
                'vb':            '3500k',
                'width':         1280,
                'height':        720,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'libvorbis',
                'ar':            44100,
                'ab':            '128k',
                'format':        'webm',
                'extraOptions':  '-quality good'
            },
            'WebM 576p': {
                'vcodec':        'libvpx',
                'vb':            '2000k',
                'width':         1024,
                'height':        576,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'libvorbis',
                'ar':            44100,
                'ab':            '128k',
                'format':        'webm',
                'extraOptions':  '-quality good'
            },
            'WebM 360p': {
                'vcodec':        'libvpx',
                'vb':            '1500k',
                'width':         640,
                'height':        360,
                'qmax':          51,
                'qmin':          11,
                'pix_fmt':       'yuv420p',
                'acodec':        'libvorbis',
                'ar':            44100,
                'ab':            '128k',
                'format':        'webm',
                'extraOptions':  '-quality good'
            },
        }

        self.initialize()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.inputFiles = []
    
    def initialize(self):
        """
        Application.initialize(inst)
        Initializes form for innstance inst of class Application
        """
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, True)
        self.grid()
        self.widgets()
        self.cancelEncoding = False
        self.cmd = None

    def widgets(self):
        """
        Application.widgets(inst)
        Creates and adds control elements (labels, etries, buttons etc.) to the form of instance inst of class Application
        """
        # Source file  frame

        source = tkinter.LabelFrame(self, text=u"Source file")
        source.grid(row=0, columnspan=3, sticky='WE',
                    padx=5, pady=5, ipadx=5, ipady=5)

        inputFileLbl = tkinter.Label(source, text="Select File:")
        inputFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.inputFileVar = tkinter.StringVar()
        self.inputFileTxt = tkinter.Entry(
            source, textvariable=self.inputFileVar, width="50")
        self.inputFileTxt.grid(row=0, column=1, sticky="WE", pady=3)

        inputFileButton = tkinter.Button(
            source, text="Browse ...", command=self.onInputBrowseClick)
        inputFileButton.grid(row=0, column=2, sticky='W', padx=5, pady=2)

        # Output file frame

        output = tkinter.LabelFrame(self, text=u"Output details")
        output.grid(row=1, columnspan=3, sticky='WE',
                    padx=5, pady=5, ipadx=5, ipady=5)

        outputFileLbl = tkinter.Label(output, text="Save File to:")
        outputFileLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.outputFileVar = tkinter.StringVar()

        self.outputFileTxt = tkinter.Entry(
            output, textvariable=self.outputFileVar, width="50")
        self.outputFileTxt.grid(row=0, column=1, sticky="WE", pady=3)

        outputFileButton = tkinter.Button(
            output, text="Browse ...", command=self.onOutputBrowseClick)
        outputFileButton.grid(row=0, column=2, sticky='W', padx=5, pady=2)

        # Preset frame

        preset = tkinter.LabelFrame(self, text=u"Preset")
        preset.grid(row=2, columnspan=3, sticky='WE',
                    padx=5, pady=5, ipadx=5, ipady=5)

        # presets list

        presetsLbl = tkinter.Label(preset, text=u"Use a preset")
        presetsLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        presets = []
        for presetName, presetOptions in self.presets.items():
            presets.append(presetName)

        self.presetsVar = tkinter.StringVar()
        self.presetsVar.trace("w", self.OnPresetSelected)
        self.presetsList = tkinter.OptionMenu(
            preset, self.presetsVar, *presets)
        self.presetsList.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.showSettingsButton = tkinter.Button(
            preset, text="More ...",state='disabled', command=self.onShowSettingsClick)
        self.showSettingsButton.grid(row=0, column=3, sticky='W', padx=5, pady=2)
        
        # total information about preset
        
        self.total_info = ''
        total = tkinter.LabelFrame(self, text=u"Total inforation")
        total.grid(row=3, columnspan=2, sticky='WE', padx=10, pady=10, ipadx=5, ipady=5)
        self.totalLbl = tkinter.Label(total, text=self.total_info, anchor="e", justify=LEFT)
        self.totalLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        
        # Encode button

        self.encodeButton = tkinter.Button(
            self, text=u"Encode", state='disabled', command=self.onEncodeClick)
        self.encodeButton.grid(row=15, column=0, sticky='NWES', padx=5, pady=2)

        # Progress bar

        self.progress = ttk.Progressbar(
            self, orient='horizontal', mode="determinate")
        self.progress.grid(row=15, column=1, sticky="WE", padx=5, pady=2)
   
        #Cancel encoding button

        self.cancelEncodeButton = tkinter.Button(
            self, text=u"Cancel", state='disabled', command=self.onCancelEncodeClick)
        self.cancelEncodeButton.grid(row=15, column=2, sticky='NWES', padx=5, pady=2)

    def onClose(self):
        """
        Application.onClose(inst)
        Runs when form is about to be closed, asks if user sure that he want to close the form 
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
    
    def onInputBrowseClick(self):
        """
        Application.onInputBrowseClick(inst)
        Shows default window for choosing file
        """
        self.inputFiles = askopenfilename(multiple=True)
        self.inputFileVar.set(self.inputFiles)

    def onOutputBrowseClick(self):
        """
        Application.onInputBrowseClick(inst)
        Shows default window for choosing where to save file
        """
        self.outputFile = asksaveasfilename()
        self.outputFileVar.set(self.outputFile)
        
    def OnPresetSelected(self, *argv):
        preset = self.presetsVar.get()
        if self.presets[preset]:
            self.preset = self.presets[preset]
            self.showSettingsButton['state'] = 'normal'
            self.encodeButton['state'] = 'normal'
        self.updateTotalInfo(preset)
            
            
    def onShowSettingsClick(self):
        """
        Application.onShowSettingsClick(inst)
        Shows form with detailed settings for choosen preset
        """
        self.settings_window = Settings(None, self)
        self.settings_window.title("Settings")
    
    def updateTotalInfo(self, preset):
        """
        Application.updateTotalInfo(inst, preset)
        Update displayed on inst main form text about preset, mainly shows all keys and values from preset
        type(preset) - dict
        """
        self.total_info = ''
        for key, value in self.preset.items():
            self.total_info += f'{key}: {value}\n'
        self.totalLbl['text'] = self.total_info
        
    def onEncodeClick(self):
        """
        Application.onEncodeClick(inst)
        Runs encoding of choosen files with choosen preset
        """
        if self.inputFiles:
            files = self.splitlist(self.inputFiles)
            for filename in files:
                self.encodeFile(filename)
                self.cancelEncodeButton['state'] = 'normal'
        else:
            messagebox.showwarning(
                u"No source selected", u"You must define at least one file to encode")

    def onCancelEncodeClick(self):
        """
        Application.onCancelEncodeClick(inst)
        Stops encoding of files if user wants so
        """
        response = messagebox.askokcancel(
            "Stop encoding?",
            "The encoding is still running!\n Do you want to stop it?\n \
            All files which are not encoded yet will not be encoded!")
        if response:
            if self.cmd is not None:
                self.cancelEncoding = True

    def encodeFile(self, filename):
        """
        Application.encodeFile(inst, filename)
        Encodes file with choosen preset in a subprocess
        """
        self.t_encodeFile = threading.currentThread()

        output = self.outputFileVar.get()
        out_format = self.preset['format']
        if output.endswith('.'+out_format) == False:
            output += '.' + out_format
        vcodec = self.preset['vcodec']
        vb = self.preset['vb']
        fps = self.preset.get('fps',0)
        qmax = self.preset['qmax']
        qmin = self.preset['qmin']
        pixfmt = self.preset['pix_fmt']
        width = self.preset['width']
        height = self.preset['height'] 
        acodec = self.preset['acodec']
        ar = self.preset['ar']
        ab = self.preset['ab']
        extraOptions = self.preset['extraOptions']

        command = 'ffmpeg -i {0} -y {1} -f {2}'.format(
            filename, output, out_format)
        video = '-vcodec {0} -vb {1} -qmax {2} -qmin {3} -pix_fmt {4}'.format(
            vcodec, vb, qmax, qmin, pixfmt)
        if fps:
            video += ' -r {}'.format(fps)
        scale = '-vf "scale=iw*min({0}/iw\,{1}/ih):ih*min({0}/iw\,{1}/ih),pad={0}:{1}:({0}-iw)/2:({1}-ih)/2"'.format(
            width, height)
        audio = '-acodec {0} -ar {1} -ab {2}'.format(acodec, ar, ab)
        options = '-strict experimental -threads 0' + ' ' + extraOptions
        command = command + ' ' + video + ' ' + scale + ' ' + audio + ' ' + options
        # print cmd

        print(f'command is:{command}')
        self.cmd = subprocess.Popen(
            command, shell=True, stderr=subprocess.PIPE)
        fcntl.fcntl(
            self.cmd.stderr.fileno(),
            fcntl.F_SETFL,
            fcntl.fcntl(
                self.cmd.stderr.fileno(),
                fcntl.F_GETFL
            ) | os.O_NONBLOCK,
        )

        duration = None
        header = ""
        progress_regex = re.compile(
            "frame=.*time=([0-9\:\.]+)",
            flags=re.IGNORECASE
        )
        header_received = False

        while True:
            progressline = select.select([self.cmd.stderr.fileno()], [], [])[0]
            if progressline:
                line = self.cmd.stderr.read().decode('utf-8')
                if line == "":
                    self.complete_callback()
                    break
                progress_match = progress_regex.match(line)
                if progress_match:
                    if not header_received:
                        header_received = True

                        if re.search(
                            ".*command\snot\sfound",
                            header,
                            flags=re.IGNORECASE
                        ):
                            messagebox.showerror(
                                u"Command error", u"Command not found")

                        if re.search(
                            "Unknown format",
                            header,
                            flags=re.IGNORECASE
                        ):
                            messagebox.showerror(
                                u"Unknown format", u"Unknown format")

                        if re.search(
                            "Duration: N\/A",
                            header,
                            flags=re.IGNORECASE | re.MULTILINE
                        ):
                            messagebox.showerror(
                                u"Unreadable file", u"Unreadable file")

                        raw_duration = re.search(
                            "Duration:\s*([0-9\:\.]+),",
                            header
                        )
                        if raw_duration:
                            units = raw_duration.group(1).split(":")
                            duration = (int(units[0]) * 60 * 60 * 1000) + (
                                int(units[1]) * 60 * 1000) + int(float(units[2]) * 1000)

                    if duration:
                        units = progress_match.group(1).split(":")
                        progress = (int(units[0]) * 60 * 60 * 1000) + (
                            int(units[1]) * 60 * 1000) + int(float(units[2]) * 1000)
                        self.progress_callback(progress, duration)

                else:
                    header += line

            time.sleep(0.0001)
            if self.cancelEncoding:
                self.cmd.kill()
                break
        self.cancelEncoding = False
        self.cancelEncodeButton['state'] = 'disable'

    def progress_callback(self, progress, duration):
        """
        Application.encodeFile(inst, progress_value, duration)
        Updates encoding progress bar 
        """
        self.progress["maximum"] = duration
        self.progress["value"] = progress
        self.progress.update()

    def complete_callback(self):
        """
        Application.encodeFile(inst)
        Shows messege box when encoding is completed
        """
        messagebox.showinfo(u"Encoding complete", u"Encoding complete")

