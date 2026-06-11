#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读 manifest.json，生成 hyperframes 主合成 index.html。
场景时序/字幕时序全部来自 TTS manifest，保证画面-配音-字幕同步。
场景间用 0.35s 叠化(crossfade)：后一场景在前一场景之上 fade-in；除最后一场景外不做退出动画。"""
import json, html

M = json.load(open("manifest.json", encoding="utf-8"))
SC = M["scenes"]
TOTAL = M["totalDuration"]
XFADE = 0.35      # 叠化时长
TAIL = 0.4        # 末尾留白

# ---------- 各场景内层 HTML（沿用 deck 的结构/样式） ----------
SCENE_HTML = {
1: """<div class="cover-text">
  <span class="cv-badge">Codex 实用技巧 · 0 成本</span>
  <div class="cv-title">撞限别干等</div>
  <div class="cv-line2">一个设置，额度<span class="em">翻倍</span></div>
  <div style="margin-top:26px"><span class="cv-sub">「5 小时滚动窗口」的小秘密</span></div>
</div>""",
2: """<div class="shead"><div class="badge b-purple">1</div><div class="htitle t-purple">额度不是「每天重置」</div></div>
<div class="sbody">
  <div class="claycard win-card">
    <div class="win-row">
      <div class="msg-chip">💬 你发出<br>第一条消息</div>
      <div class="win-arrow">→</div>
      <div class="win-bar-wrap">
        <div class="win-bar-label">5 小时滚动窗口</div>
        <div class="win-bar"><div class="win-fill"></div>
          <div class="win-ticks"><span>0h</span><span>1h</span><span>2h</span><span>3h</span><span>4h</span><span>5h</span></div></div>
      </div>
    </div>
    <div class="win-note">发出第一条消息那一刻，5 小时<b>开始倒计时</b></div>
    <div class="win-hint">不是按自然日重置，而是一个跟着你「滚」的窗口</div>
  </div>
</div>""",
3: """<div class="quote-wrap">
  <div class="q-small">窗口走完，系统不会自动给你开下一个——</div>
  <div class="q-big">它会一直<span class="qy">等</span></div>
  <div class="q-mid">等你发下一条消息，才重新计时</div>
  <div class="q-arrow">↓</div>
  <div class="q-concl">所以这个重置时间<br><span class="qy">其实你自己能控制</span></div>
</div>""",
4: """<div class="shead"><div class="badge b-blue">2</div><div class="htitle t-blue">同样下午开工，差出一整个窗口</div></div>
<div class="sbody cmp-body">
  <div class="lane laneA">
    <div class="lane-label bad">❌ 不会用</div>
    <div class="track">
      <div class="pin" style="left:37.5%">下午2点才发第一条</div>
      <div class="seg used" style="left:37.5%;width:18.75%">2点干到<br>3点半</div>
      <div class="seg idle" style="left:56.25%;width:43.75%">额度见底，剩下时间只能干瞪眼</div>
    </div>
  </div>
  <div class="ruler">
    <span style="left:0%">11点</span><span style="left:12.5%">12点</span><span style="left:25%">1点</span>
    <span style="left:37.5%">2点</span><span style="left:50%">3点</span><span style="left:62.5%">4点</span>
    <span style="left:75%">5点</span><span style="left:87.5%">6点</span><span style="left:100%">7点</span>
  </div>
  <div class="lane laneB">
    <div class="lane-label good">✅ 会用</div>
    <div class="track">
      <div class="seg win1" style="left:0%;width:62.5%">窗口① 11点先点亮 → 4点重置</div>
      <div class="seg win2" style="left:62.5%;width:37.5%">窗口② 4点起</div>
      <div class="core" style="left:37.5%;width:50%"><span>核心 2–6 点 · 吃满两个窗口</span></div>
    </div>
  </div>
