# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

from sopel_modules.SpiceBot_SBTools import github_dict


@sopel.module.nickname_commands('help', 'docs', 'wiki')
def bot_command_owners(bot, trigger):
    bot.osd(["IRC Modules Repository", str(github_dict["url_main"] + github_dict["repo_owner"] + "/" + github_dict["repo_name"] + github_dict["url_path_wiki"])])
