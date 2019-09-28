

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
                    if not targets:
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
                    if not targets:
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
                    if not targets:
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
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if not targets:
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
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        if not targets:
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
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    hasil = ""
                    for i in range(len(day)):
                        if hr == day[i]:
                            hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k):
                            bln = bulan[k - 1]
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
                    tz = pytz.timezone("Asia/Taipei")
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
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    hasil = ""
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
                    tz = pytz.timezone("Asia/Taipei")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                    hari = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
                             "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    hasil = ""
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