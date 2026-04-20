<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
<h1><center>PLY Editor</center></h1>
<h2>なにものか？</h2>
<p>
　簡単な形状のPLY(プリミティブ)作成と、それを回転・スケーリング・平行移動するだけのエディターです。<br>
<br>
　(例) 円盤を回転・スケーリング・平行移動してメッシュを作成。
</p>
<img src="images/sample1.svg">

<h3>環境構築</h3>
<p>
　pip install Open3D<br>
　pip install mapbox_earcut　･･･　img2mesh で使用<br>
　pip install imageio　　　　･･･　img2gif.py で使用<br>
　pip install mediapipe==0.10.14　･･･　img2facemesh.py, img2fingers.py, img2skeleton.pyで使用<br>
　pip install manifold3d　　 ･･･　Boolean.py で使用<br>
　pip install plyfile　　　　･･･　ply2skeleton.py で使用<br>
　pip install scikit-image　 ･･･　implicit_function.py で使用<br>
</p>

<h3>チュートリアル</h3>
<p>
　チュートリアルは <a href="https://boyoyon.github.io/PLY_EDIT/tutorial/tutorial.html">こちら</a>
</p>

<h3>更新項目</h3>

<p>
　<strong>implicit_function.py</strong>　･･･　PLY_interactive.py とは別の即席の陰関数モデリングツール<br>
　python　implicit_function.py　(式)<br>
　・後でウラ面、オモテ面の色を別々に設定できるように<br>
　　ウラ面＋オモテ面(implicit.ply), オモテ面(implicitA.ply), ウラ面(implicitAA.ply)を保存。<br>
　・aキー押下で座標軸表示/消すをトグル。<br>
　・cキー押下で、矢印キー押下時にスクリーンキャプチャーする/しないをトグル。<br>
　・7/8キーで矢印キーで調整するlevel値のステップを小さくする/大きくする。<br>
<br>
　(例)エイリアンっぽい<br>
　　python implicit_function.py ((x**2)+(y**2)+(z**2)+2*y-1)*((x**2+y**2+z**2-2*y-1)**2-8*z**2)
</p>
<img src="images/alien.png">
</p>
　(例)サンゴっぽい<br>
　　python implicit_function.py x+np.sin(4*x)*np.cos(4*y)+np.sin(4*y)*np.cos(4*z)+np.sin(4*z)*np.cos(4*x)
</p>
<img src="images/sango.gif">
<p>
　　python implicit_function.py x+y**2+z**3
</p>

<img src="images/x_plus_y2_plus_z3.gif">

<p>
　python implicit_function.py x**3+y**3+z**3-3*x*y-3*y*z-3*z*x
</p>
<img src="images/x3_y3_z3-3xy-3yz-zx.gif">
<p>
　　python implicit_function.py (1-np.sqrt(x**2+y**2))**2-z**2<br>
　　(トーラスの式の +z**2 を -z**2 に変えてみた)
</p>
<img src="images/1_minus_np_sqrt_x2_plus_y2_minus_z2.gif">

<p>
　　python implicit_function.py np.sin(3*x)*np.cos(3*y)+np.sin(3*y)*np.cos(3*z)+np.sin(3*z)*np.cos(3*x)<br>
　　(<a href="https://ja.wikipedia.org/wiki/ジャイロイド">ジャイロイド</a>)
</p>
<img src="images/gyroid.gif">
<p>
　<strong>地形っぽい面の作成</strong><br>
　　python　src\create_terrain.py<br>
<br>
　　terrainA.ply　(オモテ面)<br>
　　terrainAA.ply (ウラ面)　　
</p>
<p>
　<strong>フィルター</strong><br>
　filter　(x/-x/y/-y/z/-z/X/-X/Y/-Y/Z/-Z)<br>
　・x　　三角形の頂点の１つが x > 0 ならば削除<br>
　・-x　 三角形の頂点の１つが x < 0 ならば削除<br>
　・X　　三角形の頂点すべてが x > 0 ならば削除<br>
　・-X　 三角形の頂点すべてが x < 0 ならば削除<br>
　　(他も同様)<br>
　Points[] に対しては<br>
　p　filter　(x/-x/y/-y/z/-z)<br>

</p>

<img src="images/terrain.svg">

