#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.module.event('NICK')
@sopel.modulerule('.*')
def parse_event_NICK(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('QUIT')
@sopel.modulerule('.*')
def parse_event_QUIT(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('PART')
def parse_event_PART(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('MODE')
@sopel.modulerule('.*')
def parse_event_MODE(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('KICK')
@sopel.modulerule('.*')
def parse_event_KICK(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('JOIN')
@sopel.modulerule('.*')
def parse_event_JOIN(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('INVITE')
@sopel.modulerule('.*')
def parse_event_INVITE(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.module.event('TOPIC')
@sopel.modulerule('.*')
def parse_event_TOPIC(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WELCOME = '001'
@sopel.module.event('001')
@sopel.modulerule('.*')
def parse_event_001(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_YOURHOST = '002'
@sopel.module.event('002')
@sopel.modulerule('.*')
def parse_event_002(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_CREATED = '003'
@sopel.module.event('003')
@sopel.modulerule('.*')
def parse_event_003(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MYINFO = '004'
@sopel.module.event('004')
@sopel.modulerule('.*')
def parse_event_004(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_BOUNCE = '005'
@sopel.module.event('005')
@sopel.modulerule('.*')
def parse_event_005(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ISUPPORT = '005'
@sopel.module.event('005')
@sopel.modulerule('.*')
def parse_event_005b(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACELINK = '200'
@sopel.module.event('200')
@sopel.modulerule('.*')
def parse_event_200(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACECONNECTING = '201'
@sopel.module.event('201')
@sopel.modulerule('.*')
def parse_event_201(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEHANDSHAKE = '202'
@sopel.module.event('202')
@sopel.modulerule('.*')
def parse_event_202(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEUNKNOWN = '203'
@sopel.module.event('203')
@sopel.modulerule('.*')
def parse_event_203(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEOPERATOR = '204'
@sopel.module.event('204')
@sopel.modulerule('.*')
def parse_event_204(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEUSER = '205'
@sopel.module.event('205')
@sopel.modulerule('.*')
def parse_event_205(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACESERVER = '206'
@sopel.module.event('206')
@sopel.modulerule('.*')
def parse_event_206(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACESERVICE = '207'
@sopel.module.event('207')
@sopel.modulerule('.*')
def parse_event_207(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACENEWTYPE = '208'
@sopel.module.event('208')
@sopel.modulerule('.*')
def parse_event_208(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACECLASS = '209'
@sopel.module.event('209')
@sopel.modulerule('.*')
def parse_event_209(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACERECONNECT = '210'
@sopel.module.event('210')
@sopel.modulerule('.*')
def parse_event_210(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSLINKINFO = '211'
@sopel.module.event('211')
@sopel.modulerule('.*')
def parse_event_211(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSCOMMANDS = '212'
@sopel.module.event('212')
@sopel.modulerule('.*')
def parse_event_212(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSCLINE = '213'
@sopel.module.event('213')
@sopel.modulerule('.*')
def parse_event_213(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSNLINE = '214'
@sopel.module.event('214')
@sopel.modulerule('.*')
def parse_event_214(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSILINE = '215'
@sopel.module.event('215')
@sopel.modulerule('.*')
def parse_event_215(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSKLINE = '216'
@sopel.module.event('216')
@sopel.modulerule('.*')
def parse_event_216(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSYLINE = '218'
@sopel.module.event('218')
@sopel.modulerule('.*')
def parse_event_218(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFSTATS = '219'
@sopel.module.event('219')
@sopel.modulerule('.*')
def parse_event_219(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_UMODEIS = '221'
@sopel.module.event('221')
@sopel.modulerule('.*')
def parse_event_221(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SERVLIST = '234'
@sopel.module.event('234')
@sopel.modulerule('.*')
def parse_event_234(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SERVLISTEND = '235'
@sopel.module.event('235')
@sopel.modulerule('.*')
def parse_event_235(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSLLINE = '241'
@sopel.module.event('241')
@sopel.modulerule('.*')
def parse_event_241(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSUPTIME = '242'
@sopel.module.event('242')
@sopel.modulerule('.*')
def parse_event_242(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSOLINE = '243'
@sopel.module.event('243')
@sopel.modulerule('.*')
def parse_event_243(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSHLINE = '244'
@sopel.module.event('244')
@sopel.modulerule('.*')
def parse_event_244(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERCLIENT = '251'
@sopel.module.event('251')
@sopel.modulerule('.*')
def parse_event_251(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSEROP = '252'
@sopel.module.event('252')
@sopel.modulerule('.*')
def parse_event_252(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERUNKNOWN = '253'
@sopel.module.event('253')
@sopel.modulerule('.*')
def parse_event_253(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERCHANNELS = '254'
@sopel.module.event('254')
@sopel.modulerule('.*')
def parse_event_254(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERME = '255'
@sopel.module.event('255')
@sopel.modulerule('.*')
def parse_event_255(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINME = '256'
@sopel.module.event('256')
@sopel.modulerule('.*')
def parse_event_256(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINLOC1 = '257'
@sopel.module.event('257')
@sopel.modulerule('.*')
def parse_event_257(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINLOC2 = '258'
@sopel.module.event('258')
@sopel.modulerule('.*')
def parse_event_258(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINEMAIL = '259'
@sopel.module.event('259')
@sopel.modulerule('.*')
def parse_event_259(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACELOG = '261'
@sopel.module.event('261')
@sopel.modulerule('.*')
def parse_event_261(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEEND = '262'
@sopel.module.event('262')
@sopel.modulerule('.*')
def parse_event_262(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRYAGAIN = '263'
@sopel.module.event('263')
@sopel.modulerule('.*')
def parse_event_263(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NONE = '300'
@sopel.module.event('300')
@sopel.modulerule('.*')
def parse_event_300(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_AWAY = '301'
@sopel.module.event('301')
@sopel.modulerule('.*')
def parse_event_301(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_USERHOST = '302'
@sopel.module.event('302')
@sopel.modulerule('.*')
def parse_event_302(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ISON = '303'
@sopel.module.event('303')
@sopel.modulerule('.*')
def parse_event_303(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_UNAWAY = '305'
@sopel.module.event('305')
@sopel.modulerule('.*')
def parse_event_305(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NOWAWAY = '306'
@sopel.module.event('306')
@sopel.modulerule('.*')
def parse_event_306(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISUSER = '311'
@sopel.module.event('311')
@sopel.modulerule('.*')
def parse_event_311(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISSERVER = '312'
@sopel.module.event('312')
@sopel.modulerule('.*')
def parse_event_312(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISOPERATOR = '313'
@sopel.module.event('313')
@sopel.modulerule('.*')
def parse_event_313(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOWASUSER = '314'
@sopel.module.event('314')
@sopel.modulerule('.*')
def parse_event_314(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFWHO = '315'
@sopel.module.event('315')
@sopel.modulerule('.*')
def parse_event_315(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISIDLE = '317'
@sopel.module.event('317')
@sopel.modulerule('.*')
def parse_event_317(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFWHOIS = '318'
@sopel.module.event('318')
@sopel.modulerule('.*')
def parse_event_318(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISCHANNELS = '319'
@sopel.module.event('319')
@sopel.modulerule('.*')
def parse_event_319(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LISTSTART = '321'
@sopel.module.event('321')
@sopel.modulerule('.*')
def parse_event_321(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LIST = '322'
@sopel.module.event('322')
@sopel.modulerule('.*')
def parse_event_322(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LISTEND = '323'
@sopel.module.event('323')
@sopel.modulerule('.*')
def parse_event_323(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_CHANNELMODEIS = '324'
@sopel.module.event('324')
@sopel.modulerule('.*')
def parse_event_324(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_UNIQOPIS = '325'
@sopel.module.event('325')
@sopel.modulerule('.*')
def parse_event_325(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NOTOPIC = '331'
@sopel.module.event('331')
@sopel.modulerule('.*')
def parse_event_331(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TOPIC = '332'
@sopel.module.event('332')
@sopel.modulerule('.*')
def parse_event_332(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_INVITING = '341'
@sopel.module.event('341')
@sopel.modulerule('.*')
def parse_event_341(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SUMMONING = '342'
@sopel.module.event('342')
@sopel.modulerule('.*')
def parse_event_342(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_INVITELIST = '346'
@sopel.module.event('346')
@sopel.modulerule('.*')
def parse_event_346(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFINVITELIST = '347'
@sopel.module.event('347')
@sopel.modulerule('.*')
def parse_event_347(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_EXCEPTLIST = '348'
@sopel.module.event('348')
@sopel.modulerule('.*')
def parse_event_348(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFEXCEPTLIST = '349'
@sopel.module.event('349')
@sopel.modulerule('.*')
def parse_event_349(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_VERSION = '351'
@sopel.module.event('351')
@sopel.modulerule('.*')
def parse_event_351(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOREPLY = '352'
@sopel.module.event('352')
@sopel.modulerule('.*')
def parse_event_352(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NAMREPLY = '353'
@sopel.module.event('353')
@sopel.modulerule('.*')
def parse_event_353(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOSPCRPL = '354'
@sopel.module.event('354')
@sopel.modulerule('.*')
def parse_event_354(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LINKS = '364'
@sopel.module.event('364')
@sopel.modulerule('.*')
def parse_event_364(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFLINKS = '365'
@sopel.module.event('365')
@sopel.modulerule('.*')
def parse_event_365(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFNAMES = '366'
@sopel.module.event('366')
@sopel.modulerule('.*')
def parse_event_366(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_BANLIST = '367'
@sopel.module.event('367')
@sopel.modulerule('.*')
def parse_event_367(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFBANLIST = '368'
@sopel.module.event('368')
@sopel.modulerule('.*')
def parse_event_368(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFWHOWAS = '369'
@sopel.module.event('369')
@sopel.modulerule('.*')
def parse_event_369(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_INFO = '371'
@sopel.module.event('371')
@sopel.modulerule('.*')
def parse_event_371(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MOTD = '372'
@sopel.module.event('372')
@sopel.modulerule('.*')
def parse_event_372(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFINFO = '374'
@sopel.module.event('374')
@sopel.modulerule('.*')
def parse_event_374(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MOTDSTART = '375'
@sopel.module.event('375')
@sopel.modulerule('.*')
def parse_event_375(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFMOTD = '376'
@sopel.module.event('376')
@sopel.modulerule('.*')
def parse_event_376(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_YOUREOPER = '381'
@sopel.module.event('381')
@sopel.modulerule('.*')
def parse_event_381(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_REHASHING = '382'
@sopel.module.event('382')
@sopel.modulerule('.*')
def parse_event_382(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_YOURESERVICE = '383'
@sopel.module.event('383')
@sopel.modulerule('.*')
def parse_event_383(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TIME = '391'
@sopel.module.event('391')
@sopel.modulerule('.*')
def parse_event_391(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_USERSSTART = '392'
@sopel.module.event('392')
@sopel.modulerule('.*')
def parse_event_392(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_USERS = '393'
@sopel.module.event('393')
@sopel.modulerule('.*')
def parse_event_393(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFUSERS = '394'
@sopel.module.event('394')
@sopel.modulerule('.*')
def parse_event_394(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NOUSERS = '395'
@sopel.module.event('395')
@sopel.modulerule('.*')
def parse_event_395(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHNICK = '401'
@sopel.module.event('401')
@sopel.modulerule('.*')
def parse_event_401(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHSERVER = '402'
@sopel.module.event('402')
@sopel.modulerule('.*')
def parse_event_402(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHCHANNEL = '403'
@sopel.module.event('403')
@sopel.modulerule('.*')
def parse_event_403(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CANNOTSENDTOCHAN = '404'
@sopel.module.event('404')
@sopel.modulerule('.*')
def parse_event_404(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_TOOMANYCHANNELS = '405'
@sopel.module.event('405')
@sopel.modulerule('.*')
def parse_event_405(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_WASNOSUCHNICK = '406'
@sopel.module.event('406')
@sopel.modulerule('.*')
def parse_event_406(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_TOOMANYTARGETS = '407'
@sopel.module.event('407')
@sopel.modulerule('.*')
def parse_event_407(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHSERVICE = '408'
@sopel.module.event('408')
@sopel.modulerule('.*')
def parse_event_408(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOORIGIN = '409'
@sopel.module.event('409')
@sopel.modulerule('.*')
def parse_event_409(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_INVALIDCAPCMD = '410'
@sopel.module.event('410')
@sopel.modulerule('.*')
def parse_event_410(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NORECIPIENT = '411'
@sopel.module.event('411')
@sopel.modulerule('.*')
def parse_event_411(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTEXTTOSEND = '412'
@sopel.module.event('412')
@sopel.modulerule('.*')
def parse_event_412(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTOPLEVEL = '413'
@sopel.module.event('413')
@sopel.modulerule('.*')
def parse_event_413(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_WILDTOPLEVEL = '414'
@sopel.module.event('414')
@sopel.modulerule('.*')
def parse_event_414(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BADMASK = '415'
@sopel.module.event('415')
@sopel.modulerule('.*')
def parse_event_415(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNKNOWNCOMMAND = '421'
@sopel.module.event('421')
@sopel.modulerule('.*')
def parse_event_421(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOMOTD = '422'
@sopel.module.event('422')
@sopel.modulerule('.*')
def parse_event_422(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOADMININFO = '423'
@sopel.module.event('423')
@sopel.modulerule('.*')
def parse_event_423(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_FILEERROR = '424'
@sopel.module.event('424')
@sopel.modulerule('.*')
def parse_event_424(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NONICKNAMEGIVEN = '431'
@sopel.module.event('431')
@sopel.modulerule('.*')
def parse_event_431(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_ERRONEUSNICKNAME = '432'
@sopel.module.event('432')
@sopel.modulerule('.*')
def parse_event_432(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NICKNAMEINUSE = '433'
@sopel.module.event('433')
@sopel.modulerule('.*')
def parse_event_433(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NICKCOLLISION = '436'
@sopel.module.event('436')
@sopel.modulerule('.*')
def parse_event_436(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNAVAILRESOURCE = '437'
@sopel.module.event('437')
@sopel.modulerule('.*')
def parse_event_437(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERNOTINCHANNEL = '441'
@sopel.module.event('441')
@sopel.modulerule('.*')
def parse_event_441(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTONCHANNEL = '442'
@sopel.module.event('442')
@sopel.modulerule('.*')
def parse_event_442(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERONCHANNEL = '443'
@sopel.module.event('443')
@sopel.modulerule('.*')
def parse_event_443(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOLOGIN = '444'
@sopel.module.event('444')
@sopel.modulerule('.*')
def parse_event_444(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SUMMONDISABLED = '445'
@sopel.module.event('445')
@sopel.modulerule('.*')
def parse_event_445(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERSDISABLED = '446'
@sopel.module.event('446')
@sopel.modulerule('.*')
def parse_event_446(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTREGISTERED = '451'
@sopel.module.event('451')
@sopel.modulerule('.*')
def parse_event_451(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NEEDMOREPARAMS = '461'
@sopel.module.event('461')
@sopel.modulerule('.*')
def parse_event_461(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_ALREADYREGISTRED = '462'
@sopel.module.event('462')
@sopel.modulerule('.*')
def parse_event_462(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOPERMFORHOST = '463'
@sopel.module.event('463')
@sopel.modulerule('.*')
def parse_event_463(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_PASSWDMISMATCH = '464'
@sopel.module.event('464')
@sopel.modulerule('.*')
def parse_event_464(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_YOUREBANNEDCREEP = '465'
@sopel.module.event('465')
@sopel.modulerule('.*')
def parse_event_465(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_YOUWILLBEBANNED = '466'
@sopel.module.event('466')
@sopel.modulerule('.*')
def parse_event_466(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYSET = '467'
@sopel.module.event('467')
@sopel.modulerule('.*')
def parse_event_467(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CHANNELISFULL = '471'
@sopel.module.event('471')
@sopel.modulerule('.*')
def parse_event_471(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNKNOWNMODE = '472'
@sopel.module.event('472')
@sopel.modulerule('.*')
def parse_event_472(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_INVITEONLYCHAN = '473'
@sopel.module.event('473')
@sopel.modulerule('.*')
def parse_event_473(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BANNEDFROMCHAN = '474'
@sopel.module.event('474')
@sopel.modulerule('.*')
def parse_event_474(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BADCHANNELKEY = '475'
@sopel.module.event('475')
@sopel.modulerule('.*')
def parse_event_475(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BADCHANMASK = '476'
@sopel.module.event('476')
@sopel.modulerule('.*')
def parse_event_476(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOCHANMODES = '477'
@sopel.module.event('477')
@sopel.modulerule('.*')
def parse_event_477(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BANLISTFULL = '478'
@sopel.module.event('478')
@sopel.modulerule('.*')
def parse_event_478(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOPRIVILEGES = '481'
@sopel.module.event('481')
@sopel.modulerule('.*')
def parse_event_481(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CHANOPRIVSNEEDED = '482'
@sopel.module.event('482')
@sopel.modulerule('.*')
def parse_event_482(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CANTKILLSERVER = '483'
@sopel.module.event('483')
@sopel.modulerule('.*')
def parse_event_483(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_RESTRICTED = '484'
@sopel.module.event('484')
@sopel.modulerule('.*')
def parse_event_484(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNIQOPPRIVSNEEDED = '485'
@sopel.module.event('485')
@sopel.modulerule('.*')
def parse_event_485(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOOPERHOST = '491'
@sopel.module.event('491')
@sopel.modulerule('.*')
def parse_event_491(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UMODEUNKNOWNFLAG = '501'
@sopel.module.event('501')
@sopel.modulerule('.*')
def parse_event_501(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERSDONTMATCH = '502'
@sopel.module.event('502')
@sopel.modulerule('.*')
def parse_event_502(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STARTTLS = '670'
@sopel.module.event('670')
@sopel.modulerule('.*')
def parse_event_670(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_STARTTLS = '691'
@sopel.module.event('691')
@sopel.modulerule('.*')
def parse_event_691(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MONONLINE = '730'
@sopel.module.event('730')
@sopel.modulerule('.*')
def parse_event_730(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MONOFFLINE = '731'
@sopel.module.event('731')
@sopel.modulerule('.*')
def parse_event_731(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MONLIST = '732'
@sopel.module.event('732')
@sopel.modulerule('.*')
def parse_event_732(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFMONLIST = '733'
@sopel.module.event('733')
@sopel.modulerule('.*')
def parse_event_733(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_MONLISTFULL = '734'
@sopel.module.event('734')
@sopel.modulerule('.*')
def parse_event_734(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISKEYVALUE = '760'
@sopel.module.event('760')
@sopel.modulerule('.*')
def parse_event_760(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_KEYVALUE = '761'
@sopel.module.event('761')
@sopel.modulerule('.*')
def parse_event_761(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_METADATAEND = '762'
@sopel.module.event('762')
@sopel.modulerule('.*')
def parse_event_762(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_METADATALIMIT = '764'
@sopel.module.event('764')
@sopel.modulerule('.*')
def parse_event_764(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_TARGETINVALID = '765'
@sopel.module.event('765')
@sopel.modulerule('.*')
def parse_event_765(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOMATCHINGKEY = '766'
@sopel.module.event('766')
@sopel.modulerule('.*')
def parse_event_766(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYINVALID = '767'
@sopel.module.event('767')
@sopel.modulerule('.*')
def parse_event_767(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYNOTSET = '768'
@sopel.module.event('768')
@sopel.modulerule('.*')
def parse_event_768(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYNOPERMISSION = '769'
@sopel.module.event('769')
@sopel.modulerule('.*')
def parse_event_769(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LOGGEDIN = '900'
@sopel.module.event('900')
@sopel.modulerule('.*')
def parse_event_900(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LOGGEDOUT = '901'
@sopel.module.event('901')
@sopel.modulerule('.*')
def parse_event_901(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NICKLOCKED = '902'
@sopel.module.event('902')
@sopel.modulerule('.*')
def parse_event_902(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SASLSUCCESS = '903'
@sopel.module.event('903')
@sopel.modulerule('.*')
def parse_event_903(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLFAIL = '904'
@sopel.module.event('904')
@sopel.modulerule('.*')
def parse_event_904(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLTOOLONG = '905'
@sopel.module.event('905')
@sopel.modulerule('.*')
def parse_event_905(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLABORTED = '906'
@sopel.module.event('906')
@sopel.modulerule('.*')
def parse_event_906(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLALREADY = '907'
@sopel.module.event('907')
@sopel.modulerule('.*')
def parse_event_907(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SASLMECHS = '908'
@sopel.module.event('908')
@sopel.modulerule('.*')
def parse_event_908(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))
