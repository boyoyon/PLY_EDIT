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
　pip install Open3D<br>
  pip install mapbox_earcut　･･･　img2mesh で使用
<p>

<h3>更新項目</h3>

<p>
　<strong>画像からのメッシュ作成</strong><br>
　img2mesh　(画像ファイル名)<br>
　コンソールから実行できるようにした。表, 裏の2メッシュ＋輪郭の座標がロードされる。<br>
　・背景が黒でないとうまく動作しない。<br>
　・表と裏は select してみないとわからない.<br> 
</p>
<img src="images/img2mesh2.svg">
<p>
　<strong>3D座標：　pコマンド</strong><br>
　オプションを追加<br>
　・p　centering　･･･　Points配列内の座標をセンタリングする <br>
　・p　r　xx　xx　xx　･･･　Points配列内の座標の回転 <br>
　・p　s　xx　xx　xx　･･･　Points配列内の座標のスケーリング <br>
　・p　t　xx　xx　xx　･･･　Points配列内の座標の平行移動 <br>
　・p　save　( .npyファイル名)　･･･　Points配列内の座標を .npy ファイルに保存<br>　
<br>
　※ メッシュをスケーリングすると枠が太ったり細くなったりするので必要と思って実装したが、s(スケーリング)と save 以外はメッシュ化してから従来のコマンドで実施しても同じだった･･･<br>
　　メッシュ化しないと何が起こっているのかわからない。<br>
</p>

<p>
　<strong>手書き入力：　draw コマンド</strong><br>
　draw　[(入力画面幅)　(入力画面高さ)　(モード)]<br>
　※ (今のところ)一筆書きのみ。思い付きで実装したがいまいち ･･･<br>
　　　モード指定なしだと、z 座標は 0 固定。<br>
　　　モードに 1 を指定すると z 座標は 0.01ずつ増える。<br>
</p>
<img src="images/draw.svg">
<h3>使い方</h3>

<h4>起動・終了</h4>
<p><strong>起動</strong><br>
<br>
python PLY_interactive.py [(幅) (高さ)]<br>
・引数で Visualizer 画面の幅、高さを指定可能。<br>
　起動後でもサイズ変更可能。<br>
<br>
　コンソールにコマンドを入力すると結果が Visualizer 画面に表示される。<br>
</p>
<img src="images/screen.svg">

<p>
　(基本操作) ･･･ [ ]はオプション<br>
　・m　　　　　　　　　　　　　　　　･･･　メニューを表示する<br>
　・axis　　　　　　　　　　　　　　　･･･　座標軸を消す⇔表示する<br>
　・l　(.plyファイル)　　　　　　　　　･･･　PLYファイルをロードしメッシュを表示する<br>
　・r　(x回転角)　(y回転角)　(z回転角)　･･･　メッシュを回転する<br>
　・s　(x倍率)　(y倍率)　(z倍率)　　　　･･･　メッシュを拡大/縮小する<br>
　・t　(x移動量)　(y移動量)　(x移動量)　･･･　メッシュを移動する<br>
　・merge　　　　　　　　　　　　　　･･･　メッシュをマージする<br>
　・normals　　　　　　　　　　　　　･･･　法線を計算する / 削除する。<br>
　・d　[all]　　　　　　　　　　　　･･･　メッシュを削除する。[all]は全部削除。<br>
　・u　　　　　　　　　　　　　　　　･･･　前の操作を取り消す<br>
　・cap　[ファイル名]　　　　　　　　･･･　Visualizer 画面をキャプチャーする<br>
　・save　(.plyファイル)　　　　　　　･･･　メッシュを保存する<br>
　・quit　　　　　　　　　　　　　　　･･･　終了する<br>
<br>
　※ パラメータにスペースを含めることはできない。<br>
　※ 実数値パラメータには numpy 関数(np.***) を含んだ式を指定することができる。<br>
</p>

<h4>Visualizer 画面でのキー操作</h4>
<p>
※ 元の Visualizer 操作キーは, hキー押下でコンソールに表示される。<br>
<br>
カスタマイズしたキー操作<br> 
・x　･･･　x軸方向からのビュー<br>
・y　･･･　y軸方向からのビュー<br>
・z　･･･　z軸方向からのビュー<br>
</p>
<img src="images/VisualizerCtrl.svg">
<p>
・1/2/3　･･･　カメラ位置の回転。+Shiftで逆方向回転。+Ctrlで回転量増加<br>
・4/5/6　･･･　カメラ位置の移動。+Shiftで逆方向移動。+Ctrlで移動量増加<br>
・7/8　　･･･　回転/移動ステップの増減。+Shiftで増加<br>
・↑↓　 ･･･　ズーム(6, Shtft+6と同じ)<br>
・→←　 ･･･　移動(4,Shift+4と同じ)<br>
</p>

