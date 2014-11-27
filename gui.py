#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

from datetime import date

from poc_maker import poc_maker
from poc_clean_info import generate_info, info_temp, check_site
from utils.file_maker import read_poc_info
from utils.env import paths
from utils.env import set_paths
from utils.weekdays import weekdays


class InfoFrame(wx.Frame):

    type_list = ['SQL Injection', 'Arbitrary File Download', 'File Upload', 'Command Execution', 'Code Execution', 'Remote File Inclusion', 'Local File Inclusion' 'Privilege Escalation', 'Arbitrary File Deletion', 'Directory Traversal', 'Login Bypass', 'Weak Password', 'Information Disclosure']
    tool_list = ['sqlmap', 'Firefox', 'curl']

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "poc_maker")
        panel = wx.Panel(self)

        top_lbl = wx.StaticText(panel, -1, "POC MAKER: " + weekdays().replace(':', '/'))
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
        vultype = wx.ComboBox(panel, -1, "", (15, 30), wx.DefaultSize, self.type_list, wx.CB_DROPDOWN, name="vultype")
        # vultype = wx.TextCtrl(panel, -1, "", name="vultype")
        vulreferer_lbl = wx.StaticText(panel, -1, "*vulreferer:")
        vulreferer = wx.TextCtrl(panel, -1, "", name="vulreferer")
        vuldesc_lbl = wx.StaticText(panel, -1, "*vuldesc:")
        vuldesc = wx.TextCtrl(panel, -1, "", name="vuldesc")
        vuleffect_lbl = wx.StaticText(panel, -1, "*vuleffect:")
        vuleffect = wx.TextCtrl(panel, -1, "", name="vuleffect")
        vuldate_lbl = wx.StaticText(panel, -1, "*vuldate:")
        vuldate = wx.TextCtrl(panel, -1, "", name="vuldate")
        tools_lbl = wx.StaticText(panel, -1, "*tools:")
        tools = wx.ComboBox(panel, -1, "", (15, 30), wx.DefaultSize, self.tool_list, wx.CB_DROPDOWN, name="tools")
        # tools = wx.TextCtrl(panel, -1, "", name="tools")
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
        loadinfo_btn = wx.Button(panel, -1, "Load", name="load_poc_info")
        writeinfo_btn = wx.Button(panel, -1, "Write", name="write_poc_info")
        url_btn = wx.Button(panel, -1, "URL", name="read_from_url")

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
        infoSizer.Add(vuleffect_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vuleffect, 0, wx.EXPAND)
        infoSizer.Add(vulreferer_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vulreferer, 0, wx.EXPAND)
        infoSizer.Add(vuldesc_lbl, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        infoSizer.Add(vuldesc, 0, wx.EXPAND)
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
        btnSizer.Add((10, 10), 1)
        btnSizer.Add(make_btn)
        btnSizer.Add(clean_btn)
        btnSizer.Add((10, 10), 1)
        btnSizer.Add(loadinfo_btn)
        btnSizer.Add(writeinfo_btn)
        btnSizer.Add(url_btn)
        btnSizer.Add((10, 10), 1)

        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)

        panel.SetSizer(mainSizer)

        mainSizer.Fit(self)
        mainSizer.SetSizeHints(self)



