# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sublime
import sublime_plugin
import re


def load_data():
    f = sublime.load_binary_resource("/".join(("Packages", __package__, "typography-data.tsv")))
    lines = f.decode("utf-8").strip().split("\n")
    data = []
    names = {}
    code = 0
    for line in lines:
        code += 1
        if line[0] == "#":
            continue
        character, name = line.strip().split("\t")
        names[code] = name
        name = name.title()
        data.append([code, character, name, "{} {}".format(character, name, code)])

    return data


class SelectTypographyCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        window = self.view.window()
        data = load_data()
        items = [t[-1] for t in data]

        def callback(selection):
            if selection >= 0:
                character = data[selection][1]
                self.view.run_command("insert", {"characters": character})

        window.show_quick_panel(items, callback)
