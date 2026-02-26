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
　　　rr 18 y 10   # y軸に周りに10°回転 (rotation) を 18回<br>
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
<img src="images/manual_edit.gif"><br>
<br>
<strong>　回転・スケーリング・平行移動 [インタラクティブ版]</strong><br>
<br>
　　使い勝手が悪すぎたので, インタラクティブ版を作ってみた<br>
<br>
　　[0] 起動：python src\PLY_interactive.py<br>
<img src="images/00.png"><br>
　　コンソール画面からコマンドを入力する。<br>
　　[1] PLYファイルロード：　load data\ring_100.ply<br>
<img src="images/01.png"><br>
　　[2] 回転コマンド：r 0 10 0 18<br>
　　　　y軸周りに10°回転を18回繰り返す。<br>
<img src="images/02.png"><br>
　　[3] 座標軸を消す：axis<br>
　　　　axisを入力するたびに, 座標軸を消す→表示するをトグルする。<br>
<img src="images/03.png"><br>
　　[4] PLYをセーブする：save ball.ply<br>
<br>
　　[5] メッシュを削除する：del<br>
<img src="images/00.png"><br>
　　[6] PLYファイルロード：　load data\ring_100.ply<br>
<img src="images/01.png"><br>
　　[7] 回転/スケーリング/平行移動コマンド：g s 1 0.9 0.9 t 0 -0.5 0 r 20 0 0 t 0.1 0.5 0 30<br>
　　　　　グループコマンド<br>
　　　　　　① y-z平面で0.9倍にスケーリング<br>
　　　　　　② y方向に-0.5平行移動<br>
　　　　　　③ x軸周りに20°回転<br>
　　　　　　④ y方向に+0.5 x方向に+0.1<br>
　　　　　①～④を30回繰り返す。<br>
<img src="images/05.png"><br>
　　[8] Undo：u<br>
<img src="images/01.png"><br>
　　[9] 終了：quit<br>
　　　　　Open3D の Visualizer画面を選んでESCキー押下でも終了する。
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
<h3>PLY interactive つづき</h3>
<p>
　デバッグできていないのに、機能追加･･･<br>
<br>
　<strong>多角形メッシュ生成</strong><br>
　　polygon (辺の数) [(サイズ) (高さ)]<br>
　　POLYGON (辺の数) [(サイズ) (高さ)]<br>
<br>
　(例) polygon 5<br>
　　　 サイズ(外接円の半径)のデフォルトは 1<br>
　　　 高さを指定しないと 0 (平板)<br>
<img src="images/10.png"><br>
　(例) polygon 5 1 0.2<br>
　　　高さを指定すると柱になる(厚みがでる)<br>
<img src="images/11.png"><br>
　　　Open3D の Visualizer画面をクリックして wキーを押下するとワイヤーフレームを表示してくれる。<br>
　　　(座標軸や文字もワイヤーフレーム表示になってしまうが･･･)<br>
<img src="images/12.png"><br>
　　(例) select<br>
　　　　　select from  ['', 'polygon5_side', 'polygon5_top', 'polygon5_bottom']<br>
<br>
　　　　小文字版のコマンド(polygon)の場合、天板、底面、側面が別々のメッシュになっている。<br>
　　　　個別に操作できるが、メッシュ選択やマージ機能がちゃんとできていないので不便。<br>
　　　　削除する場合も d コマンドを3回実行する必要あり。<br>
<br>
　　(例) select polygon5_side<br>
　　　　 r 30 0 0<br>
<img src="images/13.png"><br>

　　大文字版のコマンド(POLYGON)だと全体が1個のメッシュになる。<br>
　　(例) POLYGON 5 1 0.2<br>
　　　　 r 30 0 0<br>
<img src="images/14.png"><br>　

　　高さにマイナスを指定すると側面だけになる。<br>
　　(例) polygon 5 1 -0.2<br>
<img src="images/15.png"><br>　
　　(例)正12面体を作る。<br>
　　　　一辺をz軸に揃える： t -np.cos(np.deg2rad(36)) 0 0<br>
<img src="images/16.png"><br>　
　　　　z軸に沿って折り曲げる(五角形を起こす)：r 0 0 -63.5<br>
<img src="images/17.png"><br>　
　　　　回転したときに底辺が五角形になるように平行移動する：t -np.cos(np.deg2rad(36)) 0 0<br>
<img src="images/18.png"><br>　
　　　　y軸周りに72°回転を5回繰り返す：r 0 72 0 5<br>
<img src="images/19.png"><br>
　　　　正12面体の半分を一旦セーブ：save dodecahedron_half.ply<br>
<br>
　　　　裏返しにする：r 0 0 180<br>
<img src="images/20.png"><br>　
　　　　下半分をロードする前に持ち上げる：t 0 np.sin(np.deg2rad(36))*np.sin(np.deg2rad(63.5))*5 0<br>
<img src="images/21.png"><br>　
　　　　下半分をロードする：l dodecahedron_half.ply<br>
<br>
<img src="images/22.png"><br>　
</p>
</body>
</html>