<p>
　python　src\display_opaque_translucent_mesh.py　(不透明mesh)　(半透明mesh)<br>
　(例)<br>
　python src\display_opaque_translucent_mesh.py data\terrainA.ply data\plane.ply　　
</p>
<img src="images/opaque_translucent.png">
<p>
　<strong>簡易彫刻</strong><br>
　python src\sculpt.py<br>
　(Visualizer画面上で)<br>
　　矢印キー　･･･　ドリルの位置変更<br>
　　fキー　　 ･･･　ドリルをターゲットに近づける<br>
　　bキー　　 ･･･　ドリルをターゲットから離す<br>
　　mキー　　 ･･･　削り開始位置をマーキング<br>
　　dキー　　 ･･･　マーキング位置からdキー押下位置まで削る<br>
　　uキー　　 ･･･　undo<br>
　(コンソール画面上で)<br>
　　save　　　･･･　plyにセーブする
</p>

<p>
　<strong>歯車の点列生成</strong><br>
　p　gear　(サイズ)　(歯の高さ)　(歯の本数)<br>
　(例)<br>
　l　data\gear2.txt
</p>
<img src="images/gear.png">
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
　<strong>polygon border</strong><br>
　多角形の borderのみのメッシュを生成する。<br>
　・polygon_border　(画数)　(外接円半径)　(幅)　[(表の色：rgb)　(裏の色：rgb)]<br>
　※ 厚みはない。<br>
</p>
<img src="images/polygon_border.png">

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
　<strong>c コマンド：メッシュの単色塗りつぶし</strong><br>
　　c　(red 成分:0～255)　(green 成分:0～255)　(blue 成分:0～255)</p>

<p>
　<strong>cコマンド：色セットの選択　</strong><br>
　<strong>　default/red/green/blue/pink/orange/cyan/white/gray/black オプション</strong><br>
　　SurfaceOuter/SurfaceInner/LateralOuter/LateralInner/PaddingOuter/PaddingInner<br>
　を設定するオプション<br>
<br>
　<strong>cコマンド：色セットのpush/pop　</strong><br>
<br>
　　SurfaceOuter/SurfaceInner/LateralOuter/LateralInner/PaddingOuter/PaddingInner<br>
　を push/pop する<br>
</p>

<img src="images/c_command.svg">

</p>
<p>

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

<p>
　<strong>sphereコマンド派生：　sphereAA コマンド</strong><br>
　・法線が視点方向の球面のみを表示する。<br>
　　(例)<br>
　　sphereAA　0.75　100<br>
　　normals<br>
　　polygon　100　0.74　-0.02<br>
　　r　0　0　90<br>
　　polygon　100　0.74　-0.02<br>
　　r　90　0　0<br>
　　polygon　100　0.74　-0.02<br>
　　※ Visualizer で ＠キーを押して画角を狭めた方が効果的。<br>
</p>

<img src="images/sphereAA.png">

<h4>3D座標:　p コマンド, getPoints コマンド</h4>
<p>
　Points 配列に 3D座標を格納する。<br>
　後で distribute コマンド, polyline コマンド,などを実行する際に参照される。<br>
　使用例は distribute コマンド, polyline コマンドなどで説明する。<br>
<br>
　・ p　･･･　現在の Points 配列の内容を表示する。<br>
　・ p clear　･･･　Points 配列を空にする。<br>
　・ p　(x 座標)　(y 座標)　(z座標)　･･･　Points 配列に座標を追加する。<br>
　・ p　centering　･･･　Points配列内の座標をセンタリングする <br>
　・ p　r　xx　xx　xx　･･･　Points配列内の座標の回転 <br>
　・ p　s　xx　xx　xx　･･･　Points配列内の座標のスケーリング <br>
　・ p　t　xx　xx　xx　･･･　Points配列内の座標の平行移動 <br>
　・ p　save　( .npyファイル名)　･･･　Points配列内の座標を .npy ファイルに保存<br>
　※ getPoints　　　　　　　　　　　･･･　メッシュから頂点データを抽出し Points 配列に格納する。<br>
　・ GETPoints　　　　　　　　　　　･･･　メッシュから頂点データを抽出し Points 配列に追加する。<br>
　※ l　(.npyファイル)　　　　　　　･･･　.npy ファイルから 3D座標データを読み込み Points 配列に格納する。<br>
　※ p　(polygon コマンド)　　　　　･･･　polygon コマンドの生成する座標を Points 配列に格納する。<br>
　※ p　curve　(T パラメータの範囲式)　(T を使った x 座標式)　(T を使った y 座標式)　(T を使った z 座標式)<br>
　　　　　　　　　　　　　　　　　･･･　パラメータ T による曲線座標を Points 配列に格納する。<br>
<br>
　先頭に ※ のついているコマンドは, 実行前に Points 配列をクリアする。<br>
</p>

