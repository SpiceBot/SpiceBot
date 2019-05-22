#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

# sopel imports
import sopel.module

import sopel_modules.SpiceBot as SpiceBot


@sopel.moduleevent('NICK')
@sopel.modulerule('.*')
def parse_event_NICK(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('QUIT')
@sopel.modulerule('.*')
def parse_event_QUIT(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('PART')
def parse_event_PART(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('MODE')
@sopel.modulerule('.*')
def parse_event_MODE(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('KICK')
@sopel.modulerule('.*')
def parse_event_KICK(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('JOIN')
@sopel.modulerule('.*')
def parse_event_JOIN(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('INVITE')
@sopel.modulerule('.*')
def parse_event_INVITE(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


@sopel.moduleevent('TOPIC')
@sopel.modulerule('.*')
def parse_event_TOPIC(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WELCOME = '001'
@sopel.moduleevent('001')
@sopel.modulerule('.*')
def parse_event_001(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_YOURHOST = '002'
@sopel.moduleevent('002')
@sopel.modulerule('.*')
def parse_event_002(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_CREATED = '003'
@sopel.moduleevent('003')
@sopel.modulerule('.*')
def parse_event_003(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MYINFO = '004'
@sopel.moduleevent('004')
@sopel.modulerule('.*')
def parse_event_004(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_BOUNCE = '005'
@sopel.moduleevent('005')
@sopel.modulerule('.*')
def parse_event_005(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ISUPPORT = '005'
@sopel.moduleevent('005')
@sopel.modulerule('.*')
def parse_event_005b(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACELINK = '200'
@sopel.moduleevent('200')
@sopel.modulerule('.*')
def parse_event_200(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACECONNECTING = '201'
@sopel.moduleevent('201')
@sopel.modulerule('.*')
def parse_event_201(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEHANDSHAKE = '202'
@sopel.moduleevent('202')
@sopel.modulerule('.*')
def parse_event_202(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEUNKNOWN = '203'
@sopel.moduleevent('203')
@sopel.modulerule('.*')
def parse_event_203(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEOPERATOR = '204'
@sopel.moduleevent('204')
@sopel.modulerule('.*')
def parse_event_204(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEUSER = '205'
@sopel.moduleevent('205')
@sopel.modulerule('.*')
def parse_event_205(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACESERVER = '206'
@sopel.moduleevent('206')
@sopel.modulerule('.*')
def parse_event_206(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACESERVICE = '207'
@sopel.moduleevent('207')
@sopel.modulerule('.*')
def parse_event_207(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACENEWTYPE = '208'
@sopel.moduleevent('208')
@sopel.modulerule('.*')
def parse_event_208(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACECLASS = '209'
@sopel.moduleevent('209')
@sopel.modulerule('.*')
def parse_event_209(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACERECONNECT = '210'
@sopel.moduleevent('210')
@sopel.modulerule('.*')
def parse_event_210(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSLINKINFO = '211'
@sopel.moduleevent('211')
@sopel.modulerule('.*')
def parse_event_211(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSCOMMANDS = '212'
@sopel.moduleevent('212')
@sopel.modulerule('.*')
def parse_event_212(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSCLINE = '213'
@sopel.moduleevent('213')
@sopel.modulerule('.*')
def parse_event_213(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSNLINE = '214'
@sopel.moduleevent('214')
@sopel.modulerule('.*')
def parse_event_214(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSILINE = '215'
@sopel.moduleevent('215')
@sopel.modulerule('.*')
def parse_event_215(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSKLINE = '216'
@sopel.moduleevent('216')
@sopel.modulerule('.*')
def parse_event_216(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSYLINE = '218'
@sopel.moduleevent('218')
@sopel.modulerule('.*')
def parse_event_218(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFSTATS = '219'
@sopel.moduleevent('219')
@sopel.modulerule('.*')
def parse_event_219(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_UMODEIS = '221'
@sopel.moduleevent('221')
@sopel.modulerule('.*')
def parse_event_221(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SERVLIST = '234'
@sopel.moduleevent('234')
@sopel.modulerule('.*')
def parse_event_234(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SERVLISTEND = '235'
@sopel.moduleevent('235')
@sopel.modulerule('.*')
def parse_event_235(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSLLINE = '241'
@sopel.moduleevent('241')
@sopel.modulerule('.*')
def parse_event_241(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSUPTIME = '242'
@sopel.moduleevent('242')
@sopel.modulerule('.*')
def parse_event_242(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSOLINE = '243'
@sopel.moduleevent('243')
@sopel.modulerule('.*')
def parse_event_243(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STATSHLINE = '244'
@sopel.moduleevent('244')
@sopel.modulerule('.*')
def parse_event_244(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERCLIENT = '251'
@sopel.moduleevent('251')
@sopel.modulerule('.*')
def parse_event_251(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSEROP = '252'
@sopel.moduleevent('252')
@sopel.modulerule('.*')
def parse_event_252(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERUNKNOWN = '253'
@sopel.moduleevent('253')
@sopel.modulerule('.*')
def parse_event_253(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERCHANNELS = '254'
@sopel.moduleevent('254')
@sopel.modulerule('.*')
def parse_event_254(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LUSERME = '255'
@sopel.moduleevent('255')
@sopel.modulerule('.*')
def parse_event_255(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINME = '256'
@sopel.moduleevent('256')
@sopel.modulerule('.*')
def parse_event_256(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINLOC1 = '257'
@sopel.moduleevent('257')
@sopel.modulerule('.*')
def parse_event_257(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINLOC2 = '258'
@sopel.moduleevent('258')
@sopel.modulerule('.*')
def parse_event_258(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ADMINEMAIL = '259'
@sopel.moduleevent('259')
@sopel.modulerule('.*')
def parse_event_259(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACELOG = '261'
@sopel.moduleevent('261')
@sopel.modulerule('.*')
def parse_event_261(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRACEEND = '262'
@sopel.moduleevent('262')
@sopel.modulerule('.*')
def parse_event_262(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TRYAGAIN = '263'
@sopel.moduleevent('263')
@sopel.modulerule('.*')
def parse_event_263(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NONE = '300'
@sopel.moduleevent('300')
@sopel.modulerule('.*')
def parse_event_300(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_AWAY = '301'
@sopel.moduleevent('301')
@sopel.modulerule('.*')
def parse_event_301(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_USERHOST = '302'
@sopel.moduleevent('302')
@sopel.modulerule('.*')
def parse_event_302(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ISON = '303'
@sopel.moduleevent('303')
@sopel.modulerule('.*')
def parse_event_303(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_UNAWAY = '305'
@sopel.moduleevent('305')
@sopel.modulerule('.*')
def parse_event_305(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NOWAWAY = '306'
@sopel.moduleevent('306')
@sopel.modulerule('.*')
def parse_event_306(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISUSER = '311'
@sopel.moduleevent('311')
@sopel.modulerule('.*')
def parse_event_311(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISSERVER = '312'
@sopel.moduleevent('312')
@sopel.modulerule('.*')
def parse_event_312(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISOPERATOR = '313'
@sopel.moduleevent('313')
@sopel.modulerule('.*')
def parse_event_313(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOWASUSER = '314'
@sopel.moduleevent('314')
@sopel.modulerule('.*')
def parse_event_314(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFWHO = '315'
@sopel.moduleevent('315')
@sopel.modulerule('.*')
def parse_event_315(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISIDLE = '317'
@sopel.moduleevent('317')
@sopel.modulerule('.*')
def parse_event_317(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFWHOIS = '318'
@sopel.moduleevent('318')
@sopel.modulerule('.*')
def parse_event_318(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISCHANNELS = '319'
@sopel.moduleevent('319')
@sopel.modulerule('.*')
def parse_event_319(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LISTSTART = '321'
@sopel.moduleevent('321')
@sopel.modulerule('.*')
def parse_event_321(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LIST = '322'
@sopel.moduleevent('322')
@sopel.modulerule('.*')
def parse_event_322(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LISTEND = '323'
@sopel.moduleevent('323')
@sopel.modulerule('.*')
def parse_event_323(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_CHANNELMODEIS = '324'
@sopel.moduleevent('324')
@sopel.modulerule('.*')
def parse_event_324(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_UNIQOPIS = '325'
@sopel.moduleevent('325')
@sopel.modulerule('.*')
def parse_event_325(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NOTOPIC = '331'
@sopel.moduleevent('331')
@sopel.modulerule('.*')
def parse_event_331(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TOPIC = '332'
@sopel.moduleevent('332')
@sopel.modulerule('.*')
def parse_event_332(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_INVITING = '341'
@sopel.moduleevent('341')
@sopel.modulerule('.*')
def parse_event_341(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SUMMONING = '342'
@sopel.moduleevent('342')
@sopel.modulerule('.*')
def parse_event_342(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_INVITELIST = '346'
@sopel.moduleevent('346')
@sopel.modulerule('.*')
def parse_event_346(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFINVITELIST = '347'
@sopel.moduleevent('347')
@sopel.modulerule('.*')
def parse_event_347(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_EXCEPTLIST = '348'
@sopel.moduleevent('348')
@sopel.modulerule('.*')
def parse_event_348(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFEXCEPTLIST = '349'
@sopel.moduleevent('349')
@sopel.modulerule('.*')
def parse_event_349(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_VERSION = '351'
@sopel.moduleevent('351')
@sopel.modulerule('.*')
def parse_event_351(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOREPLY = '352'
@sopel.moduleevent('352')
@sopel.modulerule('.*')
def parse_event_352(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NAMREPLY = '353'
@sopel.moduleevent('353')
@sopel.modulerule('.*')
def parse_event_353(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOSPCRPL = '354'
@sopel.moduleevent('354')
@sopel.modulerule('.*')
def parse_event_354(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LINKS = '364'
@sopel.moduleevent('364')
@sopel.modulerule('.*')
def parse_event_364(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFLINKS = '365'
@sopel.moduleevent('365')
@sopel.modulerule('.*')
def parse_event_365(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFNAMES = '366'
@sopel.moduleevent('366')
@sopel.modulerule('.*')
def parse_event_366(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_BANLIST = '367'
@sopel.moduleevent('367')
@sopel.modulerule('.*')
def parse_event_367(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFBANLIST = '368'
@sopel.moduleevent('368')
@sopel.modulerule('.*')
def parse_event_368(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFWHOWAS = '369'
@sopel.moduleevent('369')
@sopel.modulerule('.*')
def parse_event_369(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_INFO = '371'
@sopel.moduleevent('371')
@sopel.modulerule('.*')
def parse_event_371(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MOTD = '372'
@sopel.moduleevent('372')
@sopel.modulerule('.*')
def parse_event_372(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFINFO = '374'
@sopel.moduleevent('374')
@sopel.modulerule('.*')
def parse_event_374(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MOTDSTART = '375'
@sopel.moduleevent('375')
@sopel.modulerule('.*')
def parse_event_375(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFMOTD = '376'
@sopel.moduleevent('376')
@sopel.modulerule('.*')
def parse_event_376(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_YOUREOPER = '381'
@sopel.moduleevent('381')
@sopel.modulerule('.*')
def parse_event_381(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_REHASHING = '382'
@sopel.moduleevent('382')
@sopel.modulerule('.*')
def parse_event_382(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_YOURESERVICE = '383'
@sopel.moduleevent('383')
@sopel.modulerule('.*')
def parse_event_383(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_TIME = '391'
@sopel.moduleevent('391')
@sopel.modulerule('.*')
def parse_event_391(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_USERSSTART = '392'
@sopel.moduleevent('392')
@sopel.modulerule('.*')
def parse_event_392(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_USERS = '393'
@sopel.moduleevent('393')
@sopel.modulerule('.*')
def parse_event_393(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFUSERS = '394'
@sopel.moduleevent('394')
@sopel.modulerule('.*')
def parse_event_394(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_NOUSERS = '395'
@sopel.moduleevent('395')
@sopel.modulerule('.*')
def parse_event_395(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHNICK = '401'
@sopel.moduleevent('401')
@sopel.modulerule('.*')
def parse_event_401(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHSERVER = '402'
@sopel.moduleevent('402')
@sopel.modulerule('.*')
def parse_event_402(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHCHANNEL = '403'
@sopel.moduleevent('403')
@sopel.modulerule('.*')
def parse_event_403(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CANNOTSENDTOCHAN = '404'
@sopel.moduleevent('404')
@sopel.modulerule('.*')
def parse_event_404(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_TOOMANYCHANNELS = '405'
@sopel.moduleevent('405')
@sopel.modulerule('.*')
def parse_event_405(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_WASNOSUCHNICK = '406'
@sopel.moduleevent('406')
@sopel.modulerule('.*')
def parse_event_406(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_TOOMANYTARGETS = '407'
@sopel.moduleevent('407')
@sopel.modulerule('.*')
def parse_event_407(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOSUCHSERVICE = '408'
@sopel.moduleevent('408')
@sopel.modulerule('.*')
def parse_event_408(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOORIGIN = '409'
@sopel.moduleevent('409')
@sopel.modulerule('.*')
def parse_event_409(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_INVALIDCAPCMD = '410'
@sopel.moduleevent('410')
@sopel.modulerule('.*')
def parse_event_410(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NORECIPIENT = '411'
@sopel.moduleevent('411')
@sopel.modulerule('.*')
def parse_event_411(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTEXTTOSEND = '412'
@sopel.moduleevent('412')
@sopel.modulerule('.*')
def parse_event_412(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTOPLEVEL = '413'
@sopel.moduleevent('413')
@sopel.modulerule('.*')
def parse_event_413(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_WILDTOPLEVEL = '414'
@sopel.moduleevent('414')
@sopel.modulerule('.*')
def parse_event_414(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BADMASK = '415'
@sopel.moduleevent('415')
@sopel.modulerule('.*')
def parse_event_415(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNKNOWNCOMMAND = '421'
@sopel.moduleevent('421')
@sopel.modulerule('.*')
def parse_event_421(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOMOTD = '422'
@sopel.moduleevent('422')
@sopel.modulerule('.*')
def parse_event_422(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOADMININFO = '423'
@sopel.moduleevent('423')
@sopel.modulerule('.*')
def parse_event_423(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_FILEERROR = '424'
@sopel.moduleevent('424')
@sopel.modulerule('.*')
def parse_event_424(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NONICKNAMEGIVEN = '431'
@sopel.moduleevent('431')
@sopel.modulerule('.*')
def parse_event_431(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_ERRONEUSNICKNAME = '432'
@sopel.moduleevent('432')
@sopel.modulerule('.*')
def parse_event_432(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NICKNAMEINUSE = '433'
@sopel.moduleevent('433')
@sopel.modulerule('.*')
def parse_event_433(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NICKCOLLISION = '436'
@sopel.moduleevent('436')
@sopel.modulerule('.*')
def parse_event_436(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNAVAILRESOURCE = '437'
@sopel.moduleevent('437')
@sopel.modulerule('.*')
def parse_event_437(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERNOTINCHANNEL = '441'
@sopel.moduleevent('441')
@sopel.modulerule('.*')
def parse_event_441(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTONCHANNEL = '442'
@sopel.moduleevent('442')
@sopel.modulerule('.*')
def parse_event_442(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERONCHANNEL = '443'
@sopel.moduleevent('443')
@sopel.modulerule('.*')
def parse_event_443(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOLOGIN = '444'
@sopel.moduleevent('444')
@sopel.modulerule('.*')
def parse_event_444(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SUMMONDISABLED = '445'
@sopel.moduleevent('445')
@sopel.modulerule('.*')
def parse_event_445(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERSDISABLED = '446'
@sopel.moduleevent('446')
@sopel.modulerule('.*')
def parse_event_446(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOTREGISTERED = '451'
@sopel.moduleevent('451')
@sopel.modulerule('.*')
def parse_event_451(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NEEDMOREPARAMS = '461'
@sopel.moduleevent('461')
@sopel.modulerule('.*')
def parse_event_461(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_ALREADYREGISTRED = '462'
@sopel.moduleevent('462')
@sopel.modulerule('.*')
def parse_event_462(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOPERMFORHOST = '463'
@sopel.moduleevent('463')
@sopel.modulerule('.*')
def parse_event_463(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_PASSWDMISMATCH = '464'
@sopel.moduleevent('464')
@sopel.modulerule('.*')
def parse_event_464(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_YOUREBANNEDCREEP = '465'
@sopel.moduleevent('465')
@sopel.modulerule('.*')
def parse_event_465(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_YOUWILLBEBANNED = '466'
@sopel.moduleevent('466')
@sopel.modulerule('.*')
def parse_event_466(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYSET = '467'
@sopel.moduleevent('467')
@sopel.modulerule('.*')
def parse_event_467(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CHANNELISFULL = '471'
@sopel.moduleevent('471')
@sopel.modulerule('.*')
def parse_event_471(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNKNOWNMODE = '472'
@sopel.moduleevent('472')
@sopel.modulerule('.*')
def parse_event_472(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_INVITEONLYCHAN = '473'
@sopel.moduleevent('473')
@sopel.modulerule('.*')
def parse_event_473(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BANNEDFROMCHAN = '474'
@sopel.moduleevent('474')
@sopel.modulerule('.*')
def parse_event_474(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BADCHANNELKEY = '475'
@sopel.moduleevent('475')
@sopel.modulerule('.*')
def parse_event_475(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BADCHANMASK = '476'
@sopel.moduleevent('476')
@sopel.modulerule('.*')
def parse_event_476(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOCHANMODES = '477'
@sopel.moduleevent('477')
@sopel.modulerule('.*')
def parse_event_477(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_BANLISTFULL = '478'
@sopel.moduleevent('478')
@sopel.modulerule('.*')
def parse_event_478(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOPRIVILEGES = '481'
@sopel.moduleevent('481')
@sopel.modulerule('.*')
def parse_event_481(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CHANOPRIVSNEEDED = '482'
@sopel.moduleevent('482')
@sopel.modulerule('.*')
def parse_event_482(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_CANTKILLSERVER = '483'
@sopel.moduleevent('483')
@sopel.modulerule('.*')
def parse_event_483(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_RESTRICTED = '484'
@sopel.moduleevent('484')
@sopel.modulerule('.*')
def parse_event_484(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UNIQOPPRIVSNEEDED = '485'
@sopel.moduleevent('485')
@sopel.modulerule('.*')
def parse_event_485(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOOPERHOST = '491'
@sopel.moduleevent('491')
@sopel.modulerule('.*')
def parse_event_491(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_UMODEUNKNOWNFLAG = '501'
@sopel.moduleevent('501')
@sopel.modulerule('.*')
def parse_event_501(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_USERSDONTMATCH = '502'
@sopel.moduleevent('502')
@sopel.modulerule('.*')
def parse_event_502(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_STARTTLS = '670'
@sopel.moduleevent('670')
@sopel.modulerule('.*')
def parse_event_670(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_STARTTLS = '691'
@sopel.moduleevent('691')
@sopel.modulerule('.*')
def parse_event_691(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MONONLINE = '730'
@sopel.moduleevent('730')
@sopel.modulerule('.*')
def parse_event_730(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MONOFFLINE = '731'
@sopel.moduleevent('731')
@sopel.modulerule('.*')
def parse_event_731(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_MONLIST = '732'
@sopel.moduleevent('732')
@sopel.modulerule('.*')
def parse_event_732(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_ENDOFMONLIST = '733'
@sopel.moduleevent('733')
@sopel.modulerule('.*')
def parse_event_733(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_MONLISTFULL = '734'
@sopel.moduleevent('734')
@sopel.modulerule('.*')
def parse_event_734(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_WHOISKEYVALUE = '760'
@sopel.moduleevent('760')
@sopel.modulerule('.*')
def parse_event_760(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_KEYVALUE = '761'
@sopel.moduleevent('761')
@sopel.modulerule('.*')
def parse_event_761(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_METADATAEND = '762'
@sopel.moduleevent('762')
@sopel.modulerule('.*')
def parse_event_762(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_METADATALIMIT = '764'
@sopel.moduleevent('764')
@sopel.modulerule('.*')
def parse_event_764(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_TARGETINVALID = '765'
@sopel.moduleevent('765')
@sopel.modulerule('.*')
def parse_event_765(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NOMATCHINGKEY = '766'
@sopel.moduleevent('766')
@sopel.modulerule('.*')
def parse_event_766(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYINVALID = '767'
@sopel.moduleevent('767')
@sopel.modulerule('.*')
def parse_event_767(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYNOTSET = '768'
@sopel.moduleevent('768')
@sopel.modulerule('.*')
def parse_event_768(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_KEYNOPERMISSION = '769'
@sopel.moduleevent('769')
@sopel.modulerule('.*')
def parse_event_769(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LOGGEDIN = '900'
@sopel.moduleevent('900')
@sopel.modulerule('.*')
def parse_event_900(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_LOGGEDOUT = '901'
@sopel.moduleevent('901')
@sopel.modulerule('.*')
def parse_event_901(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_NICKLOCKED = '902'
@sopel.moduleevent('902')
@sopel.modulerule('.*')
def parse_event_902(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SASLSUCCESS = '903'
@sopel.moduleevent('903')
@sopel.modulerule('.*')
def parse_event_903(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLFAIL = '904'
@sopel.moduleevent('904')
@sopel.modulerule('.*')
def parse_event_904(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLTOOLONG = '905'
@sopel.moduleevent('905')
@sopel.modulerule('.*')
def parse_event_905(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLABORTED = '906'
@sopel.moduleevent('906')
@sopel.modulerule('.*')
def parse_event_906(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# ERR_SASLALREADY = '907'
@sopel.moduleevent('907')
@sopel.modulerule('.*')
def parse_event_907(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))


# RPL_SASLMECHS = '908'
@sopel.moduleevent('908')
@sopel.modulerule('.*')
def parse_event_908(bot, trigger):
   SpiceBot.logs.log('SpiceBot_Logs_IRC', str(trigger.event) + "    " + str(trigger.args))
