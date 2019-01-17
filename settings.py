#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import tkinter


class Settings(tkinter.Tk):

    def __init__(self, root, parent):
        """
        creates instance of Settings class, takes root and parent as parameters.
        root - root form for this object
        parent - instance of Application class, form where Settings form was called
        """
        tkinter.Tk.__init__(self, root)

        self.vcodecs = [
            u"libtheora",
            u"libvpx",
            u"libwebp",
            u"libx264",
            u"libx264rgb",
            u"libxvid",
            u"png",
            u"ProRes"
        ]
        self.acodecs = [
            u"aac",
            u"ac3",
            u"ac3_fixed",
            u"libfaac"
            u"libfdk_aac",
            u"libmp3lame",
            u"libopencore-amrnb",
            u"libshine",
            u"libtwolame",
            u"libvo-aacenc",
            u"libvo-amrwbenc",
            u"libopus",
            u"libvorbis",
            u"libwavpack",
            u"wavpack"
        ]

        self.formats = [
            u"null",
            u"mov",
            u"ismv",
            u"mp3",
            u"ogg",
            u"aiff",
            u"crc",
            u"framecrc",
            u"md5",
            u"framemd5",
            u"gif",
            u"hls",
            u"ico",
            u"image2",
            u"matroska",
            u"mpegts"
        ]

        self.pixfmts = [
            u"yuv420p",
            u"yuv422p",
            u"yuv444p",
            u"yuv422",
            u"yuv410p",
            u"yuv411p",
            u"yuvj420p",
            u"yuvj422p",
            u"yuvj444p",
            u"rgb24",
            u"bgr24",
            u"rgba32",
            u"rgb565",
            u"rgb555",
            u"gray",
            u"monow",
            u"monob",
            u"pal8",
        ]

        self.initialize()
        self.parent = parent
        self.preset = parent.preset
        self.vcodecVar.set(self.preset['vcodec'])
        self.vbVar.set(self.preset['vb'])
        self.widthVar.set(self.preset['width'])
        self.heightVar.set(self.preset['height'])
        self.qmax.set(self.preset['qmax'])
        self.qmin.set(self.preset['qmin'])
        self.pixfmtVar.set(self.preset['pix_fmt'])
        self.acodecVar.set(self.preset['acodec'])
        self.arVar.set(self.preset['ar'])
        self.abVar.set(self.preset['ab'])
        self.formatVar.set(self.preset['format'])
        self.extraOptionsVar.set(self.preset['extraOptions'])

        self.protocol("WM_DELETE_WINDOW", self.onClose)

    def onClose(self):
        """
        Settings.onClose(inst)
        Runs when user want to close window
        """
        self.destroy()

    def initialize(self):
        """
        Settings.onClose(inst)
        Initializes form for innstance inst of class Settings
        """
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, True)
        self.grid()
        self.widgets()

    def widgets(self):
        """
        Settings.onClose(inst)
        Creates and adds control elements (labels, etries, buttons etc.) to the form of instance inst of class Settings
        """

        # Video options
        video = tkinter.LabelFrame(self, text=u"Video options")
        video.grid(row=0, column=0, sticky='NWES',
                   padx=5, pady=5, ipadx=5, ipady=5)

        # video codec

        self.vcodecVar = tkinter.StringVar(self)
        vcodecLbl = tkinter.Label(video, text=u"Video codec")
        vcodecLbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)

        self.vcodecList = tkinter.OptionMenu(
            video, self.vcodecVar, *self.vcodecs)
        self.vcodecList.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        # Video bitrate

        vbLbl = tkinter.Label(video, text=u"Video bitrate")
        vbLbl.grid(row=1, column=0, sticky="E", padx=5, pady=2)

        self.vbVar = tkinter.StringVar(self)
        self.vbVar.set(0)
        self.vb = tkinter.Entry(video, textvariable=self.vbVar)
        self.vb.grid(row=1, column=1, sticky="WE", padx=5, pady=2)

        # Video width

        widthLbl = tkinter.Label(video, text=u"Video width")
        widthLbl.grid(row=2, column=0, sticky="E", padx=5, pady=2)

        self.widthVar = tkinter.IntVar(self)
        self.width = tkinter.Entry(video, textvariable=self.widthVar)
        self.width.grid(row=2, column=1, sticky="WE", padx=5, pady=2)

        # Video height

        heightLbl = tkinter.Label(video, text=u"Video height")
        heightLbl.grid(row=3, column=0, sticky="E", padx=5, pady=2)

        self.heightVar = tkinter.IntVar(self)
        self.height = tkinter.Entry(video, textvariable=self.heightVar)
        self.height.grid(row=3, column=1, sticky="WE", padx=5, pady=2)

        # pixel format

        self.pixfmtVar = tkinter.StringVar(self)
        pixfmtLbl = tkinter.Label(video, text=u"Pixel format")
        pixfmtLbl.grid(row=4, column=0, sticky='E', padx=5, pady=2)

        self.pixfmtList = tkinter.OptionMenu(
            video, self.pixfmtVar, *self.pixfmts)
        self.pixfmtList.grid(row=4, column=1, sticky="W", padx=5, pady=2)

        # frame rate

        fpsLbl = tkinter.Label(video, text=u"Frame rate")
        fpsLbl.grid(row=5, column=0, sticky='E', padx=5, pady=2)

        fpsComment = tkinter.Label(
            video, text=u"(if value is 0 than takes FPS from source)")
        fpsComment.grid(row=6, column=1, sticky='NW', padx=5, pady=2)
        self.fpsVar = tkinter.IntVar(self)
        self.fps = tkinter.Entry(video, textvariable=self.fpsVar)
        self.fps.grid(row=5, column=1, sticky="WE", padx=5, pady=2)

        # min quality

        self.qmin = tkinter.Scale(
            video, from_=-1, to=69, orient=tkinter.HORIZONTAL, label=u"Minimum quality")
        self.qmin.grid(row=7, column=0, columnspan=2,
                       sticky="WE", padx=5, pady=2)
        self.qmin.set(2)

        # max quality

        self.qmax = tkinter.Scale(
            video, from_=-1, to=1024, orient=tkinter.HORIZONTAL, label=u"Maximum quality")
        self.qmax.grid(row=8, column=0, columnspan=2,
                       sticky="WE", padx=5, pady=2)
        self.qmax.set(31)

        # Audio options

        audio = tkinter.LabelFrame(self, text=u"Audio options")
        audio.grid(row=0, column=1, sticky='NWES',
                   padx=5, pady=5, ipadx=5, ipady=5)

        # audio codec

        vcodecLbl = tkinter.Label(audio, text=u"Audio codec")
        vcodecLbl.grid(row=0, column=0, sticky="E", padx=5, pady=2)

        self.acodecVar = tkinter.StringVar(self)
        self.acodecList = tkinter.OptionMenu(
            audio, self.acodecVar, *self.acodecs)
        self.acodecList.grid(row=0, column=1, sticky="W", padx=5, pady=2)

        # Audio frequency

        arLbl = tkinter.Label(audio, text=u"Audio frequency")
        arLbl.grid(row=1, column=0, sticky="E", padx=5, pady=2)

        self.arVar = tkinter.IntVar(self)
        self.ar = tkinter.Entry(audio, textvariable=self.arVar)
        self.ar.grid(row=1, column=1, sticky="W", padx=5, pady=2)

        # Audio bitrate

        abLbl = tkinter.Label(audio, text=u"Audio bitrate")
        abLbl.grid(row=2, column=0, sticky="E", padx=5, pady=2)

        self.abVar = tkinter.StringVar(self)
        self.abVar.set(0)
        self.ab = tkinter.Entry(audio, textvariable=self.abVar)
        self.ab.grid(row=2, column=1, sticky="W", padx=5, pady=2)

        # Options

        options = tkinter.LabelFrame(self, text=u"Options")
        options.grid(row=1, columnspan=2, sticky='WE',
                     padx=5, pady=5, ipadx=5, ipady=5)

        # Format

        formatLbl = tkinter.Label(options, text=u"Format")
        formatLbl.grid(row=0, column=0, sticky="E", padx=5, pady=2)

        self.formatVar = tkinter.StringVar(self)
        self.formatList = tkinter.OptionMenu(
            options, self.formatVar, *self.formats)
        self.formatList.grid(row=0, column=1, sticky="W", padx=5, pady=2)

        # Format options

        extraOptionsLbl = tkinter.Label(options, text="Extra options")
        extraOptionsLbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)

        self.extraOptionsVar = tkinter.StringVar(self)
        extraOptionsTxt = tkinter.Entry(
            options, textvariable=self.extraOptionsVar, width="65")
        extraOptionsTxt.grid(row=1, column=1, sticky="WE", pady=3)

        # Save changes of preset button

        saveButton = tkinter.Button(
            self, text=u"Save", command=self.onSaveClick)
        saveButton.grid(row=3, column=0, sticky='NWES', padx=5, pady=2)

        # Cancel changes of preset button

        cancelButton = tkinter.Button(
            self, text=u"Cancel", command=self.onClose)
        cancelButton.grid(row=3, column=1, sticky='NWES', padx=5, pady=2)

    def onSaveClick(self):
        """
        Settings.OnSaveClick(inst)
        Copies choosen custom options for preset into preset dict, save it in parent (instance of Application class)
        and closes itself
        """
        self.preset['vcodec'] = self.vcodecVar.get()
        self.preset['vb'] = self.vbVar.get()
        self.preset['fps'] = self.fpsVar.get()
        self.preset['width'] = self.widthVar.get()
        self.preset['height'] = self.heightVar.get()
        self.preset['qmax'] = self.qmax.get()
        self.preset['qmin'] = self.qmin.get()
        self.preset['pix_fmt'] = self.pixfmtVar.get()
        self.preset['acodec'] = self.acodecVar.get()
        self.preset['ar'] = self.arVar.get()
        self.preset['ab'] = self.abVar.get()
        self.preset['format'] = self.formatVar.get()
        self.preset['extraOptions'] = self.extraOptionsVar.get()

        self.parent.preset = self.preset
        self.parent.updateTotalInfo(self.preset)
        self.destroy()