<p>
　<strong>マーカー表示</strong><br>
　　3D 座標は polyline コマンド, distribute コマンドなどでメッシュ化しないと,<br>
　　どうなっているかわからなかったので、マーカー表示するようにした。<br>
　　p　disp　･･･　Points 配列内座標のマーカー表示 on/off をトグルする。<br>
　　(例)<br>
　　p　1　1　0　　･･･　3D 座標 (1,1,0) を追加する<br>
　　p　-1　-1　0　･･･　3D 座標 (-1,-1,0) を追加する<br>
　　p　clear　　　･･･　3D 座標を空にする<br>
　　l　data/f.txt　･･･　「F」字の頂点座標を読み込む<br>
　　p　t　0.4　0.4　0　･･･　座標軸と重なって見にくいので 3D 座標を平行移動する
</p>

<img src="images/p.svg">

<p>

　<strong>3D座標:　回転/スケーリング/平行移動/組み合わせの複数回実施</strong><br>
　　メッシュに対して回転/スケーリング/平行移動/組み合わせを複数回できるが、<br>
　　同様のことを 3D座標に対しても適用できるようにした。<br>

</p>

<p>
　　回転/スケーリング/平行移動/組み合わせを複数回実施した点を使って面を張る。<br>
　　surface　[pclose/eclose/peclose]<br>
　　(例)<br>
　　　p　polygon　30　･･･　正30角形の頂点<br>
　　　p　r 0　0　-90　･･･　3D 座標群を z 軸周りに90°回転<br>
　　　p　g　s　1　0.9　0.9　t　0　-0.5　0　r　20　0　0　t　0.1　0.5　0　30<br>
　　　･･･　スケーリング/平行移動/回転を組み合わせた変換を30回実施<br>
　　　surface　･･･　変換途中の座標を使って面を張る<br>
<p>

<img src="images/surface.svg">

<p>
　　surface コマンドのパラメータ：　pclose/eclose/peclose<br>
　　※ テキトーに付けた名前<br>
　　　 3D 座標列の path 方向の最後と最初を閉じる<br>
　　　 押し出し(extrusion)方向の最後と最初を閉じる<br>
</p>

<img src="images/surface2.svg">

<p>
　　(例) eclose が有効な例<br>
　　　draw　･･･　手書きで 2D 曲線を入力する<br>
　　　p r 0 10 0 36　･･･　2D 曲線を360°回転して器っぽいものを作る。<br>
</p>

<img src="images/surface3.svg">

<p>
　　(例) pclose が有効な例<br>
　　　l　data/f.txt　･･･　「F」字の頂点データをロード<br>
　　　p　t　0.2　0.2　0　･･･　3D座標を平行移動(座標軸と重なって見ずらいため)<br>
　　　p　t　0　0　0.2　2　･･･　z 軸方向に 0.2 移動(押し出す)<br>
　　　※ count ≧ 2 にしないと面を張れない。<br>
　　　surface　･･･　「F」の底辺がつながらない<br>
　　　surface　pclose　･･･　底辺がつながる
</p>

<img src="images/surface4.svg">

<p>
　<strong>3D座標配列関連のコマンド・オプション</strong><br>
</p>
<img src="images/p_p2_options.svg">

<p>
　<strong>p2コマンド：　p2pオプション</strong><br>
　　P2[ ] 内の n,m,3 データを n×m, 3 データに reshape して Points[ ] に格納する。
</p>
<p>
　<strong>pコマンド: p2pオプション　(num)</strong><br>
　　Points[ ] を (num) 個のシーケンスに分割して P2[ ]に移動する。<br>
　　Points[ ] にはシーケンスの最後の点が格納される。
</p>
<img src="images/p2p4.svg"><br>