<h4>コンソールからの Visualizer 制御</h4>
<p>
・getEyePos　･･･　カメラパラメータの取得<br>
・setEyePos　･･･　カメラパラメータの設定<br>
<br>
・cam x　　　　　　　　　　･･･　x軸方向からのビュー<br>
・cam rotate x (角度)　　　･･･　x軸周りに回転<br>
・cam rotate -x (角度)　　　･･･　x軸周りに逆回転<br>
・cam rotate x (-角度)　　　･･･　(同上)<br>
・cam translate x (移動量)　･･･　x軸方向に平行移動<br>
・cam translate -x (移動量)　･･･　x軸方向に平行移動<br>
・cam translate x (-移動量)　･･･　(同上)<br>
<br>
※ y, zについても同様のコマンドあり。<br>

</p>

<p><strong>終了</strong><br>
<br>
・Visualizer 画面で ESC キー押下<br>
　または<br>
・コンソールに quit と入力する。<br>

<h4>ロード・セーブ:　l コマンド / save コマンド</h4>

<p>
<strong>ロード</strong><br>
<br>
・l　( .ply ファイル)　･･･　PLYファイルが読み込まれ Visualize 画面に表示される。<br>
<br>
・l　( .txt ファイル)　･･･　コマンド列が記述されたファイルが読み込まれ実行される。<br>
　　　　　　　　　　　　　　※ もう一回エンターキーを押すと実行される。<br>
・l　( .npy ファイル)　･･･　座標データが読み込まれ Points[ ]に格納される。<br>
　　　　　　　　　　　　　　※ 後でPoints[ ]を使うコマンドを実行するまで外観上変化はない。

<br>
<strong>セーブ</strong><br>
<br>
・save　( .ply ファイル)　･･･　メッシュを指定されたファイルにセーブする。<br>
　　　　　　　　　　　　　　編集中のすべてのメッシュがマージされてセーブされる。
</p>

<h4>回転/スケーリング/平行移動/グループ:　r コマンド / s コマンド / t コマンド / g コマンド</h4>

<p><strong>回転</strong><br>
　r (x 軸周りの回転角度)　(y 軸周りの回転角度)　(z 軸周りの回転角度)　[(回数)]<br>
　・角度は度数(degree)で指定する。
</p>    
<img src="images/rotate.svg">
<p>
回数パラメータを指定すると, オリジナル＋(回数-1)回, 回転されたメッシュが作成される。
</p>
<img src="images/rotate2.svg">
<p><strong>スケーリング</strong><br>
　s (x 軸方向のスケーリング)　(y 軸方向のスケーリング)　(z 軸方向のスケーリング)　[(回数)]
</p>

<img src="images/scaling.svg">

<p>
回数パラメータを指定すると, オリジナル＋(回数-1)回, スケーリングされたメッシュが作成される。
</p>

<img src="images/scaling2.svg">

<p><strong>平行移動</strong><br>
　t (x 軸方向の平行移動量)　(y 軸方向の平行移動量)　(z 軸方向の平行移動量)　[(回数)]
</p> 

<img src="images/translate.svg">

<p>
回数パラメータを指定すると, オリジナル＋(回数-1)回, 平行移動されたメッシュが作成される。
</p>

<img src="images/translate2.svg">

<p><strong>グループ</strong><br>
　g 　(rコマンド/sコマンド/tコマンドの任意の並び)　[(回数)]
</p> 

<img src="images/group.svg">

<h4>正多角形:　polygon コマンド</h4>

<p style="padding-left:1em;"><strong>厚みのない正多角形</strong></p>

<p>polygon (正多角形の辺の数) [(外接円半径)･･･]</p>

<img src="images/polygon.svg">

<p style="padding-left:1em;"><strong>厚みのある正多角形</strong></p>

<p>polygon (正多角形の辺の数) [(外接円半径) (厚み)･･･]<br>
・天板, 底面,側面の 3 つのメッシュが作成される。<br>
・大文字(POLYGON)で指定すると, 天板, 底面, 側面がマージされた 1 つのメッシュが作成される。<br>
・厚みにマイナスを指定すると側面のみ(天板, 底面なし)のメッシュが生成される。</p>

<img src="images/polygon2.svg">

<p>
(例)
</p>
<img src="images/apple.svg">
<p>
(例)
</p>
<img src="images/hourglass.svg">

