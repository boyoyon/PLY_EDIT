<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
<h1><center>PLY Editor</center></h1>
<h2>なにものか？</h2>
<p>
　簡単な形状のPLY(プリミティブ)作成と、それを回転・スケーリング・平行移動するだけのエディターです。
</p>

<h3>環境構築</h3>
<p>
　pip install Open3D
<p>

<h3>プリミティブ作成</h3>

<p>
　<strong>リングの作成</strong><br>
　　python src\createRing.py (分割数) (サイズ) (幅) (表面色) (裏面色)<br>
<br>
　(例１)<br>
　　python src\createRing.py  100  1  0.01  0  0  255  200  200  255<br>
<br>
　　　y-z 平面上にリング(100角形)を作成。サイズ(半径)は 1, 幅は 0.01。<br>
　　　表面は濃い青(0 0 255), 裏面は薄い青(200 200 255)。<br>
<img src="images/ring_100.gif">
<br>
　(例２)<br>
　　python src\createRing.py 5  1  0.01  0  0  255  200  200  255<br>
<br>
　　　y-z 平面上にリング(5角形)を作成。サイズ(半径)は 1, 幅は 0.01。<br>
　　　表面は濃い青(0 0 255), 裏面は薄い青(200 200 255)。<br>
<img src="images/ring_5.gif">
<br>
　<strong>白黒リングの作成</strong><br>
　　python src\createRingBW.py (分割数) (サイズ) (幅)<br>
<br>
　(例１)<br>
　　python src\createRingBW.py  100  1  0.01<br>
<br>
　　　y-z 平面上にリング(100角形)を作成。サイズ(半径)は 1, 幅は 0.01。<br>
<img src="images/ringBW_100.gif">
</p>

<h3>PLY編集</h3>
<p>
<strong>　回転・スケーリング・平行移動</strong><br>
<br>
　プリミティブ PLY を回転・スケーリング・平行移動して PLYを作成する。<br>
　python src\PLY_RST.py (プリミティブPLY) (手順)<br>
<br>
　(例１)<br>
　　python src\PLY_RST.py data\ring_100.ply data\手順_りんご.txt<br>
<br>
　　(手順_りんご.txt)<br>
　　　s 1 1 0.5    # z 方向に 0.5倍 (scaling)<br>
　　　t 0 0 0.6    # z 方向に 0.6移動 (translation)<br>
　　　rr 36 y 10   # y軸に周りに10°回転 (rotation) を 36回<br>
　　　apple.ply    # apple.plyとしてセーブ<br>
<br>
　　　※ 手順ファイルの # 以降は無視されます。<br>
<br>
<img src="images/apple.png">
<br>
　(例２)<br>
　　python src\PLY_RST.py data\ring_100.ply data\手順_砂時計.txt<br>
<br>
　　(手順_砂時計.txt)<br>
　　　s 1 1 0.3　　  # z方向に0.3倍<br>
　　　r z 45　　　　 # z軸周りに45°回転<br>
　　　rr 36 x 10　　 # x軸周りに10°回転を36回<br>
　　　hourglass.ply　# hourglass.ply としてセーブ<br>
<img src="images/hourglass.png">
<br>
　(例３)<br>
　　python src\PLY_RST.py data\ring_100.ply data\手順_螺旋.txt<br>
<br>
　　(手順_螺旋.txt)<br>
　　　g 10 t 0 -1.5 0 r x 36 t 0.5 1.5 0　# (移動→回転→移動)をグループとして10回実行<br>
　　　spiral.ply　　　　　　　　　　# spiral.ply としてセーブ<br>
<img src="images/spiral.gif">
<br>
<strong>　回転・スケーリング・平行移動＋マージ</strong><br>
<br>
　　回転・スケーリング・平行移動で複数の PLY を作成し、<br>
　　① python src\PLY_RST.py (プリミティブPLY) (手順)<br>
<br>
　　１つのPLYにマージする。<br>
　　② python src\merge_mesh_plys.py (PLYファイルへのワイルドカード(例：*.PLY))<br>
　　　　または<br>
　　②'python src\merge_mesh_plys.py (PLYファイル1) (PLYファイル2) ･･･<br>
<br>
　　(例１)<br>
　　　① python src\PLY_RST.py data\ring_100.ply data\手順_二枚貝.txt<br>
<br>
　　　(手順_二枚貝.txt)<br>
　　　　s 1 0.5 0.5<br>
　　　　r z -18<br>
　　　　t -np.sin(np.deg2rad(18))*0.5 0 0<br>
　　　　01.ply<br>
<br>
　　　　s 1 0.5 0.5<br>
　　　　r z 18<br>
　　　　t np.sin(np.deg2rad(18))*0.5 0 0<br>
　　　　02.ply<br>
<br>
　　　※数値の部分に np(numpy) を使った式を使うことができます。<br>
　　　　ただし, スペースを含めることはできません。<br>
<br>
　　　② python src\merge_mesh_plys.py *.ply<br>
<br>
　　　※ マージされた PLY が merged.ply に出力されます。<br>
<img src="images/clams.gif"＞<br>
<br>
<strong>　手動で複数の PLY の位置関係を調整</strong>
<br>
　　python PLY_manual_edit.py (PLYファイル1) (PLYファイル2)<br>
<br>
　　1/2/3/4/5/6キーで PLY2 を回転、平行移動する。<br>
　　Shiftキーで逆方向に回転, 平行移動。<br>
　　7/8キー、Shift+7/Shift+8キーで回転量、平行移動量を増減。<br>
　　Ctrlキーで回転量, 平行移動量を大きくする。<br>
　　ESCキーを押下するとプログラム終了。マージされた結果が merged.ply に出力される。<br>
<img src="images/manual_edit.gif">
</p>

<h3>PLY表示</h3>
<p>
　python src\o3d_display_mesh.py (PLY) [-normal]<br>
<br>
　　-normal/指定せず： 　　　　　　 法線を計算する/しない<br>
　　マウスドラッグ: 　　　　　　　　モデルを回転する<br>
　　ホィールボタン押下＋ドラッグ：　モデルを移動する<br>
　　ホィールを回す：　　　　　　　　モデルの拡大、縮小<br>
　　＠キー/[キー押下：　　　　　　　画角変更<br>
　　pキー押下：　　　　　　　　　　 スクリーンキャプチャー<br>
　　1キー/Shift+1キー押下：　　　　 モデルの回転(x軸周り)<br>
　　2キー/Shift+1キー押下：　　　　 モデルの回転(y軸周り)<br>
　　3キー/Shift+1キー押下：　　　　 モデルの回転(z軸周り)<br>
　　4キー/Shift+1キー押下：　　　　 モデルの移動(x軸方向)<br>
　　5キー/Shift+1キー押下：　　　　 モデルの移動(y軸方向)<br>
　　6キー/Shift+1キー押下：　　　　 モデルの移動(z軸方向)<br>
　　7キー/Shift+7キー押下：　　　　 回転量を下げる/上げる<br>
　　8キー/Shift+8キー押下：　　　　 移動量を下げる/上げる<br>
    Ctrlキー＋1/2/3/4/5/6キー：　　 回転量, 移動量を大きくする<br>
　　↑キー/↓キー押下:　　　　　　　モデルのスケーリング<br>
　　ESCキー押下：　　　　　　　　　プログラム終了<br>
<br>
　python src\o3d_display_mesh_animate.py (PLY) [-normal]<br>
<br>
　　回転しつづける<br>
　　1～9キー,↑キー, ↓キーは効かない。
</p>

</body>
</html>