<p>
　<strong>3D座標配列(p2)のload、save</strong><br>
　・l　***.npy　･･･　numpy 配列の形状で Points か P2 かを自動判断する<br>
　・p2　save　　･･･　p2配列が　.npy にセーブされる
</p>


<p>
　<strong>pコマンド:　subdiv オプション</strong><br>
　　点と点の間を細分化する。あとの twist オプションなどで必要になる。<br>
　　p　subdiv　(細分化の長さ)　･･･　最後の点と最初の点の間は細分化しない<br>
　　p　SUBDIV　(細分化の長さ)　･･･　最後の点と最初の点の間は細分化する
</p>

<img src="images/subdiv.svg">
<p>
　(細分化の長さ) を決めるための参考情報<br>
　(例)<br>
　　l　data/f.txt　　　　　　　･･･　「F」字の頂点データをロード<br>
　　(エンターキー押下)　　　　 ･･･　スクリプト実行<br>
　　p　i　　　　　　　　　　　 ･･･　3D 座標データの情報表示<br>
<br>
　　x　0.600000　0.000000　-　0.600000<br>
　　y　0.900000　0.000000　-　0.900000<br>
　　z　0.000000　0.000000　-　0.000000<br>
　　length between adjacent points: 0.200000 - 0.900000　･･･　細分化前の点と点の間隔は最小 0.2<br>

</p>
<br>
<p>
　<strong>pコマンド:　twist オプション</strong><br>
　　p　twist　(x/z/z)　(ねじる角度)<br>
</p>
<img src="images/twist.svg">
<p>
　(twist オプションの利用例) ツイストする雷門<br>
</p>

<img src="images/twisted_raimon.gif"><br>

<p>
　<strong>pコマンド:　surface オプション</strong><br>
　　p　surface　(xの範囲)　(zの範囲)　(y=f(x,z)の式)<br>
　(例)<br>
　　p　surface　np.linspace(-1,1,100)　np.linspace(-1,1,100)　0.1*np.sin(np.sqrt(x**2+z**2)*np.pi*2)<br>
　(例)<br>
　　p　surface　np.linspace(-1,1,100)　np.linspace(-1,1,100)　0.3*np.random.rand(100,100)<br>
</p>

<img src="images/p_surface.svg">

<p>
・p surface → surface　コマンドでメッシュ化 → 五角形や三角形に剪定<br>
・正 12 面体や正 20 面体を作成するスクリプトで p polygon の代わりに<br>
　剪定した メッシュをロードすると･･･
</p>

<img src="tutorial/data/images/scrubbing_brush.png">

<p>
　<strong>surfaceコマンド：パラメータ　Eclose</strong><br>
　押し出し方向の最後と最初を接続する際、indexの同じ点ではなく、距離の近い点を接続する。<br>
　(例)<br>
　　裏と表がつながるような場合に使用する。<br>
　　l　data\kline.npy　･･･　クラインの壺の頂点列をロード<br>
　　surface　Eclose　0　10　･･･　P2(Pointsの履歴)の 0～10 をメッシュ化<br>
　　p2　transpose　･･･　P2 (Points の履歴)を転置(後述)<br>
　　p　pop　0　･･･　転置した履歴の 0番目 (断面)　を Points に読み込む<br>
　　LateralOuter　255　128　255　･･･　側面色をピンクに設定<br>
　　polyline　25　0.06　･･･　断片をピンクの折れ線でメッシュ化<br>
　　p　pop　11　･･･　もう一方の断面(indexが1個ずれる･･･)をPointsに読み込む<br>
　　LateralOuter　255　200　64　･･･　側面色をオレンジに設定<br>
　　polyline　255　0.06　･･･　もう一方の断面をオレンジの折れ線でメッシュ化<br>
    save　kline_cut_model.ply　･･･　メッシュをセーブ<br>
<img src="images/Eclose.svg"><br>
</p>

<p>
　<strong>surfaceコマンド：パラメータ　start　end</strong><br></p>
　　表面の生成を開始、終了する path 方向の index を指定できるようにした。<br>
　　上の、クラインの壺の内部を表示する場合などに利用できる。<br>
</p>
<p>
　<strong>p2コマンド：パラメータ　transpose</strong><br></p>
　　path 方向と extrusion 方向を入れ替える。<br>
　　start, endパラメータを使ってカットモデルを作成した場合の断面表示などで利用できる。<br>
<img src="images/transpose.svg"><br>
<img src="images/surface6.svg"><br>