<p style="padding-left:1em;"><strong>正多面体</strong></p>
<p>正多角形を回転/スケーリング/平行移動することで正多面体を作る。<br>
l (スクリプト) # スクリプトファイルをロードして実行する。
</p>

<img src="images/polyhedron.svg">
<p>
<strong>(例) 回転と平行移動で正五角形から正12面体を作る</strong>
</p>
<img src="images/dodecahedron.svg"><br>
<p style="padding-left:1em;"><strong>螺旋</strong></p>
<p>
多角形の側面を作成しつつ y 軸方向に移動させることで螺旋を作ることができる。<br>
polygon (多角形の辺の数) (外接円半径) (厚み) (螺旋高さ) (回転数) (最終半径)
</p>
<img src="images/spiral0.svg">

<h4>色指定: c コマンド, 環境変数</h4>
<p>
　<strong>c コマンド</strong><br>
　　メッシュ全体を単色で塗りつぶす。<br>
　　c　(red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
<br>
　<strong>環境変数</strong><br>
　　天板・底面の表：SurfaceOuter (red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
　　天板・底面の裏：SurfaceInner (red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
<br>
　　側面の表　　　：LateralOuter (red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
　　側面の裏　　　：LateralInner (red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
<br>
　　padding の表　：PaddingOuter (red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
　　padding の裏　：PaddingInner (red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)<br>
　　※ padding については 折れ線：polyline コマンドで説明する。
</p>

<p>　(例)<br>
　　　l  data\pole.txt<br>
　　　(一部)<br>
　　　　LateralOuter 255 0 0　　　# 側面(表)を赤に設定<br>
　　　　LateralInner 255 230 230　# 側面(裏)をうすい赤に設定<br>
　　　　polygon 100 0.5 0.1 0.6 4 # 螺旋を作成<br>
　　　　save spiral_red.ply　　　 # セーブ<br>
<br>
　　　　LateralOuter 0 0 255　　　# 側面(表)を青に設定<br>
　　　　LateralInner 230 230 255　# 側面(裏)をうすい青に設定<br>
　　　　polygon 100 0.5 0.1 0.6 4 # 螺旋を作成<br>
　　　　r 0 180 0　　　　　　　　 # y 軸周りに 180°回転<br>
　　　　save spiral_blue.ply　　　# セーブ<br>

</p>
<img src="images/up.gif">

<h4>メッシュの選択:　select コマンド, selected コマンド</h4>

<p>
　以下のようにしてメッシュを選択する。(使い勝手が悪い･･･)<br>
<br>
　(例)<br>
　　l　data/pole.txt<br>
　　select　･･･　選択可能なメッシュ一覧がコンソールに表示される。<br>
<br>
　　select from  ['', 'polygon100_side', 'spiral_red', 'POLYGON100']<br>
<br>
　　名前を指定してメッシュを選択する。<br>
　　select　polygon100_side<br>
<br>
　　選択されたものだけ表示。<br>
　　selected <br>
<br>
　　もう一回 selected を実行すると全メッシュを表示する。
</p>

<img src="images/select.svg">

<h4>球面:　sphere コマンド</h4>
<p>
sphere (半径)　(分割数)　(緯度開始角)　(緯度終了角)　(経度開始角)　(緯度終了角)<br>
</p>
<img src="images/sphere.svg">
<p>
分割数による外観の違い
</p>
<img src="images/sphere2.svg">

<h4>3D座標:　p コマンド, getPoints コマンド</h4>
<p>
Points 配列に 3D座標を格納する。<br>
後で distribute コマンド, polyline コマンド,などを実行する際に参照される。<br>
使用例は distribute コマンド, polyline コマンドなどで説明する。<br>
<br>
・ p　･･･　現在の Points 配列の内容を表示する。<br>
※ p clear　･･･　Points 配列を空にする。<br>
・ p　(x 座標)　(y 座標)　(z座標)　･･･　Points 配列に座標を追加する。<br>
※ getPoints　　　　　　　　　　　･･･　メッシュから頂点データを抽出し Points 配列に格納する。<br>
・ GETPoints　　　　　　　　　　　･･･　メッシュから頂点データを抽出し Points 配列に追加する。<br>
※ l　(.npyファイル)　　　　　　　･･･　.npy ファイルから 3D座標データを読み込み Points 配列に格納する。<br>
※ p　(polygon コマンド)　　　　　･･･　polygon コマンドの生成する座標を Points 配列に格納する。<br>
※ p　curve　(T パラメータの範囲式)　(T を使った x 座標式)　(T を使った y 座標式)　(T を使った z 座標式)<br>
　　　　　　　　　　　　　　　　　･･･　パラメータ T による曲線座標を Points 配列に格納する。<br>
<br>
先頭に ※ のついているコマンドは, 実行前に Points 配列をクリアする。<br>
</p>

<h4>配置:　distribute コマンド</h4>
<p>
Points 配列に格納されている座標にメッシュを配置する。<br>
・distribute　( .plyファイル)　･･･　.plyファイルを読み込み、配置する。<br>
　　原点→配置場所方向に向けたい場合はオプション「radial」を指定する。<br>
　　配置場所→原点方向に向けたい場合はオプション「-radial」を指定する。<br>
<br>
・distribute sphere (サイズ)　･･･　球を生成し配置する。<br>

</p>
<img src="images/distribute.svg">

</p>

<h4>折れ線:　polyline コマンド, POLYLINE コマンド</h4>
<p>
Points 配列の点を折れ線(パイプ)で接続する。<br>
・polyline　[(断面の画数)　(断面の半径)　(比率)]　終点と始点をつながない。すき間を padding する。<br>
・POLYLINE　[(断面の画数)　(断面の半径)　(比率)]　終点と始点をつなぐ。　　すき間を padding する。<br>
・poly-line　[(断面の画数)　(断面の半径)　(比率)]　終点と始点をつながない。すき間を padding しない。<br>
・POLY-LINE　[(断面の画数)　(断面の半径)　(比率)]　終点と始点をつなぐ。　　すき間を padding しない。<br>　
<br>
　<strong>断面の画数と断面の半径</strong><br>
　・デフォルトの画数：25<br>
　・デフォルトの半径：0.02<br>
</p>
<img src="images/polyline.svg">
<p>
　<strong>ハイフンありとハイフンなし, 小文字と大文字</strong><br>
　　折れ線接続した際に、曲がり角でパイプとパイプの間にすき間ができる。<br>
　　・ハイフンなし：　すき間を padding する。<br>
　　・ハイフンあり：　すき間を padding しない。<br>
　　・小文字：　終点と始点をつながない。<br>
　　・大文字：　終点と始点をつなぐ。<br>
</p>
<img src="images/polyline2.svg">

<p>
　<strong>比率</strong><br>
　　点と点をパイプで覆う比率を設定する。<br>
　　・1.0(デフォルト)：　完全に覆う。<br>
　　・0.0：　　　　　　　全く覆わない。(padding のみ)<br>
　　・0 ＜, ＜ 1：　　　 　部分的に覆う。(破線。padding がじゃまな場合はハイフンありコマンドを使う)<br>
</p>

<img src="images/ratio.svg">

<p>　ratio = 0の使用例</p>

<img src="images/ratio2.svg">

<p>
　<strong>折れ線の始端・終端処理</strong><br>
　パラメータの指定で折れ線の始端・終端にキャップを付けることができる。<br>
　　polyline　(断面の画数)　(断面の半径)　(比率)　(始端のキャップ)　(終端のキャップ)<br>
　　(例)<br>
　　polyline　25　0.02　1　sphere　sphere<br>
</p>

<img src="images/polyline4.svg">

<p>
　キャップが裏返しになる場合があり, 手動で設定する必要がある･･･<br>
　・sphere　･･･　裏返さない<br>
　・-sphere　･･･　裏返す<br>
　(例)<br>
　　l　data/raimon.txt<br>
　　polyline　25　0.02　1 shpere　sphere<br>
</p>

<img src="images/polyline5.svg">

<p>
　<strong>折れ線の使用例</strong><br>
　　他のソフトウェアで作成した 3D 軌道データを PLY 化する。<br>
　　　l  data\chaos_trajectory.npy　･･･　10,000点のカオス軌道データ<br>
　　　poly-line<br>
<br>
　　※ padding 処理は地味に重いので, 点の数が多い場合はハイフンありを使った方が良い。<br>
　　　 ハイフンなし(polyline)で実行すると, すごく時間が掛り, 作成されるメッシュも巨大になる。<br>
</p>
<img src="images/polyline3.svg">

<h4>その他コマンド</h4>
<p>
　<strong>メッシュ情報表示</strong><br>
　　i<br>
　メッシュのx軸, y軸, z軸の幅, min, maxを表示する。<br>
　(例)<br>
　　x　4.799944　-2.399972　-　2.399972<br>
　　y　4.666745　-2.333372　-　2.333372<br>
　　z　4.874035　-2.437017　-　2.437017<br>
</p>
　<strong>センタリング</strong><br>
　　centering<br>
　　(例)
<p>
<img src="images/centering.svg">
</p>
</body>
</html>





