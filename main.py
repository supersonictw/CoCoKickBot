# -*- coding: utf-8 -*-
import codecs
import datetime
import json
import os
import pytz
import sys
import time
import timeit
from datetime import datetime

from linepy import *

line_client = LINE()
line_client.log("Auth Token : " + str(line_client.authToken))
tracer = OEPoll(line_client)

data = {
    "read": None,
    "temp": None,
    "blacklist": None,
    "creator": None,
    "reread": None
}

for _data in data:
    with open("{}.json".format(_data), "r") as f:
        data[_data] = json.load(f)

clProfile = line_client.getProfile()
clMID = line_client.profile.mid
admin = ['u28d781fa3ba9783fd5144390352b0c24', clMID]

botStart = time.time()

for owner in data["creator"]["Max"]:
    admin = [clMID, owner]

bl = []


def cTime_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(int(str(unix_time)[:len(str(unix_time)) - 3]))


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def restartBot():
    print("[ 訊息 ] 機器 重新啟動")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)


def backupData():
    try:
        for data_ in data:
            with open('{}.json'.format(data_), 'w') as file:
                json.dump(data[data_], file, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False


def logError(text):
    line_client.log("[ 錯誤 ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt", "a") as error:
        error.write("\n[%s] %s" % (str(time_), text))


def logRead():
    try:
        with open("Reread.json", "w", encoding='utf8') as f:
            json.dump(data["reread"], f, ensure_ascii=False, indent=4, separators=(',', ': '))
    except Exception as error:
        logError(error)
        return False


def Tag(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":' + json.dumps(mid) + '}'
        text_ = '@co \n'
        line_client.sendMessage(to, text_, contentMetadata={'MENTION': '{"MENTIONEES":[' + aa + ']}'}, contentType=0)
    except Exception as error:
        logError(error)


def helpmessage():
    helpMessage = """☆║．．．．CoCo特製半垢．．．．║☆
↪ 「Help」        查看指令列表
↪ 「Help Black」  查看黑單指令
↪ 「Help Bot」    查看機器指令
↪ 「Help Group」  查看群組指令
↪ 「Help Kick」   查看踢人指令
↪ 「Help Other」  查看其他指令
〘 Creator By: ©CoCo™  〙
〘 line.me/ti/p/1MRX_Gjbmv 〙
☆║．．．．．．．．．．．．．．．║☆"""
    return helpMessage


def helpblack():
    helpBlack = """☆║．．．．．黑名單指令．．．．．║☆
↪ 「Clear Ban」  清空黑單
↪ 「Ban」        好友資料加入黑單
↪ 「Ban:」       系統識別碼加入黑單
↪ 「Ban @」      標註加入黑單
↪ 「banlist」    查看黑單
↪ 「Kill Ban」   剔除黑單
↪ 「Unban」      好友資料解除黑單
↪ 「Unban:」     系統識別碼解除黑單
↪ 「Unban @」    標註解除黑單
〘 Creator By: ©CoCo™  〙
〘 line.me/ti/p/1MRX_Gjbmv 〙
☆║．．．．．．．．．．．．．．．║☆"""
    return helpBlack


def helpbot():
    helpBot = """☆║．．．．．機器指令表．．．．．║☆
↪ 「Add On/Off」   自動加入好友 打開/關閉
↪ 「Join On/Off」  邀請自動進入群組 打開/關閉
↪ 「Leave On/Off」 自動離開副本 打開/關閉
↪ 「Reread On/Off」查看文字收回 打開/關閉
↪ 「Rec On/Off」   查看貼圖收回 打開/關閉
↪ 「Tag On/Off」   標註全部人 打開/關閉
〘 Creator By: ©CoCo™  〙
〘 line.me/ti/p/1MRX_Gjbmv 〙
☆║．．．．．．．．．．．．．．．║☆"""
    return helpBot


def helpgroup():
    helpGroup = """☆║．．．．．群組指令表．．．．．║☆
↪ 「Cancel」  取消群組成員的邀請
↪ 「Curl」    關閉群組網址
↪ 「Gcancel」 清空邀請中的群組
↪ 「Ginfo」   查看群組狀態
↪ 「Inv mid」 使用系統識別碼邀請進入群組
↪ 「Ourl」    開啟群組網址
〘 Creator By: ©CoCo™  〙
〘 line.me/ti/p/1MRX_Gjbmv 〙
☆║．．．．．．．．．．．．．．．║☆"""
    return helpGroup


def helpkick():
    helpKick = """☆║．．．．．踢人指令表．．．．．║☆
↪ 「Dk Name」  使用定名踢出成員
↪ 「Kill ban」 踢出黑單成員
↪ 「Nk Name」  使用名子踢出成員
↪ 「Ri @」     標註來回機票
↪ 「Tk @」     標注踢出成員
↪ 「Uk mid」   使用系統識別碼踢出成員
〘 Creator By: ©CoCo™  〙
〘 line.me/ti/p/1MRX_Gjbmv 〙
☆║．．．．．．．．．．．．．．．║☆"""
    return helpKick


def helpother():
    helpOther = """☆║．．．．．其他指令表．．．．．║☆
↪ 「About」  查看自己的狀態
↪ 「DT」     已讀點關閉
↪ 「Fbc:」   好友廣播
↪ 「Gbc:」   群組廣播
↪ 「NT」     已讀點開啟
↪ 「R」      查看已讀
↪ 「Rebot」  重新啟動機器
↪ 「Runtime」查看機器運行時間
↪ 「Sf」     已讀點關閉
↪ 「Sn」     已讀點開啟
↪ 「Speed」  查看機器速度
↪ 「Sr」     已讀點重設
↪ 「Tagall」 標註群組所有成員
〘 Creator By: ©CoCo™  〙
〘 line.me/ti/p/1MRX_Gjbmv 〙
☆║．．．．．．．．．．．．．．．║☆"""
    return helpOther


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    print("[19] NOTIFIED_KICKOUT_FROM_GROUP")
    try:
        if owner in op.param3:
            line_client.kickoutFromGroup(op.param1, [op.param2])
            line_client.inviteIntoGroup(op.param1, [owner])
            data["black"]["blacklist"][op.param2] = True
            backupData()
    except Exception as e:
        logError(e)


tracer.addOpInterrupt(19, NOTIFIED_KICKOUT_FROM_GROUP)


def CREATE_ROOM(op):
    print("[20] CREATE_ROOM")


tracer.addOpInterrupt(20, CREATE_ROOM)


def INVITE_INTO_ROOM(op):
    print("[21] INVITE_INTO_ROOM")


tracer.addOpInterrupt(21, INVITE_INTO_ROOM)


def NOTIFIED_INVITE_INTO_ROOM(op):
    print("[22] NOTIFIED_INVITE_INTO_ROOM")
    if data["settings"]["autoLeave"]:
        line_client.leaveRoom(op.param1)


tracer.addOpInterrupt(22, NOTIFIED_INVITE_INTO_ROOM)


def LEAVE_ROOM(op):
    print("[23] LEAVE_ROOM")


tracer.addOpInterrupt(23, LEAVE_ROOM)


def NOTIFIED_LEAVE_ROOM(op):
    print("[24] NOTIFIED_LEAVE_ROOM")
    if data["settings"]["autoLeave"]:
        line_client.leaveRoom(op.param1)


tracer.addOpInterrupt(24, NOTIFIED_LEAVE_ROOM)

# OP 25


def RECEIVE_MESSAGE(op):
    print("[26] RECEIVE_MESSAGE")
    try:
        msg = op.message
        if data["settings"]["reread"]:
            if msg.contentType == 0:
                if msg.toType == 0:
                    line_client.log("[%s]" % (msg._from) + msg.text)
                else:
                    line_client.log("[%s]" % (msg.to) + msg.text)
                if msg.contentType == 0:
                    data["reread"][msg.id] = {"text": msg.text, "from": msg._from, "createdTime": msg.createdTime}
        if data["settings"]["reck"]:
            if msg.contentType == 7:
                stk_id = msg.contentMetadata['STKID']
                if msg.toType == 0:
                    line_client.log("[%s]" % (msg._from) + stk_id)
                else:
                    line_client.log("[%s]" % (msg.to) + stk_id)
                if msg.contentType == 7:
                    data["reread"][msg.id] = {"id": stk_id, "from": msg._from, "createdTime": msg.createdTime}
        if len(data["reread"]) > 100:
            del data["reread"][min(list(data["reread"].keys()))]
        logRead()
    except Exception as e:
        print(e)


tracer.addOpInterrupt(26, RECEIVE_MESSAGE)


def NOTIFIED_READ_MESSAGE(op):
    print("[55] NOTIFIED_READ_MESSAGE")
    try:
        if op.param1 in data["read"]['readPoint']:
            if op.param2 in data["read"]['readMember'][op.param1]:
                pass
            else:
                data["read"]['readMember'][op.param1] += op.param2
            data["read"]['ROM'][op.param1][op.param2] = op.param2
            backupData()
        else:
            pass
    except Exception as error:
        logError(error)


tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)


def NOTIFIED_DESTROY_MESSAGE(op):
    print("[65] NOTIFIED_DESTROY_MESSAGE")
    try:
        msg = op.message
        at = op.param1
        msg_id = op.param2
        if data["settings"]["reread"]:
            if msg_id in data["reread"]:
                if data["reread"][msg_id]["from"] not in bl:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(int(round(data["reread"][msg_id]["createdTime"] / 1000))))
                    newtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time()))))
                    try:
                        mi_d = data["reread"][msg_id]["from"]
                        cmem = line_client.getContact(mi_d)
                        zx = ""
                        zxc = ""
                        zx2 = []
                        xpesan = '[ 收回者 ]\n'
                        xretext = '[ 收回訊息 ]\n'
                        xname = str(cmem.displayName)
                        pesan = ''
                        pesan2 = pesan + "@c\n"
                        xlen = str(len(zxc) + len(xpesan))
                        xlen2 = str(len(zxc) + len(pesan2) + len(xpesan) - 1)
                        zx = {'S': xlen, 'E': xlen2, 'M': cmem.mid}
                        zx2.append(zx)
                        zxc += pesan2
                        retext = data["reread"][msg_id]["text"]
                        text = xpesan + zxc + xretext + retext + "\n[ 發送時間 ]\n" + rereadtime + "\n[ 收回時間 ]: \n" + newtime
                        line_client.sendMessage(at, text, contentMetadata={
                            'MENTION': str('{"MENTIONEES":' + json.dumps(zx2).replace(' ', '') + '}')}, contentType=0)
                    except:
                        aa = '{"S":"0","E":"3","M":' + json.dumps(data["reread"][msg_id]["from"]) + '}'
                        txr = '[收回了一個貼圖]\n\n[發送時間]\n%s\n[收回時間]\n%s' % (rereadtime, newtime)
                        pesan = '@c \n'
                        text_ = pesan + txr
                        line_client.sendMessage(at, text_, contentMetadata={'MENTION': '{"MENTIONEES":[' + aa + ']}'},
                                       contentType=0)
                        line_client.sendImageWithURL(at, 'https://stickershop.line-scdn.net/stickershop/v1/sticker/' +
                                            data["reread"][msg_id]["id"] + '/ANDROID/sticker.png')
                del data["reread"][msg_id]
        else:
            pass
    except Exception as e:
        logError(e)


tracer.addOpInterrupt(65, NOTIFIED_DESTROY_MESSAGE)


while True:
    tracer.trace()
