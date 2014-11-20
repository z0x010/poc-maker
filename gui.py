#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from poc_maker import poc_maker
from poc_clean_info import generate_info, info_temp
from utils.file_maker import read_poc_info
from utils.env import paths
from utils.env import set_paths



class InfoFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "poc_maker")
        panel = wx.Panel(self)

        top_lbl = wx.StaticText(panel, -1, "POC MAKER")
        top_lbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        appname_lbl = wx.StaticText(panel, -1, "*appname:")
        appname = wx.TextCtrl(panel, -1, "", size=(800, -1), name="appname")
        appversion_lbl = wx.StaticText(panel, -1, "appversion:")
        appversion = wx.TextCtrl(panel, -1, "", name="appversion")
        appvendor_lbl = wx.StaticText(panel, -1, "appvendor:")
        appvendor = wx.TextCtrl(panel, -1, "", name="appvendor")
        vulid_lbl = wx.StaticText(panel, -1, "vulid:")
        vulid = wx.TextCtrl(panel, -1, "", name="vulid")
        vulpath_lbl = wx.StaticText(panel, -1, "*vulpath:")
        vulpath = wx.TextCtrl(panel, -1, "", name="vulpath")
        vultype_lbl = wx.StaticText(panel, -1, "*vultype:")
        vultype = wx.TextCtrl(panel, -1, "", name="vultype")
        vulreferer_lbl = wx.StaticText(panel, -1, "*vulreferer:")
        vulreferer = wx.TextCtrl(panel, -1, "", name="vulreferer")
        vuldesc_lbl = wx.StaticText(panel, -1, "*vuldesc:")
        vuldesc = wx.TextCtrl(panel, -1, "", name="vuldesc")
        vuleffect_lbl = wx.StaticText(panel, -1, "*vuleffect:")
        vuleffect = wx.TextCtrl(panel, -1, "", name="vuleffect")
        vuldate_lbl = wx.StaticText(panel, -1, "*vuldate:")
        vuldate = wx.TextCtrl(panel, -1, "", name="vuldate")
        tools_lbl = wx.StaticText(panel, -1, "*tools:")
        tools = wx.TextCtrl(panel, -1, "", name="tools")
        tooldesc_lbl = wx.StaticText(panel, -1, "*tooldesc:")
        tooldesc = wx.TextCtrl(panel, -1, "", name="tooldesc")
        myname_lbl = wx.StaticText(panel, -1, "*myname:")
        myname = wx.TextCtrl(panel, -1, "", name="myname")
        shortname_lbl = wx.StaticText(panel, -1, "*shorname:")
        shortname = wx.TextCtrl(panel, -1, "", name="shortname")
        targeturl_lbl = wx.StaticText(panel, -1, "#traget_url:")
        targeturl = wx.TextCtrl(panel, -1, "", name="info_target_url")
        postdata_lbl = wx.StaticText(panel, -1, "#post_data:")
        postdata = wx.TextCtrl(panel, -1, "", name="info_post_data")
        match_lbl = wx.StaticText(panel, -1, "#match:")
        match = wx.TextCtrl(panel, -1, "", name="info_match")
        othermatch_lbl = wx.StaticText(panel, -1, "#other_match:")
        othermatch = wx.TextCtrl(panel, -1, "", name="info_other_match")
        testurl_lbl = wx.StaticText(panel, -1, "#testurl:")
        testurl = wx.TextCtrl(panel, -1, "", name="info_test_url")

        make_btn = wx.Button(panel, -1, "Maker", name="poc_maker")
        clean_btn = wx.Button(panel, -1, "Clean", name="poc_clean_info")


        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(top_lbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)


        infoSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        infoSizer.AddGrowableCol(1)
        infoSizer.Add(appname_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(appname, 0, wx.EXPAND)
        infoSizer.Add(appversion_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(appversion, 0, wx.EXPAND)
        infoSizer.Add(appvendor_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(appvendor, 0, wx.EXPAND)
        infoSizer.Add((10, 10))
        infoSizer.Add((10, 10))
        infoSizer.Add(vulid_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vulid, 0, wx.EXPAND)
        infoSizer.Add(vulpath_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vulpath, 0, wx.EXPAND)
        infoSizer.Add(vultype_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vultype, 0, wx.EXPAND)
        infoSizer.Add(vulreferer_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vulreferer, 0, wx.EXPAND)
        infoSizer.Add(vuldesc_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vuldesc, 0, wx.EXPAND)
        infoSizer.Add(vuleffect_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vuleffect, 0, wx.EXPAND)
        infoSizer.Add(vuldate_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vuldate, 0, wx.EXPAND)
        infoSizer.Add((10, 10))
        infoSizer.Add((10, 10))
        infoSizer.Add(tools_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(tools, 0, wx.EXPAND)
        infoSizer.Add(tooldesc_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(tooldesc, 0, wx.EXPAND)
        infoSizer.Add((10, 10))
        infoSizer.Add((10, 10))
        infoSizer.Add(myname_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(myname, 0, wx.EXPAND)
        infoSizer.Add(shortname_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(shortname, 0, wx.EXPAND)
        infoSizer.Add((10, 10))
        infoSizer.Add((10, 10))
        infoSizer.Add(targeturl_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(targeturl, 0, wx.EXPAND)
        infoSizer.Add(postdata_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(postdata, 0, wx.EXPAND)
        infoSizer.Add(match_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(match, 0, wx.EXPAND)
        infoSizer.Add(othermatch_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(othermatch, 0, wx.EXPAND)
        infoSizer.Add(testurl_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(testurl, 0, wx.EXPAND)

        mainSizer.Add(infoSizer, 0, wx.EXPAND | wx.ALL, 10)


        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(make_btn)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(clean_btn)
        btnSizer.Add((20, 20), 1)

        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)


        panel.SetSizer(mainSizer)

        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)


class App(wx.App):

    words = {'appname': '', 'vuldate': '', 'vuleffect': '', 'vuldesc': '', 'vultype': '', 'vulid': '', 'appvendor': '', 'vuldesc': '', 'vulreferer': '', 'tools': '', 'tooldesc': '', 'myname': '', 'shortname': '', 'info_target_url': '', 'info_post_data': '', 'info_match': '', 'info_other_match': '', 'info_test_url': '', 'appversion': '', 'vulpath': ''} 

    def OnInit(self):
        set_paths()
        self.frame = InfoFrame()
        self.frame.Show()
        self.frame.Bind(wx.EVT_BUTTON, self.make_click, wx.FindWindowByName('poc_maker'))
        self.frame.Bind(wx.EVT_BUTTON, self.clean_click, wx.FindWindowByName('poc_clean_info'))
        self.read_info()
        return True


    def read_info(self):
        read_poc_info(self.words, paths.INFO_PATH, modify=False)
        for key in self.words:
            textctrl = wx.FindWindowByName(key)
            try:
                textctrl.Clear()
            except AttributeError:
                pass
            textctrl.AppendText(self.words[key])


    def make_click(self, event):
        for key in self.words:
            textctrl = wx.FindWindowByName(key)
            value = textctrl.GetValue()
            self.words[key] = value

        info_words = self.words
        info_file = paths.INFO_PATH
        f = open(info_file, 'w')
        info = generate_info(info_temp, info_words)
        f.write(info.encode('utf-8'))
        f.close()

        poc_maker(info_file, self.words)


    def clean_click(self, event):
        for key in self.words:
            textctrl = wx.FindWindowByName(key)
            textctrl.Clear()


if __name__ == "__main__":
    app = App()
    app.MainLoop()