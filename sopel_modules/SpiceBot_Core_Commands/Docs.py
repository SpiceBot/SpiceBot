# coding=utf-8

from __future__ import unicode_literals, absolute_import, division, print_function

import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@SpiceBot.prerun('nickname')
@sopel.module.nickname_commands('help', 'docs', 'wiki')
def bot_command_docs(bot, trigger, botcom):
    sb_git_url = str(
                    SpiceBot.github_dict["url_main"] +
                    SpiceBot.github_dict["repo_owner"] + "/" +
                    SpiceBot.github_dict["repo_name"] +
                    SpiceBot.github_dict["url_path_wiki"]
                    )
    bot.osd(["IRC Modules Repository", sb_git_url])
