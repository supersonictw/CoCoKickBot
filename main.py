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

cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))
tracer = OEPoll(cl)

readOpen = codecs.open("read.json", "r", "utf-8")
settingsOpen = codecs.open("temp.json", "r", "utf-8")
blackOpen = codecs.open("blacklist.json", "r", "utf-8")
adminsOpen = codecs.open("creator.json", "r", "utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)
black = json.load(blackOpen)
admins = json.load(adminsOpen)

clProfile = cl.getProfile()
clMID = cl.profile.mid
admin = ['u28d781fa3ba9783fd5144390352b0c24', clMID]

botStart = time.time()
setTime = {}
setTime = read['wait2']['setTime']

for owner in admins["Max"]:
    admin = [clMID, owner]

try:
    with open("Reread.json", "r", encoding="utf_8_sig") as f:
        msg_dict = json.loads(f.read())
except:
    print("讀取紀錄失敗")

bl = []


def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime)) - 3]))


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
        backup = settings
        f = codecs.open('temp.json', 'w', 'utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json', 'w', 'utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = black
        f = codecs.open('blacklist.json', 'w', 'utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = admins
        f = codecs.open('creator.json', 'w', 'utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False


def logError(text):
    cl.log("[ 錯誤 ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt", "a") as error:
        error.write("\n[%s] %s" % (str(time_), text))


def logRead():
    try:
        with open("Reread.json", "w", encoding='utf8') as f:
            json.dump(msg_dict, f, ensure_ascii=False, indent=4, separators=(',', ': '))
    except Exception as error:
        logError(error)
        return False


def Tag(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":' + json.dumps(mid) + '}'
        text_ = '@co \n'
        cl.sendMessage(to, text_, contentMetadata={'MENTION': '{"MENTIONEES":[' + aa + ']}'}, contentType=0)
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


def END_OF_OPERATION(op):
    return


tracer.addOpInterrupt(0, END_OF_OPERATION)


def UPDATE_PROFILE(op):
    print("[1] UPDATE_PROFILE")


tracer.addOpInterrupt(1, UPDATE_PROFILE)


def NOTIFIED_UPDATE_PROFILE(op):
    print("[2] NOTIFIED_UPDATE_PROFILE")


tracer.addOpInterrupt(2, NOTIFIED_UPDATE_PROFILE)


def REGISTER_USERID(op):
    print("[3] REGISTER_USERID")


tracer.addOpInterrupt(3, REGISTER_USERID)


def ADD_CONTACT(op):
    print("[4] ADD_CONTACT")


tracer.addOpInterrupt(4, ADD_CONTACT)


def NOTIFIED_ADD_CONTACT(op):
    print("[5] NOTIFIED_ADD_CONTACT")


tracer.addOpInterrupt(5, NOTIFIED_ADD_CONTACT)


def BLOCK_CONTACT(op):
    print("[6] BLOCK_CONTACT")


tracer.addOpInterrupt(6, BLOCK_CONTACT)


def UNBLOCK_CONTACT(op):
    print("[7] UNBLOCK_CONTACT")


tracer.addOpInterrupt(7, UNBLOCK_CONTACT)


def NOTIFIED_RECOMMEND_CONTACT(op):
    print("[8] NOTIFIED_RECOMMEND_CONTACT")


tracer.addOpInterrupt(8, NOTIFIED_RECOMMEND_CONTACT)


def CREATE_GROUP(op):
    print("[9] CREATE_GROUP")


tracer.addOpInterrupt(9, CREATE_GROUP)


def UPDATE_GROUP(op):
    print("[10] UPDATE_GROUP")


tracer.addOpInterrupt(10, UPDATE_GROUP)


def NOTIFIED_UPDATE_GROUP(op):
    print("[11] NOTIFIED_UPDATE_GROUP")


tracer.addOpInterrupt(11, NOTIFIED_UPDATE_GROUP)


def INVITE_INTO_GROUP(op):
    print("[12] INVITE_INTO_GROUP")


tracer.addOpInterrupt(12, INVITE_INTO_GROUP)


def NOTIFIED_INVITE_INTO_GROUP(op):
    print("[13] NOTIFIED_INVITE_INTO_GROUP")


tracer.addOpInterrupt(13, NOTIFIED_INVITE_INTO_GROUP)


def LEAVE_GROUP(op):
    print("[14] LEAVE_GROUP")


tracer.addOpInterrupt(14, LEAVE_GROUP)


def NOTIFIED_LEAVE_GROUP(op):
    print("[15] NOTIFIED_LEAVE_GROUP")


tracer.addOpInterrupt(15, NOTIFIED_LEAVE_GROUP)


def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    print("[17] NOTIFIED_ACCEPT_GROUP_INVITATION")


tracer.addOpInterrupt(17, NOTIFIED_ACCEPT_GROUP_INVITATION)


def KICKOUT_FROM_GROUP(op):
    print("[18] KICKOUT_FROM_GROUP")


tracer.addOpInterrupt(18, KICKOUT_FROM_GROUP)


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    print("[19] NOTIFIED_KICKOUT_FROM_GROUP")
    try:
        if owner in op.param3:
            cl.kickoutFromGroup(op.param1, [op.param2])
            cl.inviteIntoGroup(op.param1, [owner])
            black["blacklist"][op.param2] = True
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
    if settings["autoLeave"] == True:
        cl.leaveRoom(op.param1)


tracer.addOpInterrupt(22, NOTIFIED_INVITE_INTO_ROOM)


def LEAVE_ROOM(op):
    print("[23] LEAVE_ROOM")


tracer.addOpInterrupt(23, LEAVE_ROOM)


def NOTIFIED_LEAVE_ROOM(op):
    print("[24] NOTIFIED_LEAVE_ROOM")
    if settings["autoLeave"] == True:
        cl.leaveRoom(op.param1)


tracer.addOpInterrupt(24, NOTIFIED_LEAVE_ROOM)


def SEND_MESSAGE(op):
    print("[25] SEND_MESSAGE")
    try:
        msg = op.message
        text = msg.text
        msg_id = msg.id
        receiver = msg.to
        sender = msg._from
        if msg.toType == 0:
            if sender != cl.profile.mid:
                to = sender
            else:
                to = receiver
        else:
            to = receiver
        if msg.contentType == 13:
            if settings["wblack"] == True:
                if msg.contentMetadata["mid"] in black["blacklist"]:
                    cl.sendMessage(to, "已經在黑名單了")
                    settings["wblack"] = False
                else:
                    black["blacklist"][msg.contentMetadata["mid"]] = True
                    cl.sendMessage(to, "已加入黑名單")
                    settings["wblack"] = False
                backupData()
            elif settings["dblack"] == True:
                if msg.contentMetadata["mid"] in black["blacklist"]:
                    del black["blacklist"][msg.contentMetadata["mid"]]
                    cl.sendMessage(to, "已解除黑名單")
                    settings["dblack"] = False
                else:
                    cl.sendMessage(to, "他不在黑名單")
                    settings["dblack"] = False
                backupData()
        if msg.contentType == 0:
            if sender in admin:
                if msg.text is None:
                    pass
                elif text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif text.lower() == 'help black':
                    helpBlack = helpblack()
                    cl.sendMessage(to, str(helpBlack))
                elif text.lower() == 'help bot':
                    helpBot = helpbot()
                    cl.sendMessage(to, str(helpBot))
                elif text.lower() == 'help group':
                    helpGroup = helpgroup()
                    cl.sendMessage(to, str(helpGroup))
                elif text.lower() == 'help kick':
                    helpKick = helpkick()
                    cl.sendMessage(to, str(helpKick))
                elif text.lower() == 'help other':
                    helpOther = helpother()
                    cl.sendMessage(to, str(helpOther))
                elif "Fbc:" in msg.text:
                    bctxt = text.replace("Fbc:", "")
                    t = cl.getAllContactIds()
                    try:
                        for manusia in t:
                            cl.sendMessage(manusia, (bctxt))
                    except Exception as e:
                        print(e)
                elif "Gbc:" in msg.text:
                    bctxt = text.replace("Gbc:", "")
                    n = cl.getGroupIdsJoined()
                    try:
                        for manusia in n:
                            cl.sendMessage(manusia, (bctxt))
                    except Exception as e:
                        print(e)
                elif "Ri " in msg.text:
                    Ri0 = text.replace("Ri ", "")
                    Ri1 = Ri0.rstrip()
                    Ri2 = Ri1.replace("@", "")
                    Ri3 = Ri2.rstrip()
                    _name = Ri3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                cl.kickoutFromGroup(to, [target])
                                cl.findAndAddContactsByMid(target)
                                cl.inviteIntoGroup(to, [target])
                elif "Uk " in msg.text:
                    midd = text.replace("Uk ", "")
                    cl.kickoutFromGroup(to, [midd])
                elif "Tk " in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        if target in admin:
                            pass
                        else:
                            cl.kickoutFromGroup(to, [target])
                elif "Nk " in msg.text:
                    _name = text.replace("Nk ", "")
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                cl.kickoutFromGroup(to, [target])
                elif "Dk " in msg.text:
                    _name = text.replace("Dk ", "")
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        try:
                            contact = cl.getContact(g.mid)
                            if _name in contact.displayNameOverridden:
                                targets.append(g.mid)
                        except:
                            pass
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in admin:
                                pass
                            else:
                                cl.kickoutFromGroup(to, [target])
                elif "NT " in msg.text:
                    _name = text.replace("NT ", "")
                    gs = cl.getGroup(to)
                    txt = u''
                    s = 0
                    b = []
                    for g in gs.members:
                        if _name in g.displayName:
                            b.append({"S": str(s), "E": str(s + 6), "M": g.mid})
                            s += 7
                            txt += u'@CoCo \n'
                    if b == []:
                        cl.sendMessage(to, "這個群組沒有這個人")
                    else:
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES': b})},
                                       contentType=0)
                elif "DT " in msg.text:
                    _name = text.replace("DT ", "")
                    gs = cl.getGroup(to)
                    txt = u''
                    s = 0
                    b = []
                    for g in gs.members:
                        try:
                            contact = cl.getContact(g.mid)
                            if _name in contact.displayNameOverridden:
                                b.append({"S": str(s), "E": str(s + 6), "M": g.mid})
                                s += 7
                                txt += u'@CoCo \n'
                        except:
                            pass
                    if b == []:
                        cl.sendMessage(to, "這個群組沒有這個人")
                    else:
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES': b})},
                                       contentType=0)
                elif msg.text in ["c", "C", "cancel", "Cancel"]:
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        if X.invitee is not None:
                            gInviMids = (contact.mid for contact in X.invitee)
                            ginfo = cl.getGroup(msg.to)
                            sinvitee = str(len(ginfo.invitee))
                            start = time.time()
                            for cancelmod in gInviMids:
                                cl.cancelGroupInvitation(to, [cancelmod])
                                time.sleep(0.5)
                            elapsed_time = time.time() - start
                            cl.sendMessage(to, "已取消完成\n取消時間: %s秒" % (elapsed_time))
                            cl.sendMessage(to, "取消人數:" + sinvitee)
                        else:
                            cl.sendMessage(to, "沒有任何人在邀請中！！")
                elif text.lower() == 'gcancel':
                    gid = cl.getGroupIdsInvited()
                    start = time.time()
                    for i in gid:
                        cl.rejectGroupInvitation(i)
                    elapsed_time = time.time() - start
                    cl.sendMessage(to, "全部群組邀請已取消")
                    cl.sendMessage(to, "取消時間: %s秒" % (elapsed_time))
                elif "Inv " in msg.text:
                    try:
                        midd = msg.text.replace("Inv ", "")
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(msg.to, [midd])
                    except:
                        cl.sendMessage(to, "Mid錯誤或可能在邀請中了！！")
                elif text.lower() == 'ban':
                    settings["wblack"] = True
                    backupData()
                    cl.sendMessage(msg.to, "請丟出好友資料")
                elif text.lower() == 'unban':
                    settings["dblack"] = True
                    backupData()
                    cl.sendMessage(msg.to, "請丟出好友資料")
                elif "Ban:" in msg.text:
                    midd = msg.text.replace("Ban:", "")
                    try:
                        black["blacklist"][midd] = True
                        backupData()
                        cl.sendMessage(to, "已加入黑名單")
                    except:
                        pass
                elif "Unban:" in msg.text:
                    midd = msg.text.replace("Unban:", "")
                    try:
                        del black["blacklist"][midd]
                        backupData()
                        cl.sendMessage(to, "已解除黑名單")
                    except:
                        pass
                elif "Ban " in msg.text:
                    if msg.toType == 2:
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            try:
                                for target in targets:
                                    black["blacklist"][target] = True
                                backupData()
                                cl.sendMessage(to, "已加入黑名單")
                            except:
                                pass
                elif "Unban " in msg.text:
                    if msg.toType == 2:
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if targets == []:
                            pass
                        else:
                            try:
                                for target in targets:
                                    del black["blacklist"][target]
                                backupData()
                                cl.sendMessage(to, "已解除黑名單")
                            except:
                                pass
                elif text.lower() == 'clear ban':
                    black["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
                elif text.lower() == 'banlist':
                    if black["blacklist"] == {}:
                        cl.sendMessage(to, "沒有黑名單")
                    else:
                        cl.sendMessage(to, "以下是黑名單")
                        mc = ""
                        for mi_d in black["blacklist"]:
                            mc += "->" + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                        cl.sendMessage(to, "總共 {} 個黑名單".format(str(len(black["blacklist"]))))
                elif text.lower() == 'kill ban':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                        for tag in black["blacklist"]:
                            matched_list += filter(lambda str: str == tag, gMembMids)
                        if matched_list == []:
                            cl.sendMessage(to, "沒有黑名單")
                        else:
                            for jj in matched_list:
                                cl.kickoutFromGroup(to, [jj])
                            cl.sendMessage(to, "黑名單以踢除")
                elif "/invitemeto:" in msg.text:
                    gid = msg.text.replace("/invitemeto:", "")
                    if gid == "":
                        cl.sendMessage(to, "請輸入群組ID")
                    else:
                        try:
                            cl.findAndAddContactsByMid(sender)
                            cl.inviteIntoGroup(gid, [sender])
                        except:
                            cl.sendMessage(to, "我不在那個群組裡")
                elif "拒絕:群組邀請" in msg.text or "拒絕：群組邀請" in msg.text:
                    gid = cl.getGroupIdsInvited()
                    for i in gid:
                        cl.acceptGroupInvitation(i)
                        time.sleep(0.5)
                        try:
                            cl.leaveGroup(i)
                        except:
                            pass
                    cl.sendMessage(to, "已拒絕所有群組邀請！\n群組數量：{}".format(str(len(gid))))
                elif "同意:群組邀請" in msg.text or "同意：群組邀請" in msg.text:
                    gid = cl.getGroupIdsInvited()
                    for i in gid:
                        cl.acceptGroupInvitation(i)
                    cl.sendMessage(to, "已進入邀請中的群組！\n群組數量：{}".format(str(len(gid))))
                elif text.lower() == 'speed' or text.lower() == 'sp':
                    curTime = time.time()
                    cl.sendMessage(to, "請稍等...")
                    rtime = time.time()
                    xtime = rtime - curTime
                    cl.sendMessage(to, '處理速度\n' + format(str(xtime)) + '秒')
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=5000)
                    str1 = str(time0)
                    cl.sendMessage(to, '反應時間\n' + str1 + '秒')
                elif text.lower() == 'rebot':
                    cl.sendMessage(to, "重新啟動")
                    restartBot()
                elif text.lower() == 'uptime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = datetime.timedelta(seconds=runtime)
                    cl.sendMessage(to, "機器運行時間 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        owner = "u28d781fa3ba9783fd5144390352b0c24"
                        creator = cl.getContact(owner)
                        contact = cl.getContact(clMID)
                        grouplist = cl.getGroupIdsJoined()
                        contactlist = cl.getAllContactIds()
                        blockedlist = cl.getBlockedContactIds()
                        groupinvite = cl.getGroupIdsInvited()
                        ret_ = "╔══[ 關於自己 ]"
                        ret_ += "\n╠ 名稱 : {}".format(contact.displayName)
                        ret_ += "\n╠ 群組 : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ 好友 : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ 黑單 : {}".format(str(len(blockedlist)))
                        ret_ += "\n╠ 邀請 : {}".format(str(len(groupinvite)))
                        ret_ += "\n╠══[ 關於機器 ]"
                        ret_ += "\n╠ 版本 : CoCo特製版v1.5"
                        ret_ += "\n╠ 作者 : {}".format(creator.displayName)
                        ret_ += "\n╚══[ 未經許可禁止重製 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'set':
                    try:
                        ret_ = "╔══[ 設定 ]"
                        if settings["autoAdd"] == True:
                            ret_ += "\n╠ 自動加入好友 ✅"
                        else:
                            ret_ += "\n╠ 自動加入好友 ❌"
                        if settings["autoJoin"] == True:
                            ret_ += "\n╠ 自動加入群組 ✅"
                        else:
                            ret_ += "\n╠ 自動加入群組 ❌"
                        if settings["autoLeave"] == True:
                            ret_ += "\n╠ 自動離開副本 ✅"
                        else:
                            ret_ += "\n╠ 自動離開副本 ❌"
                        if settings["targets"] == True:
                            ret_ += "\n╠ 標註全部人 ✅"
                        else:
                            ret_ += "\n╠ 標註全部人 ❌"
                        if settings["reread"] == True:
                            ret_ += "\n╠ 查詢收回開啟 ✅"
                        else:
                            ret_ += "\n╠ 查詢收回關閉 ❌"
                        if settings["reck"] == True:
                            ret_ += "\n╠ 查詢貼圖收回開啟 ✅"
                        else:
                            ret_ += "\n╠ 查詢貼圖收回關閉 ❌"
                        ret_ += "\n╚══[ 設定 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'add on':
                    settings["autoAdd"] = True
                    backupData()
                    cl.sendMessage(to, "自動加入好友已開啟")
                elif text.lower() == 'add off':
                    settings["autoAdd"] = False
                    backupData()
                    cl.sendMessage(to, "自動加入好友已關閉")
                elif text.lower() == 'join on':
                    settings["autoJoin"] = True
                    backupData()
                    cl.sendMessage(to, "自動加入群組已開啟")
                elif text.lower() == 'join off':
                    settings["autoJoin"] = False
                    backupData()
                    cl.sendMessage(to, "自動加入群組已關閉")
                elif text.lower() == 'leave on':
                    settings["autoLeave"] = True
                    backupData()
                    cl.sendMessage(to, "自動離開副本已開啟")
                elif text.lower() == 'leave off':
                    settings["autoLeave"] = False
                    backupData()
                    cl.sendMessage(to, "自動離開副本已關閉")
                elif text.lower() == 'reread on':
                    settings["reread"] = True
                    backupData()
                    cl.sendMessage(to, "查詢收回開啟")
                elif text.lower() == 'reread off':
                    settings["reread"] = False
                    backupData()
                    cl.sendMessage(to, "查詢收回關閉")
                elif text.lower() == 'rec on':
                    settings["reck"] = True
                    backupData()
                    cl.sendMessage(to, "查詢收回開啟")
                elif text.lower() == 'rec off':
                    settings["reck"] = False
                    backupData()
                    cl.sendMessage(to, "查詢收回關閉")
                elif text.lower() == 'tag on':
                    settings["targets"] = True
                    cl.sendMessage(to, "標註開啟")
                elif text.lower() == 'tag off':
                    settings["targets"] = False
                    cl.sendMessage(to, "標註關閉")
                elif text.lower() == 'ourl':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == False:
                            cl.sendMessage(to, "群組網址已開啟")
                        else:
                            G.preventedJoinByTicket = False
                            cl.updateGroup(G)
                            cl.sendMessage(to, "成功開啟群組網址")
                elif text.lower() == 'curl':
                    if msg.toType == 2:
                        G = cl.getGroup(to)
                        if G.preventedJoinByTicket == True:
                            cl.sendMessage(to, "群組網址已關閉")
                        else:
                            G.preventedJoinByTicket = True
                            cl.updateGroup(G)
                            cl.sendMessage(to, "成功關閉群組網址")
                elif text.lower() == 'ginfo':
                    group = cl.getGroup(to)
                    gtime = group.createdTime
                    gtimee = int(round(gtime / 1000))
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "未找到"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "沒有"
                    else:
                        gQr = "開啟"
                        gTicket = "https://cl.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                        try:
                            path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                        except:
                            pass
                    ret_ = "╔══[ 群組資料 ]"
                    ret_ += "\n╠ 顯示名稱 : {}".format(str(group.name))
                    ret_ += "\n╠ 群組ＩＤ : {}".format(group.id)
                    ret_ += "\n╠ 群組作者 : {}".format(str(gCreator))
                    ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
                    ret_ += "\n╠ 邀請數量 : {}".format(gPending)
                    ret_ += "\n╠ 群組網址 : {}".format(gQr)
                    ret_ += "\n╠ 群組網址 : {}".format(gTicket)
                    ret_ += "\n╠ 群組建立時間 : {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(gtimee)))
                    ret_ += "\n╚══[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    try:
                        cl.sendImageWithURL(to, path)
                    except:
                        pass
                elif text.lower() == 'tagall':
                    if msg.toType == 2:
                        if settings["targets"] == True:
                            group = cl.getGroup(msg.to)
                            nama = [contact.mid for contact in group.members]
                            k = len(nama) // 100
                            for a in range(k + 1):
                                txt = u''
                                s = 0
                                b = []
                                for i in group.members[a * 100: (a + 1) * 100]:
                                    b.append({"S": str(s), "E": str(s + 6), "M": i.mid})
                                    s += 7
                                    txt += u'@CoCo \n'
                                cl.sendMessage(to, text=txt,
                                               contentMetadata={u'MENTION': json.dumps({'MENTIONEES': b})},
                                               contentType=0)
                                cl.sendMessage(to, "總共 {} 個成員".format(str(len(nama))))
                        else:
                            cl.sendMessage(to, "標註未開啟")
                elif text.lower() == 'sn':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k - 1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                        '%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "已讀點已開始")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            cl.sendMessage(msg.to, "設定已讀點:\n" + readTime)
                    backupData()
                elif text.lower() == 'sf':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k - 1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                        '%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        cl.sendMessage(msg.to, "已讀點已經關閉")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        cl.sendMessage(msg.to, "刪除已讀點:\n" + readTime)
                    backupData()
                elif text.lower() == 'rr':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k - 1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                        '%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        cl.sendMessage(msg.to, "重置已讀點:\n" + readTime)
                    else:
                        cl.sendMessage(msg.to, "已讀點未設定")
                    backupData()
                elif text.lower() == 'r':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k - 1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                        '%Y') + "\n時間 : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            cl.sendMessage(receiver, "[ 已讀者 ]:\n沒有")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = cl.getContacts(chiya)
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = '[ 已讀者 ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan + "@c\n"
                            xlen = str(len(zxc) + len(xpesan))
                            xlen2 = str(len(zxc) + len(pesan2) + len(xpesan) - 1)
                            zx = {'S': xlen, 'E': xlen2, 'M': cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan + zxc + "\n[ 已讀時間 ]: \n" + readTime
                        try:
                            cl.sendMessage(receiver, text, contentMetadata={
                                'MENTION': str('{"MENTIONEES":' + json.dumps(zx2).replace(' ', '') + '}')},
                                           contentType=0)
                        except Exception as error:
                            print(error)
                    else:
                        cl.sendMessage(receiver, "已讀點未設定")
                    backupData()
    except Exception as e:
        logError(e)


tracer.addOpInterrupt(25, SEND_MESSAGE)


def RECEIVE_MESSAGE(op):
    print("[26] RECEIVE_MESSAGE")
    try:
        msg = op.message
        if settings["reread"] == True:
            if msg.contentType == 0:
                if msg.toType == 0:
                    cl.log("[%s]" % (msg._from) + msg.text)
                else:
                    cl.log("[%s]" % (msg.to) + msg.text)
                if msg.contentType == 0:
                    msg_dict[msg.id] = {"text": msg.text, "from": msg._from, "createdTime": msg.createdTime}
        if settings["reck"] == True:
            if msg.contentType == 7:
                stk_id = msg.contentMetadata['STKID']
                if msg.toType == 0:
                    cl.log("[%s]" % (msg._from) + stk_id)
                else:
                    cl.log("[%s]" % (msg.to) + stk_id)
                if msg.contentType == 7:
                    msg_dict[msg.id] = {"id": stk_id, "from": msg._from, "createdTime": msg.createdTime}
        if len(msg_dict) > 100:
            del msg_dict[min(list(msg_dict.keys()))]
        logRead()
    except Exception as e:
        print(e)


tracer.addOpInterrupt(26, RECEIVE_MESSAGE)


def NOTIFIED_CANCEL_INVITATION_GROUP(op):
    print("[32] NOTIFIED_CANCEL_INVITATION_GROUP")


tracer.addOpInterrupt(32, NOTIFIED_CANCEL_INVITATION_GROUP)


def NOTIFIED_REJECT_GROUP_INVITATION(op):
    print("[35] NOTIFIED_REJECT_GROUP_INVITATION")


tracer.addOpInterrupt(35, NOTIFIED_REJECT_GROUP_INVITATION)


def SEND_CHAT_CHECKED(op):
    print("[40] SEND_CHAT_CHECKED")


tracer.addOpInterrupt(40, SEND_CHAT_CHECKED)


def NOTIFIED_READ_MESSAGE(op):
    print("[55] NOTIFIED_READ_MESSAGE")
    try:
        if op.param1 in read['readPoint']:
            if op.param2 in read['readMember'][op.param1]:
                pass
            else:
                read['readMember'][op.param1] += op.param2
            read['ROM'][op.param1][op.param2] = op.param2
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
        if settings["reread"] == True:
            if msg_id in msg_dict:
                if msg_dict[msg_id]["from"] not in bl:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(int(round(msg_dict[msg_id]["createdTime"] / 1000))))
                    newtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time()))))
                    try:
                        mi_d = msg_dict[msg_id]["from"]
                        cmem = cl.getContact(mi_d)
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
                        retext = msg_dict[msg_id]["text"]
                        text = xpesan + zxc + xretext + retext + "\n[ 發送時間 ]\n" + rereadtime + "\n[ 收回時間 ]: \n" + newtime
                        cl.sendMessage(at, text, contentMetadata={
                            'MENTION': str('{"MENTIONEES":' + json.dumps(zx2).replace(' ', '') + '}')}, contentType=0)
                    except:
                        aa = '{"S":"0","E":"3","M":' + json.dumps(msg_dict[msg_id]["from"]) + '}'
                        txr = '[收回了一個貼圖]\n\n[發送時間]\n%s\n[收回時間]\n%s' % (rereadtime, newtime)
                        pesan = '@c \n'
                        text_ = pesan + txr
                        cl.sendMessage(at, text_, contentMetadata={'MENTION': '{"MENTIONEES":[' + aa + ']}'},
                                       contentType=0)
                        cl.sendImageWithURL(at, 'https://stickershop.line-scdn.net/stickershop/v1/sticker/' +
                                            msg_dict[msg_id]["id"] + '/ANDROID/sticker.png')
                del msg_dict[msg_id]
        else:
            pass
    except Exception as e:
        logError(e)


tracer.addOpInterrupt(65, NOTIFIED_DESTROY_MESSAGE)


def NOTIFIED_BLOCK_CONTACT(op):
    print("[68] NOTIFIED_BLOCK_CONTACT")


tracer.addOpInterrupt(68, NOTIFIED_BLOCK_CONTACT)


def NOTIFIED_UNBLOCK_CONTACT(op):
    print("[69] NOTIFIED_UNBLOCK_CONTACT")


tracer.addOpInterrupt(69, NOTIFIED_UNBLOCK_CONTACT)


def NOTIFIED_ADD_FOLLOW(op):
    print("[84] NOTIFIED_ADD_FOLLOW")


tracer.addOpInterrupt(84, NOTIFIED_ADD_FOLLOW)


def NOTIFIED_DELETE_FOLLOW(op):
    print("[86] NOTIFIED_DELETE_FOLLOW")


tracer.addOpInterrupt(86, NOTIFIED_DELETE_FOLLOW)


def NOTIFIED_FRIEND_REQUEST(op):
    print("[88] NOTIFIED_FRIEND_REQUEST")


tracer.addOpInterrupt(88, NOTIFIED_FRIEND_REQUEST)

while True:
    tracer.trace()