</div>""",
5: """<div class="shead"><div class="badge b-green">3</div><div class="htitle t-green">用「自动化」自动点亮窗口</div></div>
<div class="sbody">
  <div class="steps">
    <div class="steprow"><div class="snum b-purple">1</div><div class="stitle">打开 Codex 的「自动化」</div><div class="sdesc">面板里找到<br>Automations</div></div>
    <div class="steprow"><div class="snum b-blue">2</div><div class="stitle">点右上角「从聊天创建」</div><div class="sdesc">用大白话<br>写一句任务</div></div>
    <div class="steprow"><div class="snum b-green">3</div><div class="stitle">输入<span class="scmd">每天上午九点跟我说声你好</span></div><div class="sdesc">存下来<br>就完事了</div></div>
  </div>
  <div class="step-foot">它每天九点自动发一条 = <span class="hl">帮你把窗口提前点亮</span>，设一次长期生效</div>
</div>""",
6: """<div class="shead"><div class="badge b-orange">!</div><div class="htitle t-orange">很多教程不会告诉你的坑</div></div>
<div class="sbody warn-body">
  <div class="claycard warn-card"><div class="warn-ic">💻</div>
    <div><div class="warn-t">自动化是跑在「本地」的</div>
    <div class="warn-d">得让电脑一直开着、Codex 一直运行，定时任务才会执行</div></div></div>
  <div class="claycard warn-card"><div class="warn-ic moon">🌙</div>
    <div><div class="warn-t">系统里打开「防止睡眠」</div>
    <div class="warn-d">否则电脑一休眠，到点的任务就跑空了，等于白设</div></div></div>
</div>""",
7: """<div class="cover-text">
  <div class="cv-title s2">关注 <span class="em">AI少年</span></div>
  <div class="cv-line2">AI 的事，听 AI少年 说</div>
  <div style="margin-top:26px"><span class="cv-sub">咱们下期接着聊 👋</span></div>