</p>

<p>
　<strong>p2コマンド：パラメータ　reverse　(p/e)</strong><br></p>
　　path方向、extrusion方向のindexを逆順に付け替える、<br>
<img src="images/reverse.svg"><br>
</p>　

<p>
　<strong>surfaceコマンド：　surfaceコマンド,　sideA コマンド, sideAA コマンド</strong><br>
　・surface コマンド ･･･ 面の法線方向によらずメッシュ化する<br>
　・sideAA コマンド　･･･ 面の法線が視点方向のもののみメッシュ化する<br>
　・sideA コマンド　･･･　面の法線が視点方向と反対方向のもののみメッシュ化する<br>
　※ 頂点の index の振り方によって変わるので, sidaA / sideAA コマンドを試して確認する必要あり。<br>
　(例)<br>
　　l　data/KleinBottle.npy　<br>
　　sideAA　pEclose
</p>
<img src="images/KleinBottle.gif">

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

<p>
　<strong>画像からのメッシュ作成</strong><br>
　img2mesh　(画像ファイル名)<br>
　コンソールから実行できるようにした。表, 裏の2メッシュ＋輪郭の座標がロードされる。<br>
　・背景が黒でないとうまく動作しない。<br>
　・表と裏は select してみないとわからない.<br> 
</p>
<img src="images/img2mesh2.svg">

<p>
　<strong>手書き入力：　draw コマンド</strong><br>
　draw　[(入力画面幅)　(入力画面高さ)　(モード)]<br>
　※ (今のところ)一筆書きのみ。思い付きで実装したがいまいち ･･･<br>
　　　モード指定なしだと、z 座標は 0 固定。<br>
　　　モードに 1 を指定すると z 座標は 0.01ずつ増える。<br>
</p>
<img src="images/draw.svg">

<h4>その他コマンド</h4>

<p>
　<strong>ループ実行：　loop start/quit/end [count]</strong><br>
　　指定したコマンド列を count 回数繰り返す。<br>
　　(例)<br>
　　　[ 0]　python src\PLY_interactive.py 400 300 # 画面サイズを指定して起動<br>
　　　[ 1]　l　data/f.txt　　　　# F の頂点データ読み込み<br>
　　　[ 2]　(エンターキー押下)　# スクリプト実行<br>
　　　[ 3]　POLYLINE　　　　　　# F の輪郭の折れ線メッシュを作成する<br>
　　　[ 4]　(Visualizer画面をドラッグしカメラ位置を設定する)<br>
　　　[ 5]　getEyePos　　　　　 # カメラ位置を保存する<br>
　　　[ 6]　del 0*.png　　　　　# 不要なキャプチャー画像を削除<br>
　　　[ 7]　loop start　　　　　# ループコマンド列の入力を始める<br>
　　　[ 8]　cap　　　　　　　　 # スクリーンキャプチャー<br>
　　　[ 9]　r 0 10 0　　　　　　# y軸周りに10°回転<br>
　　　[10]　setEyePos　　　　　 # カメラ位置を復元する<br>
　　　[11]　loop end 36　　　　 # ループコマンド入力完了。36回繰り返す<br>
　　　[12]　(エンターキー押下)　# スクリプト実行<br>
　　　[13]　python　src\img2gif.py　0*.png　15　0 # 15fps, 無限繰り返しでgif化
</p>

<img src="images/rotate_F.gif">

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

<img src="images/centering.svg">

