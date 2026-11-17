# -*- coding: utf-8 -*-
"""キクペディアの部屋に入れる「動き」（ハート目・ブチッ・溶断・ドジ消火器）を、1枚の絵（コマを並べた物）にまとめる。2026-11-18 酒井さん
  「この前ちょこっと作ったアニメーションも入れてもいいかも。ガス切りしてるやつ、頭が爆発するやつ、ハートになるやつ」
  ・元のコマ（背景が透けた絵）は kikuken-line-bot\\docs\\chara3d\\k5 にある（Blender で作った物）
  ・全部のコマで絵が入っている範囲だけを切り出し、CELL の大きさにそろえて並べる → room\\fx\\名前.webp
  ・体（ピンクの丸）の真ん中と半径を1コマ目から測って、fx.json に書く（部屋の中で、立体のキャラと同じ大きさ・同じ場所に重ねるため）
使い方: python room/tools/make_fx_sheets.py
"""
import os, json, glob, math
from PIL import Image, ImageSequence

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(HERE), 'fx')
K5 = os.path.join(os.path.expanduser('~'), 'Documents', 'kikuken-line-bot', 'docs', 'chara3d', 'k5')
CELL = 360


def gif_dur(name):
    return [f.info.get('duration', 80) for f in ImageSequence.Iterator(Image.open(os.path.join(K5, name)))]


def holds(act):
    return [int(l.rstrip('\n').split('\t')[5]) * 83 for l in open(os.path.join(K5, 'fx', 'list.txt'), encoding='utf-8') if l.split('\t')[0] == act]


def heart_files():
    d = os.path.join(K5, 'heart', 'anim3')
    names = ['base'] + [f'g{i:02d}' for i in range(16)] + [f'f{i:02d}' for i in range(46)] + [f's{i:02d}' for i in range(16)] + [f'z{i:02d}' for i in range(10)] + ['base']
    return [os.path.join(d, n + '.png') for n in names]


ANIMS = [   # 名前, コマの絵, 1コマの長さ（ミリ秒）, 何コマおきに使うか
    ('heart', heart_files(), gif_dur('キクペディア_ハート目.gif'), 2),
    ('buchi', sorted(glob.glob(os.path.join(K5, 'fx', 'buchi', '[0-9]*.png'))), holds('buchi'), 1),
    ('yodan', sorted(glob.glob(os.path.join(K5, 'fx', 'yodan', '[0-9]*.png'))), holds('yodan'), 1),
    ('doji', [os.path.join(K5, 'doji', l.split()[0] + '.png') for l in open(os.path.join(K5, 'doji', 'list.txt'), encoding='utf-8') if l.strip()], gif_dur('キクペディア_ドジ_消火器.gif'), 1),
]


def body(im):
    """体（濃いピンクの丸）の真ん中と半径を測る"""
    px = im.load(); w, h = im.size; xs = []; ys = []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b, a = px[x, y]
            if a > 200 and r > 190 and g < 120 and 90 < b < 200 and r - g > 110: xs.append(x); ys.append(y)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    return (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) / 2


os.makedirs(OUT, exist_ok=True); meta = {}
for name, files, durs, step in ANIMS:
    assert len(files) == len(durs), (name, len(files), len(durs))
    ims = [Image.open(f).convert('RGBA') for f in files]
    # 何コマおきに使う（抜いたコマの長さは、前のコマに足す）。最初と最後のコマは必ず残す
    keep = sorted(set(list(range(0, len(ims), step)) + [len(ims) - 1])); fr = []; du = []
    for a, b in zip(keep, keep[1:] + [len(ims)]):
        fr.append(ims[a]); du.append(sum(durs[a:b]))
    # 絵が入っている範囲（全部のコマを合わせた物）を、正方形に
    bx = [im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox() for im in fr]
    x0 = min(b[0] for b in bx); y0 = min(b[1] for b in bx); x1 = max(b[2] for b in bx); y1 = max(b[3] for b in bx)
    side = max(x1 - x0, y1 - y0) + 12; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    L, T = int(round(cx - side / 2)), int(round(cy - side / 2))
    bcx, bcy, br = body(fr[0])
    cols = math.ceil(math.sqrt(len(fr))); rows = math.ceil(len(fr) / cols)
    sheet = Image.new('RGBA', (cols * CELL, rows * CELL), (0, 0, 0, 0))
    for i, im in enumerate(fr):
        c = Image.new('RGBA', (side, side), (0, 0, 0, 0)); c.alpha_composite(im, (-L, -T)) if L <= 0 and T <= 0 else c.paste(im.crop((max(0, L), max(0, T), max(0, L) + side, max(0, T) + side)), (max(0, -L), max(0, -T)))
        sheet.alpha_composite(c.resize((CELL, CELL), Image.LANCZOS), ((i % cols) * CELL, (i // cols) * CELL))
    p = os.path.join(OUT, name + '.webp'); sheet.save(p, 'WEBP', quality=82, method=6)
    meta[name] = dict(n=len(fr), cols=cols, rows=rows, dur=du, cx=round((bcx - L) / side, 4), cy=round((bcy - T) / side, 4), r=round(br / side, 4))
    print(name, len(fr), 'コマ', sheet.size, round(os.path.getsize(p) / 1024), 'KB', meta[name]['cx'], meta[name]['cy'], meta[name]['r'], sum(du) / 1000, '秒')
json.dump(meta, open(os.path.join(OUT, 'fx.json'), 'w', encoding='utf-8'), ensure_ascii=False)
