# game
菊建ページ内のゲーム開発

## メモ
- `index.html` … 1人用「菊建クラッシャー」。2026-11-13 から、アームの先のハサミをキャラクター「キクペディア」（2026-11-14 に「ガブ」→「キクリン」→「キクペディア」と名前を変えた）（菊建ボットの顔）に変えた（`drawNibbler`）。前のハサミの絵は `drawNibblerClassic` に残してある（戻すときは `drawExcavator` の中の呼び先を変える）。重機と運転席の先代社長はそのまま
- `taisen/`・`taisen3d/` … 対戦版。2026-11-14 に、こちらもアームの先をキクペディアに変えた。色は機体の色（P1ピンク・P2青）。平面の絵は `drawCrusher`（前のハサミは `drawCrusherClassic`）。対戦3Dの立体は `buildMachine3d` の中の「キクペディア」の所（丸い体の上半分＝上あご・下半分＝下あごが開く）

## キクペディアの部屋（room/）

3Dのキクペディアが部屋の中を歩き回るページ（2026-11-13）。https://kikukenkogyo.github.io/game/room/

- コンクリートを見つけると食べに行く。押すと反応して、ひとこと話す。床を押すと、そこにコンクリートが落ちてくる
- `?kanban=1` を付けると、ボタンを消した「映しっぱなし用」（事務所の電子黒板など）
- セリフは room/index.html の LINES / EAT_LINES / POKE_LINES に足すだけ（丁寧語＋「！」）
- 2026-11-18：キャラを、ほかのキクペディアと同じ「5番基準」の顔（まゆ毛なし・足なし）に入れかえた（酒井さん「イメージと違う。水玉が後ろがちょっと多すぎ。ほかのキクペディアと同じ感じに」）。背中の水玉は半分。足がないので、はねて進む。押すと、にっこり／キラキラの顔になる
  - 立体データ：room/model/k0・k1・k2（口の開き3段）・kblink・knikori・kkira。作り方は room/index.html の頭の説明（kikuken-line-bot の make_chara3d.py で、顔の名前の最後に `_room` を付けて書き出す）
  - 前の形（足つき）は room/model/room0〜2.glb に残してある（使っていない）
- 2026-11-18：前に作った動き（ハート目・ブチッ・溶断・ドジ消火器）を、押したとき（4割くらい）と、40〜70秒に1回、その場で見せる。絵は room/fx/*.webp（コマを並べた物）。作り直す・足すときは `python room/tools/make_fx_sheets.py`（元のコマは kikuken-line-bot\docs\chara3d\k5）→ room/index.html の `FX` に fx/fx.json の中身とセリフを書く
- 手元で見るとき：`python -m http.server 8767 --directory C:\Users\shuta\Documents\game` → http://localhost:8767/room/