<p>
　<strong>システムコマンド：　python, dir, copy, move, ren, del</strong><br>
　　コンソールから dir, copy, move, ren, del を実行できるようにした。<br>
　　(例)<br>
　　　花びらふうのメッシュを作成～セーブし、思い付きスクリプトで変形してロード。<br>
　　　[ 1]　LateralOuter 255 128 255　　　　　　# 花びらの外側をピンクにする<br>
　　　[ 2]　LateralInner 230 230 255　　　　　　# 花びらの内側をうすい青にする<br>
　　　[ 3]　sphere 1 30 0 180 -360/5/2 360/5/2 　# 花びらを作成<br>
　　　[ 4]　t 0 1 0　　　　　　　　　　　　　　   # 花びらの付け根を原点に移動<br>
　　　[ 5]　r 30 0 0　　　　　　　　　　　　　　# 花びらを傾ける<br>
　　　[ 6]　r 0 360/5 0 5　　　　　　　　　　　 # 花びらを 5 枚にする<br>
　　　[ 7]　s 1 1.3 1　　　　　　　　　　　　　 # 縦(y軸方向)にちょっと伸ばす<br>
　　　[ 8]　save flower.ply　　　　　　　　　　 # セーブ<br>
　　　[ 9]　d　　　　　　　　　　　　　　　　　 # 消す<br>
　　　[10]　python src\twist.py flower.ply 50　 # <strong>外部スクリプトで</strong>ねじる (y方向のみのお試し実装)<br>
　　　[11]　l flower_twisted.ply　　　　　　　　# ねじった ply をロード～表示
</p>
<img src="images/flower.svg">
</p>

<p>
　<strong>cylinderコマンド</strong><br>
　・o3d.geometry.TriangleMesh.create_cylinder で円筒形のメッシュを作成する。<br>
　　cylinder　(半径)　(高さ)　[(解像度 ･･･ 天板、底面の円周上の点の数)]<br>
<br>
　　manifold3d によるブール演算が、なぜか自前で作ったメッシュでは失敗するため、追加した。<br>
　　(例)<br>
　　cylinder　0.5　1　･･･　半径 0.5, 高さ 1 の円筒形を作る<br>
　　save　yoko.ply　　･･･　yoko.ply でセーブ <br>
　　d　　　　　　　　 ･･･　表示を消す<br>
　　cylinder　0.25　3 ･･･　半径 0.25, 高さ 3 の円筒形を作る<br>
　　r　90　0　0　　　 ･･･　x 軸周りに 90°回転<br>
　　save　tate.ply　　･･･　tate.ply でセーブ<br>
　　python　src\Boolean.py　yoko.ply　tate.ply　･･･　ブーリアン(引き算)を実施<br>
</p>

<img src="images/Boolean01.svg">

<p>
　<strong>skeleton コマンド：　fast パラメータ</strong><br>
　　指の表示では今の画数(25), 太さ(0.02)がほしいが、データが大きくて処理が重いので、<br>
　　第二引数で fast を指定した場合、画数(5),太さ(0.001)として細くて軽量処理になるようにした。<br>
　　(例)<br>
　　　python　src\ply2skeleton.py　yoko_minus_tate.ply　･･･　ブーリアン演算結果の ply <br>
　　　l　yoko_minus_tate_skeleton.npy　･･･　skeleton化したデータをロード<br>
　　　skeleton　fast<br>
</p>

<img src="images/ply2skeleton.png">

<p>
　<strong>顔, 指、全身の骨格データの取り込み</strong><br>
　img2facemesh.py,　img2fingers.py,　img2skeleton.py<br>
　(例) 指の骨格データ取り込み<br>
<br>
　　python　src\PLY_interactive.ply<br>
　　python　src\img2fingers.py　images\2hands.png　･･･　画像から指の抽出<br>
　　l　2hands_hand_1_fingers.npy　･･･　指の骨格座標をロード<br>
　　skeleton　･･･　座標をパイプで接続<br>
　　normals　･･･　法線算出<br>
　　l　2hands_hand_2_fingers.npy　･･･　指の骨格座標をロード<br>
　　skeleton　･･･　座標をパイプで接続<br>
　　normals　･･･　法線算出<br>
　
<img src="images/2hands.gif"><br>

　(例) 全身の骨格データ取り込み<br>
　　python　src/img2pose_keypoints　data/pose.png　･･･　全身のキーポイント抽出<br>
　　python　src/keypoints2parts.py　(pose_keypoints.npy)　･･･　キーポイントからパーツをメッシュ化するスクリプトを作成<br>
　　l　skeleton.txt　･･･　スクリプトをロード<br>
　　(エンターキー押下)　･･･　スクリプト実行<br>
　　s　1　1　1/2　･･･　z方向に出っ張っているでのz方向だけ1/2にスケーリング<br>
<img src="images/pose.gif"><br>
</p>
<p>
　(例) フェイスメッシュデータ取り込み<br>
　　python　src/img2facemesh.py　(画像ファイル)<br>
</p>

