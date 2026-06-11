#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把口播分段用 Kokoro(zf_xiaobei) 中文 TTS 合成 narration.wav，并产出场景/字幕时序 manifest.json。
中文 G2P 走 misaki[zh]（hyperframes 自带 CLI 的 espeak 后端不支持 zh）。"""
import sys, json, re
import numpy as np
import soundfile as sf
import kokoro_onnx
from misaki import zh

MODEL = "/Users/aehyok/.cache/hyperframes/tts/models/kokoro-v1.0.onnx"
VOICES = "/Users/aehyok/.cache/hyperframes/tts/voices/voices-v1.0.bin"
VOICE = "zf_xiaobei"
SR = 24000
GAP_SENT = 0.18     # 句间停顿
GAP_SCENE = 0.42    # 场景(段)间停顿

# en_callable：英文片段尽量用 misaki.en 正确发音；不可用就原样透传（草稿可接受）
en_callable = None
try:
    from misaki import en as _en
    _eng = _en.G2P(british=False, fallback=None)
    def en_callable(t):
        ph, _ = _eng(t)
        return ph
    print("[en] misaki.en G2P 已启用", file=sys.stderr)
except Exception as e:
    print(f"[en] misaki.en 不可用，英文片段原样透传：{e}", file=sys.stderr)

g2p = zh.ZHG2P(en_callable=en_callable)
model = kokoro_onnx.Kokoro(MODEL, VOICES)

# 仅用于「念稿」的英文专名音译（字幕/屏上字保持正确英文）。长键先替换避免子串误伤。
TTS_SUBS = [("Codex", "扣德克斯"), ("AI少年", "诶艾少年"), ("AI", "诶艾")]
def tts_text(s):
    for k, v in TTS_SUBS:
        s = s.replace(k, v)
    return s

# 7 段口播（对齐 deck 7 页）。文本为「念稿」，屏上字幕单独维护以保英文专名准确。
SCENES = [
    # i, 念稿
    "用 Codex 的朋友，是不是经常干到一半，啪一下撞到限额，剩下的时间只能干瞪眼？今天教你一个零成本的小设置，让额度变相翻倍。大家好，我是 AI少年。",
    "先说原理。Codex 的额度不是每天重置的，而是一个五小时的滚动窗口。你发出第一条消息那一刻，五小时就开始倒计时。",
    "关键在这儿：窗口走完，系统不会自动给你开下一个，它会一直等，等你发下一条消息才重新计时。也就是说，这个重置时间，其实是你自己能控制的。",
    "举个例子。你习惯下午两点开工，两点一发消息，窗口就从两点算到晚上七点。可你手速一快，三点半额度就见底了，剩下三个半小时只能干等。但要是上午十一点先随手发一条，窗口就从十一点开始、下午四点就重置，你两点干到四点额度又刷新一波，四点之后又是一个全新窗口。等于两点到六点这段核心时间，你白嫖了两个额度窗口。",
    "怎么让它自动发生？打开 Codex 的自动化，点右上角从聊天创建，跟它说一句，每天上午九点跟我说声你好，存下来就行。以后它每天九点自动发一条，帮你把窗口提前点亮，设一次长期生效。",
    "还有一个很多教程不会告诉你的坑：这个自动化是跑在本地的，得让电脑一直开着、Codex 一直运行它才会执行。所以记得在系统里打开防止睡眠。",
    "AI 的事，听 AI少年 说，关注我，咱们下期接着聊。",
]

def split_sents(t):
    parts = re.split(r'(?<=[。！？])', t)
    return [p.strip() for p in parts if p.strip()]

def synth(text):
    ph, _ = g2p(text)
    samples, sr = model.create(ph, voice=VOICE, speed=1.0, is_phonemes=True)
    return np.asarray(samples, dtype=np.float32)

def silence(sec):
    return np.zeros(int(SR * sec), dtype=np.float32)

audio = []
cursor = 0.0
manifest = {"sampleRate": SR, "voice": VOICE, "scenes": []}

for i, scene_text in enumerate(SCENES):
    sents = split_sents(scene_text)
    scene_start = cursor
    cap_units = []
    for j, s in enumerate(sents):
        wav = synth(tts_text(s))
        dur = len(wav) / SR
        cap_units.append({"text": s, "start": round(cursor, 3), "dur": round(dur, 3)})
        audio.append(wav)
        cursor += dur
        if j < len(sents) - 1:
            audio.append(silence(GAP_SENT)); cursor += GAP_SENT
    scene_dur = round(cursor - scene_start, 3)
    manifest["scenes"].append({
        "scene": i + 1,
        "start": round(scene_start, 3),
        "dur": scene_dur,
        "captions": cap_units,
    })
    print(f"  场景{i+1}: {scene_dur:.2f}s  ({len(sents)} 句)", file=sys.stderr)
    if i < len(SCENES) - 1:
        audio.append(silence(GAP_SCENE)); cursor += GAP_SCENE

full = np.concatenate(audio)
manifest["totalDuration"] = round(len(full) / SR, 3)
sf.write(sys.argv[1], full, SR)
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"总时长 {manifest['totalDuration']:.2f}s -> {sys.argv[1]}", file=sys.stderr)
