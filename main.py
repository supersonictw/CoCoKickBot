# -*- coding: utf-8 -*-
# import codecs
import datetime
import json
import os
# import pytz
import sys
import time
# import timeit
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
    with open("conf/{}.json".format(_data), "r") as f:
        data[_data] = json.load(f)

clProfile = line_client.profile
clMID = line_client.profile.mid

botStart = time.time()

for owner in data["creator"]["Max"]:
    admin = [clMID, owner]


def cTime_to_datetime(unix_time):
    return datetime.datetime.fromtimestamp(int(str(unix_time)[:-3]))


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
        with open("Reread.json", "w", encoding='utf8') as file:
            json.dump(data["reread"], file, ensure_ascii=False, indent=4, separators=(',', ': '))
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


def NOTIFIED_INVITE_INTO_ROOM(op):
    print("[22] NOTIFIED_INVITE_INTO_ROOM")
    if data["settings"]["autoLeave"]:
        line_client.leaveRoom(op.param1)


tracer.addOpInterrupt(22, NOTIFIED_INVITE_INTO_ROOM)


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
                    line_client.log("[%s]" % msg._from + msg.text)
                else:
                    line_client.log("[%s]" % msg.to + msg.text)
                if msg.contentType == 0:
                    data["reread"][msg.id] = {"text": msg.text, "from": msg._from, "createdTime": msg.createdTime}
        if data["settings"]["reck"]:
            if msg.contentType == 7:
                stk_id = msg.contentMetadata['STKID']
                if msg.toType == 0:
                    line_client.log("[%s]" % msg._from + stk_id)
                else:
                    line_client.log("[%s]" % msg.to + stk_id)
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
        to_id = op.param1
        msg_id = op.param2
        if data["settings"]["reread"]:
            if msg_id in data["reread"]:
                if data["reread"][msg_id]["from"] not in data["blacklist"]:
                    read_time = time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime(int(round(data["reread"][msg_id]["createdTime"] / 1000)))
                    )
                    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time()))))
                    try:
                        mi_d = data["reread"][msg_id]["from"]
                        contact_info = line_client.getContact(mi_d)
                        metion_msg = ""
                        msg_header1 = '[ 收回者 ]\n'
                        msg_header2 = '[ 收回訊息 ]\n'

                        tag_msg = "@user\n"
                        tag_msg_length1 = str(len(metion_msg) + len(msg_header1))
                        tag_msg_length2 = str(len(metion_msg) + len(tag_msg) + len(msg_header1) - 1)

                        mention = {'S': tag_msg_length1, 'E': tag_msg_length2, 'M': contact_info.mid}
                        mentions = {"MENTIONEES": [mention]}

                        metion_msg += tag_msg
                        cached_msg = data["reread"][msg_id]["text"]

                        text = "{}{}{}{}\n[ 發送時間 ]\n{}\n[ 收回時間 ]: \n{}".format(
                            msg_header1,
                            metion_msg,
                            msg_header2,
                            cached_msg,
                            read_time,
                            now_time
                        )

                        line_client.sendMessage(
                            contentType=0,
                            to=to_id,
                            text=text,
                            contentMetadata={
                                'MENTION': json.dumps(mentions)
                            }
                        )
                    except:
                        aa = '{"S":"0","E":"3","M":' + json.dumps(data["reread"][msg_id]["from"]) + '}'
                        txr = '[收回了一個貼圖]\n\n[發送時間]\n%s\n[收回時間]\n%s' % (read_time, now_time)
                        pesan = '@c \n'
                        text_ = pesan + txr
                        line_client.sendMessage(
                            contentType=0,
                            to=to_id,
                            text=text_,
                            contentMetadata={'MENTION': '{"MENTIONEES":[' + aa + ']}'}
                        )
                        line_client.sendImageWithURL(
                            to=to_id,
                            url='https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png'.
                                format(data["reread"][msg_id]["id"])
                        )
                del data["reread"][msg_id]
        else:
            pass
    except Exception as e:
        logError(e)


tracer.addOpInterrupt(65, NOTIFIED_DESTROY_MESSAGE)

while True:
    tracer.trace()