<p>
　<strong>輪郭の立体化</strong>(スケーリング＋平行移動)<br>
　　※ 輪郭線が細いとうまくいかない。<br>
　(例)<br>
　　l　data\section.txt　　　　　　　･･･　断面用の点データ定義スクリプトをロード<br>
　　(エンターキー押下)　　　　　　　･･･　スクリプト実行<br>
　　p　push　section　　　　　　　　･･･　Points[] から Section[] にコピー<br>
　　img2mesh　data\heart.png　　　　･･･　背景黒の二値(っぽい)画像から輪郭抽出<br>
　　(ESCキー以外を押下)　　　　　　　･･･　結果がセーブされる<br>
　　puccho　　　　　　　　　　　　　･･･　輪郭 (Points[]) を断面 (Section[]) で立体化<br>
　　surface　pclose　　　　　　　　　･･･　立体化した結果 (P2[]) をメッシュ化<br>
<br>
　　ウラ返しになる場合は、<br>
　　d　　　　　　　　　　　　　　　　･･･　メッシュを削除<br>
　　p2　reverse　p　　　　　　　　　･･･　path方向の順番を逆順にして<br>
　　surface　pclose　　　　　　　　　･･･　再度メッシュ化
</p>
<img src="images/puccho.svg">

<p>
　人工物に飽きたら･･･(猫(などの自然画像)に癒される)
</p>
<img src="images/neko.gif">

<p>
作り方<br>
　① <a href="https://huggingface.co/spaces/depth-anything/Depth-Anything-V2">DepthAnything V2 デモ</a> で画像から深度画像を作る
</p>
<img src="images/DepthAnythingV2.svg">
<p>
　② 画像, 深度画像 → 点群 → メッシュ
</p>
<img src="images/WorkflowImg2Mesh.svg">
<br>

<p>
　<strong>cat コマンド</strong><br>
　　ネコに癒されたら、次はネコの手を借りる。<br>
　　(実態はタートルグラフィックス)<br>
</p>
　<img src="images/cat_command.gif">
<p>
　　cat　create　(x　y　z　dx　dy　dz)：ネコを作成する<br>
　　※ xyz：ネコの位置,　dxdydz：ネコの向き<br>
　　　 (例) cat　create　1　0　0　0　0　-1<br>
　　　　　(1,0,0)に z 軸と反対向きのネコが生成される<br>

　　cat　f　(長さ)：ネコを前に進める<br>
　　cat　up/down/right/left/roll  (角度：degree)：ネコの向きを変える<br>
　　cat　c2p　：Points[] が空または 1 点の状態でネコを作成～移動した場合は, Points[]に移動軌跡をコピー<br>
　　　　　　　　Points[] が2点以上の状態でネコを作成～移動した場合は, P2[] に移動軌跡をコピー<br>
　　cat　disp　on/off：ネコ表示をする/しない<br>
　　　　　　　　　　　 on/off指定なしの場合はトグル<br>
　　cat　d　　：ネコ終了<br>
<br>
　(例)<br>
　　l　data\mebius1.txt<br>
　　(エンターキー押下)<br>
　　(※ ネコが止まるまで待つ)<br>
　　l　data\mebius2.txt<br>
<br>
　※<br>
　・ねじるところが loop 処理でうまく表現できず(loop変数を参照できるようにしないと･･･)2つのスクリプトに分けた。<br>
　・mebius1.txt の処理が終わるのを待たないと、loop処理と後処理(mebius2.txt)の順番がぐちゃぐちゃになる。<br>
</p>
　<img src="images/mebius.png">
<p>
　(例)<br>
　　l　data/cat_spiral.txt<br>
　　(エンターキー押下)<br>
　　(complete scriptと表示されたら)<br>
　　cat　c2p<br>
　　polyline
</p>
　<img src="images/cat_spiral.png">

<p>
　<strong>星</strong><br>
　・star　(サイズ)　(膨らみ)　[(色：rgb)]<br>
</p>
<img src="images/star.png">

<p>
　<strong>電卓：　calc</strong><br>
　　(例) calc np.sin(np.deg2rad(36))
　　コンソールから 式を入力して計算できるようにした。
</p>
</body>
</html>