class App(wx.App):

    words = {'appname': '', 'vuldate': '', 'vuleffect': '', 'vuldesc': '', 'vultype': '', 'vulid': '', 'appvendor': '', 'vuldesc': '', 'vulreferer': '', 'tools': '', 'tooldesc': '',
             'myname': '', 'shortname': '', 'info_target_url': '', 'info_post_data': '', 'info_match': '', 'info_other_match': '', 'info_test_url': '', 'appversion': '', 'vulpath': ''}

    def OnInit(self):
        set_paths()
        self.frame = InfoFrame()
        self.frame.Show()
        self.frame.Bind(wx.EVT_BUTTON, self.make_click, wx.FindWindowByName('poc_maker'))
        self.frame.Bind(wx.EVT_BUTTON, self.clean_click, wx.FindWindowByName('poc_clean_info'))
        self.frame.Bind(wx.EVT_BUTTON, self.load_click, wx.FindWindowByName('load_poc_info'))
        self.frame.Bind(wx.EVT_BUTTON, self.write_click, wx.FindWindowByName('write_poc_info'))
        self.frame.Bind(wx.EVT_BUTTON, self.url_click, wx.FindWindowByName('read_from_url'))
        self.frame.Bind(wx.EVT_COMBOBOX, self.set_vuleffect, wx.FindWindowByName('vultype'))
        self.frame.Bind(wx.EVT_COMBOBOX, self.set_tooldesc, wx.FindWindowByName('tools'))
        self.read_info()
        return True

    def read_info(self):
        read_poc_info(self.words, paths.INFO_PATH, modify=False)
        for key in self.words:
            textctrl = wx.FindWindowByName(key)
            if key not in ('vultype', 'tools'):
                try:
                    textctrl.Clear()
                except AttributeError:
                    pass
                textctrl.AppendText(self.words[key])
            else:
                textctrl.SetValue(self.words[key])

    def make_click(self, event):
        info_file = self.write_info()
        poc_maker(info_file, self.words)

    def clean_click(self, event):
        default_key = ['vultype', 'vuleffect', 'tools', 'tooldesc', 'myname', 'shortname']
        for key in self.words:
            if key not in default_key:
                textctrl = wx.FindWindowByName(key)
                textctrl.Clear()
        textctrl = wx.FindWindowByName('vuldate')
        textctrl.AppendText(str(date.today()))

    def load_click(self, event):
        self.read_info()

    def write_click(self, event):
        self.write_info()

    def url_click(self, event):
        dialog = wx.TextEntryDialog(None, "Please entry url", "Read info from url", "")
        if dialog.ShowModal() == wx.ID_OK:
            progress = wx.ProgressDialog("Read info from url", "Reading...", 10, style=wx.PD_AUTO_HIDE)
            progress.Update(6)
            url = dialog.GetValue()
            self.words = check_site(url)
            progress.Update(10)

            for key in self.words:
                textctrl = wx.FindWindowByName(key)
                try:
                    textctrl.Clear()
                except AttributeError:
                    pass
                textctrl.AppendText(self.words[key])

    def set_vuleffect(self, event):
        vultype = wx.FindWindowByName('vultype')
        vuleffect = wx.FindWindowByName('vuleffect')
        effect = self.trans_type(vultype.GetValue())
        try:
            vuleffect.Clear()
        except AttributeError:
            pass
        vuleffect.AppendText(effect)

    
    def set_tooldesc(self, event):
        tools = wx.FindWindowByName('tools')
        tooldesc = wx.FindWindowByName('tooldesc')
        desc = self.trans_tools(tools.GetValue())
        try:
            tooldesc.Clear()
        except AttributeError:
            pass
        tooldesc.AppendText(desc)

    def write_info(self):
        error = self.check_info()
        if not error:
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
            return info_file
        else:
            wx.MessageBox("Some info must be provided", "Error")

    def check_info(self):
        error_list = ['appname', 'vultype', 'vulpath', 'appvendor', 'vulreferer', 'vuldesc', 'vuleffect', 'vuldate', 'myname', 'shortname']
        error = False
        for key in error_list:
            textctrl = wx.FindWindowByName(key)
            value = textctrl.GetValue()
            if not value:
                textctrl.SetBackgroundColour("pink")
                textctrl.Refresh()
                error = True
            else:
                textctrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                textctrl.Refresh()

        return error

    def trans_tools(self, tool):
        key_dic = {
            'sqlmap': u'SQL注入测试工具',
            'firefox': u'浏览器',
            'curl': u'文件传输工具',
        }

        return key_dic.get(tool.lower(), '')

    def trans_type(self, vultype):
        key_dic = {
            'SQL Injection': u'SQL注入,泄露信息',
            'Arbitrary File Download': u'任意文件下载,泄露信息',
            'Arbitrary File Deletion': u'任意文件删除',
            'Login Bypass': u'登录绕过,权限绕过,非授权访问',
            'File Upload': u'文件上传导致代码执行',
        }

        return key_dic.get(vultype, '')


if __name__ == "__main__":
    app = App()
    app.MainLoop()
