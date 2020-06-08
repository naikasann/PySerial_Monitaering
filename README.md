# PySerial_Monitaering

PySerialを用いて値を取得しそれをグラフ化する

---

## 目的

マイコンを用いてセンサーからデータを取得し、そのデータをraspberrypieにシリアル通信で受け取る。
(受け取るデータはカンマ区切り。)
受け取ったデータを、リアルタイムでグラフに描画しさらに[Ambient – IoTデーター可視化サービス](https://ambidata.io/)に送信するプログラム。

---

## 構成

```  構成.
各種センサー =値> マイコン =Serial> Raspberrypie =============> matlabplot(graph)
                                                ｜=Wifi(Http?)> Ambient

```

---

## 用途・目的

1日の通信回数制限があるためambientにリアルタイムで送信することは現実的ではない。
(サーバーの負荷なども考え迷惑かけちゃダメ)
そのため数分に一度の送信になる。
しかしデバッグの際にリアルタイムで計測を取得できているのかも確認する必要があると思い、
作成した。
グラフはリアルタイムで、ambientは数分に一度のように分けて使うことでより分析やプロトタイプ作成がはかどると考えた。

---

## 実行方法

1. RaspberrypieをWifi接続する。
2. マイコンを接続する。(マイコンはセンサーの値を取得してUSBに値を送信する。)
3. シリアルポートを確認する。(大体/dev/ttyACM0とかそのあたり)
4. ```python SerialMonitering.py```で実行することができる。

マイコンのセンサーの値の送信は

``` .
[センサー1の値], [センサー3の値], [センサー3の値], [センサー4の値]
```

のような形で送信を行う。またセンサーの値は現状最大４つ表示することができる。

---

## 参考文献

1. [Ambient – IoTデーター可視化サービス](https://ambidata.io/)
2. [同じ値で埋めた配列(リスト)を作成するには (fill) | hydroculのメモ](https://hydrocul.github.io/wiki/programming_languages_diff/list/fill.html)
3. [pythonで3D, 2Dのリアルタイムグラフを作る - Qiita](https://qiita.com/42t4345545242/items/710cd42b3ee1f8780260)
4. [python3 文字列を辞書に変換 - Qiita](https://qiita.com/lamplus/items/b5d8872c76757b2c0dd9)
5. [Pythonでリスト（配列）の要素を削除するclear, pop, remove, del | note.nkmk.me](https://note.nkmk.me/python-list-clear-pop-remove-del/)
6. [micro:bitとAmbientで社内の温度、環境光を可視化した - Qiita](https://qiita.com/m_ryusei/items/ec7b6c97f5f4929b43be)