</div>""",
}
SCENE_CLASS = {1:"cover", 2:"slide", 3:"quote-slide", 4:"slide", 5:"slide", 6:"slide", 7:"cover"}

# 每场景入场动画 (选择器, vars, 相对场景起点的偏移)
def entrances(sid):
    p = f"#s{sid}"
    if sid in (1,7):
        items = []
        if sid == 1:  # 仅封面有 badge
            items.append((f"{p} .cv-badge", {"y":40,"opacity":0,"duration":0.55,"ease":"power3.out"}, 0.15))
        items += [
            (f"{p} .cv-title", {"y":50,"opacity":0,"duration":0.6,"ease":"back.out(1.4)"}, 0.2),
            (f"{p} .cv-line2", {"y":34,"opacity":0,"duration":0.5,"ease":"power2.out"}, 0.36),
            (f"{p} .cv-sub", {"opacity":0,"duration":0.5,"ease":"sine.out"}, 0.52),
        ]
        return items
    if sid == 2:
        return [
            (f"{p} .shead", {"y":-30,"opacity":0,"duration":0.5,"ease":"power3.out"}, 0.15),
            (f"{p} .msg-chip", {"x":-50,"opacity":0,"duration":0.5,"ease":"back.out(1.5)"}, 0.35),
            (f"{p} .win-bar-wrap", {"x":40,"opacity":0,"duration":0.55,"ease":"power2.out"}, 0.5),
            (f"{p} .win-note, {p} .win-hint", {"y":24,"opacity":0,"duration":0.5,"ease":"sine.out","stagger":0.12}, 0.75),
        ]
    if sid == 3:
        return [
            (f"{p} .q-small", {"opacity":0,"duration":0.45,"ease":"sine.out"}, 0.15),
            (f"{p} .q-big", {"scale":0.8,"opacity":0,"duration":0.55,"ease":"back.out(1.6)"}, 0.32),
            (f"{p} .q-mid", {"y":20,"opacity":0,"duration":0.45,"ease":"power2.out"}, 0.55),
            (f"{p} .q-concl", {"y":36,"opacity":0,"duration":0.6,"ease":"power3.out"}, 0.85),
        ]
    if sid == 4:
        return [
            (f"{p} .shead", {"y":-28,"opacity":0,"duration":0.5,"ease":"power3.out"}, 0.15),
            (f"{p} .laneA", {"x":-60,"opacity":0,"duration":0.55,"ease":"power2.out"}, 0.4),
            (f"{p} .ruler", {"opacity":0,"duration":0.4,"ease":"sine.out"}, 0.65),
            (f"{p} .laneB", {"x":-60,"opacity":0,"duration":0.55,"ease":"power2.out"}, 0.8),
            (f"{p} .core", {"scale":0.9,"opacity":0,"duration":0.5,"ease":"back.out(1.5)"}, 1.2),
        ]
    if sid == 5:
        return [
            (f"{p} .shead", {"y":-28,"opacity":0,"duration":0.5,"ease":"power3.out"}, 0.15),
            (f"{p} .steprow", {"x":-50,"opacity":0,"duration":0.5,"ease":"back.out(1.3)","stagger":0.22}, 0.4),
            (f"{p} .step-foot", {"y":24,"opacity":0,"duration":0.5,"ease":"power2.out"}, 1.3),
        ]
    if sid == 6:
        return [
            (f"{p} .shead", {"y":-28,"opacity":0,"duration":0.5,"ease":"power3.out"}, 0.15),
            (f"{p} .warn-card", {"y":40,"opacity":0,"duration":0.55,"ease":"back.out(1.3)","stagger":0.28}, 0.45),
        ]
    return []

# ---------- 计算场景 clip 时序（带叠化重叠） ----------
def scene_start(i):  # i: 0-based
    return SC[i]["start"]

clips = []   # (id, start, dur, zclass, htmlclass, inner)
for i, s in enumerate(SC):
    sid = s["scene"]
    start = round(scene_start(i), 3)
    if i < len(SC) - 1:
        next_start = scene_start(i + 1)
        dur = round((next_start - start) + XFADE, 3)
    else:
        dur = round(s["dur"] + TAIL, 3)
    clips.append((sid, start, dur))

# ---------- 字幕 clip ----------
caps = []
cid = 0
for s in SC:
    n = len(s["captions"])
    for k, c in enumerate(s["captions"]):
        # 字幕显示到下一句开始（含句间停顿），末句到场景结束
        if k < n - 1:
            cdur = round(s["captions"][k+1]["start"] - c["start"], 3)
        else:
            cdur = round((s["start"] + s["dur"]) - c["start"], 3)
        caps.append((f"c{cid}", round(c["start"],3), cdur, c["text"]))
        cid += 1

# ---------- 生成 HTML ----------
scene_divs = []
for (sid, start, dur) in clips:
    z = 10 + sid
    cls = SCENE_CLASS[sid]
    scene_divs.append(
        f'<div id="s{sid}" class="scene clip {cls}" style="z-index:{z}" '
        f'data-start="{start}" data-duration="{dur}" data-track-index="{sid}">\n{SCENE_HTML[sid]}\n</div>'
    )

cap_divs = []
for (cidn, start, dur, text) in caps:
    cap_divs.append(
        f'<div id="{cidn}" class="cap clip" data-start="{start}" data-duration="{dur}" data-track-index="8">'
        f'<span class="cap-in">{html.escape(text)}</span></div>'
    )

# GSAP 时间线
tl_lines = []
for (sid, start, dur) in clips:
    # 场景叠化入场（透明度），最后一场景额外做收尾淡出
    tl_lines.append(f'tl.from("#s{sid}", {{opacity:0, duration:{XFADE}, ease:"power1.out"}}, {start});')
    for (sel, vars_, off) in entrances(sid):
        vj = json.dumps(vars_, ensure_ascii=False)
        tl_lines.append(f'tl.from("{sel}", {vj}, {round(start+off,3)});')
# 末场景收尾淡出（唯一允许的退出动画）
last_sid, last_start, last_dur = clips[-1]
fade_at = round(last_start + last_dur - 0.5, 3)
tl_lines.append(f'tl.to("#s{last_sid}", {{opacity:0, duration:0.5, ease:"power1.in"}}, {fade_at});')
# 字幕入场
for (cidn, start, dur, text) in caps:
    tl_lines.append(f'tl.from("#{cidn} .cap-in", {{opacity:0, y:22, duration:0.22, ease:"power2.out"}}, {start});')

TL = "\n      ".join(tl_lines)
SCENES = "\n\n    ".join(scene_divs)
CAPS = "\n    ".join(cap_divs)
ROOT_DUR = round(TOTAL + TAIL, 3)

CSS = """
    *{margin:0;padding:0;box-sizing:border-box}
    html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#2a2336;
      font-family:"Yuanti SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC","Source Han Sans SC",sans-serif}
    :root{--bg:#efe7d6;--cream:#f3ecdb;--ink:#4a4636;--ink2:#8a8470;
      --purpleD:#6a4fd0;--greenD:#3f9a3f;--blueD:#3f6fd0;--orangeD:#d8821c;--yellow:#f6c945}
    .scene{position:absolute;top:0;left:0;width:1920px;height:1080px;overflow:hidden}
    .slide{padding:70px 90px;display:flex;flex-direction:column;
      background:#efe7d6;background-image:radial-gradient(rgba(255,255,255,.45) 1px,transparent 1px);background-size:8px 8px}
    .shead{display:flex;align-items:center;gap:26px;margin-bottom:38px}
    .badge{width:96px;height:96px;border-radius:50%;display:flex;align-items:center;justify-content:center;
      font-weight:900;font-size:48px;color:#fff;flex:none;
      box-shadow:0 12px 22px rgba(0,0,0,.18),inset 0 6px 9px rgba(255,255,255,.45),inset 0 -9px 14px rgba(0,0,0,.20)}
    .b-purple{background:linear-gradient(160deg,#9b80ee,#7a5ce0)}
    .b-green{background:linear-gradient(160deg,#74c474,#4fa84f)}
    .b-blue{background:linear-gradient(160deg,#72a0f2,#4f7fe0)}
    .b-orange{background:linear-gradient(160deg,#f5b65c,#e08f2c)}
    .htitle{font-weight:900;letter-spacing:.5px;line-height:1.2;font-size:62px;
      -webkit-text-stroke:4px #fff;paint-order:stroke fill;text-shadow:0 4px 0 rgba(0,0,0,.10),0 7px 11px rgba(0,0,0,.08)}
    .t-purple{color:var(--purpleD)}.t-green{color:var(--greenD)}.t-blue{color:var(--blueD)}.t-orange{color:var(--orangeD)}
    .sbody{flex:1;display:flex;flex-direction:column;justify-content:center}
    .claycard{background:var(--cream);border-radius:40px;padding:50px 56px;
      box-shadow:inset 0 5px 12px rgba(255,255,255,.8),inset 0 -8px 16px rgba(170,150,110,.16),0 16px 30px rgba(150,128,80,.14)}
    .steps{display:flex;flex-direction:column;gap:30px}
    .steprow{display:flex;align-items:center;gap:36px;background:var(--cream);border-radius:34px;padding:30px 46px;
      box-shadow:inset 0 5px 11px rgba(255,255,255,.8),inset 0 -6px 12px rgba(170,150,110,.16),0 12px 22px rgba(150,128,80,.10)}
    .steprow .stitle{font-size:52px;font-weight:800;color:var(--ink)}
    .steprow .sdesc{margin-left:auto;font-size:31px;font-weight:700;color:var(--ink2);text-align:right;line-height:1.25}

    /* 视觉页(封面/CTA) */
    .cover{background:#5a4a8c url("bg-cover.png") center center/cover no-repeat;
      display:flex;flex-direction:row;align-items:center;justify-content:flex-start}
    .cover::before{content:"";position:absolute;inset:0;
      background:linear-gradient(90deg,rgba(74,58,138,.62) 0 30%,rgba(74,58,138,.30) 48%,transparent 64%)}
    .cover-text{position:relative;z-index:2;margin-left:112px;max-width:880px}
    .cv-badge{display:inline-block;background:#6a4fd0;color:#fff;font-size:34px;font-weight:800;
      padding:13px 30px;border-radius:22px;margin-bottom:34px;box-shadow:inset 0 3px 7px rgba(255,255,255,.28),0 9px 16px rgba(40,25,90,.4)}
    .cv-title{font-size:130px;font-weight:900;color:#fff;line-height:1.04;
      -webkit-text-stroke:9px #5a3fc0;paint-order:stroke fill;text-shadow:0 8px 0 rgba(70,45,160,.55),0 15px 22px rgba(40,28,110,.45)}
    .cv-title.s2{font-size:104px}
    .cv-title .em{color:var(--yellow);-webkit-text-stroke:9px #c98a14}
    .cv-line2{font-size:66px;font-weight:900;color:#fff;line-height:1.1;margin-top:22px;
      -webkit-text-stroke:5px #5a3fc0;paint-order:stroke fill;text-shadow:0 6px 14px rgba(40,28,110,.4)}
    .cv-line2 .em{color:var(--yellow);-webkit-text-stroke:5px #c98a14}
    .cv-sub{display:inline-block;background:rgba(255,255,255,.18);color:#fff;font-size:40px;font-weight:700;
      padding:15px 34px;border-radius:24px;box-shadow:inset 0 0 0 3px rgba(255,255,255,.28)}

    /* P2 滚动窗口 */
    .win-card{padding:54px 60px}
    .win-row{display:flex;align-items:center;gap:40px}
    .msg-chip{flex:none;width:300px;background:linear-gradient(160deg,#72a0f2,#4f7fe0);color:#fff;
      font-size:38px;font-weight:800;text-align:center;line-height:1.3;padding:30px 24px;border-radius:30px;
      box-shadow:0 12px 22px rgba(50,80,180,.28),inset 0 4px 8px rgba(255,255,255,.3)}
    .win-arrow{flex:none;font-size:76px;color:var(--purpleD);font-weight:900}
    .win-bar-wrap{flex:1}
    .win-bar-label{display:inline-block;background:#6a6152;color:#fff;font-size:32px;font-weight:800;padding:8px 26px;border-radius:18px;margin-bottom:18px}
    .win-bar{position:relative;height:130px;border-radius:26px;background:#e7dfcd;box-shadow:inset 0 5px 12px rgba(150,128,80,.22);overflow:hidden}
    .win-fill{position:absolute;left:0;top:0;bottom:0;width:100%;background:linear-gradient(90deg,#74c474,#f5b65c 70%,#ec7a5a);opacity:.92}
    .win-ticks{position:absolute;inset:0;display:flex;justify-content:space-between;align-items:flex-end;padding:0 4px 12px;pointer-events:none}
    .win-ticks span{font-size:30px;font-weight:800;color:#fff;text-shadow:0 2px 4px rgba(0,0,0,.35)}
    .win-note{margin-top:34px;font-size:42px;font-weight:700;color:var(--ink);text-align:center}
    .win-note b{color:var(--purpleD)}
    .win-hint{margin-top:14px;font-size:34px;font-weight:700;color:var(--ink2);text-align:center}

    /* P3 金句 */
    .quote-slide{align-items:center;justify-content:center;text-align:center;
      background:linear-gradient(150deg,#9b80ee 0%,#7155d6 100%)}
    .quote-wrap{max-width:1520px;padding:0 80px}
    .q-small{font-size:50px;font-weight:800;color:rgba(255,255,255,.9)}
    .q-big{font-size:118px;font-weight:900;color:#fff;line-height:1.1;margin:14px 0 6px}
    .q-big .qy{color:var(--yellow)}
    .q-mid{font-size:54px;font-weight:800;color:rgba(255,255,255,.95)}
    .q-arrow{font-size:60px;color:rgba(255,255,255,.85);margin:10px 0}
    .q-concl{margin-top:34px;font-size:78px;font-weight:900;color:#fff;line-height:1.18;
      -webkit-text-stroke:3px rgba(90,63,192,.55);paint-order:stroke fill}
    .q-concl .qy{color:var(--yellow);-webkit-text-stroke:3px #c98a14}

    /* P4 对比时间轴 */
    .cmp-body{justify-content:center;gap:18px}
    .lane{display:flex;align-items:center;gap:30px}
    .lane-label{flex:none;width:230px;font-size:40px;font-weight:900;text-align:center;padding:18px 0;border-radius:24px;color:#fff;
      box-shadow:0 10px 18px rgba(0,0,0,.16),inset 0 4px 8px rgba(255,255,255,.3)}
    .lane-label.bad{background:linear-gradient(160deg,#f0826f,#dc5340)}
    .lane-label.good{background:linear-gradient(160deg,#74c474,#4fa84f)}
    .track{position:relative;flex:1;height:128px}
    .seg{position:absolute;top:0;bottom:0;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;
      font-size:29px;font-weight:800;line-height:1.2;border-radius:20px;padding:0 8px;
      box-shadow:inset 0 4px 9px rgba(255,255,255,.28),0 8px 15px rgba(0,0,0,.14)}
    .seg.used{background:linear-gradient(160deg,#74c474,#4fa84f)}
    .seg.idle{background:repeating-linear-gradient(45deg,#e06a56 0 22px,#cf5641 22px 44px)}
    .seg.win1{background:linear-gradient(160deg,#9b80ee,#7a5ce0)}
    .seg.win2{background:linear-gradient(160deg,#72a0f2,#4f7fe0)}
    .core{position:absolute;top:-16px;bottom:-16px;border:6px dashed var(--yellow);border-radius:24px;display:flex;align-items:flex-start;justify-content:center}
    .core span{transform:translateY(-46px);background:var(--yellow);color:#7a5a08;font-size:28px;font-weight:900;padding:7px 22px;border-radius:18px;white-space:nowrap;box-shadow:0 8px 14px rgba(180,140,20,.3)}
    .ruler{position:relative;height:40px;margin:4px 0 4px 260px}
    .ruler span{position:absolute;transform:translateX(-50%);font-size:28px;font-weight:800;color:var(--ink2)}
    .pin{position:absolute;top:-50px;transform:translateX(-50%);background:#4a4636;color:#fff;font-size:25px;font-weight:800;padding:7px 18px;border-radius:16px;white-space:nowrap}
    .pin::after{content:"";position:absolute;left:50%;top:100%;transform:translateX(-50%);border:9px solid transparent;border-top-color:#4a4636}

    /* P5 步骤 */
    .snum{width:104px;height:104px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;font-size:54px;font-weight:900;color:#fff;
      box-shadow:0 12px 22px rgba(0,0,0,.18),inset 0 6px 9px rgba(255,255,255,.45),inset 0 -9px 14px rgba(0,0,0,.20)}
    .step-foot{margin-top:30px;text-align:center;font-size:38px;font-weight:800;color:var(--purpleD)}
    .step-foot .hl{background:var(--yellow);color:#7a5a08;padding:4px 18px;border-radius:14px}
    .scmd{font-family:"SF Mono",Menlo,monospace;background:#2c2a36;color:#7ccb7c;font-size:30px;font-weight:600;padding:6px 16px;border-radius:12px;margin-left:8px}

    /* P6 注意 */
    .warn-body{justify-content:center;gap:40px}
    .warn-card{display:flex;align-items:center;gap:40px;padding:46px 54px}
    .warn-ic{flex:none;width:128px;height:128px;border-radius:32px;display:flex;align-items:center;justify-content:center;font-size:70px;
      background:linear-gradient(160deg,#f5b65c,#e08f2c);box-shadow:0 12px 22px rgba(180,140,20,.3),inset 0 4px 8px rgba(255,255,255,.4)}
    .warn-ic.moon{background:linear-gradient(160deg,#9b80ee,#7a5ce0)}
    .warn-t{font-size:54px;font-weight:900;color:var(--ink)}
    .warn-d{font-size:36px;font-weight:700;color:var(--ink2);margin-top:8px;line-height:1.3}

    /* 字幕 */
    .cap{position:absolute;left:0;right:0;bottom:54px;text-align:center;z-index:100}
    .cap-in{display:inline-block;max-width:1500px;background:rgba(26,20,42,.82);color:#fff;
      font-size:46px;font-weight:800;line-height:1.34;padding:16px 40px;border-radius:22px;
      box-shadow:0 10px 26px rgba(0,0,0,.32);text-shadow:0 2px 6px rgba(0,0,0,.4)}
"""

DOC = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{ROOT_DUR}" data-width="1920" data-height="1080">

    {SCENES}

    {CAPS}

    <audio id="vo" data-start="0" data-duration="{ROOT_DUR}" data-track-index="9" src="narration.wav" data-volume="1"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {TL}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

open("index.html", "w", encoding="utf-8").write(DOC)
print(f"index.html 生成完毕：根时长 {ROOT_DUR}s，{len(clips)} 场景，{len(caps)} 条字幕，{len(tl_lines)} 条 tween")
for (sid, start, dur) in clips:
    print(f"  S{sid}: start {start:.2f}  dur {dur:.2f}")
