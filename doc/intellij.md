# Git for Windows を入手

Git for Windows はデフォルトで `c:\Program Files\Git` にインストールされる。

基本的にはMinGWのような気がする。`Win-s "git bash"`を起動すると`/usr/bin/`のさまざまなUNIXコマンドが利用できるようになる。`git`や`ssh`もそれらの一部だと思えばよさそう。これがあれば、Win10 Anniversary editionはあまりいらなさそう。

便利だと思ったら`Git Bash`をスタートメニューとかタスクメニューに保存するとよい。

# Anaconda3 の設定

Anaconda3を本家からダウンロードしてインストール。このドキュメント執筆時点でのAnaconda3の最新版は4.20。

Anaconda3の

- バージョンの確認方法は`conda --version`

- アップデートの方法は

    - `conda update conda`
    - `conda update anaconda`
    - `conda update --all`

## Pythonの仮想環境(`glvis`)の作成と設定

`cmd.exe`を開き、以下を実行

```
conda create --name glvis python=3
activate glvis
conda install pyopengl numpy matplotlib mpmath notebook pyopengl scipy
```

PyQt5の少し古い版(`pyqt5.6`)もAnaconda3でインストールできるけれど、最新版を入れるのであれば次の節の方法を用いる。

## QtとPyQt5の最新版のインストール

この文章の執筆時点ではQt 5.7.0 for MSVC 2015, 64bit版とPyQt5.7の組み合わせ。PyQtはQtにPythonの革を被せたものなので、対応するバージョンのQtをインストールすることに気をつけること。PyQtの開発はQtの開発に半年ほど遅れる傾向がある。

まず、インストール可能なPyQt5のバージョンを確認するために以下を実行する。

`pip search PyQt5`

リストのなかからPyQt5に該当する項目を探し、名前の右に表示されるバージョン番号を確認する。このバージョンのQt5をインストールしなくてはいけない。

### Qt5のインストール

Qt5は配布元からダウンロードしてインストールする。以下の点に気をつけること

- Windows版であること

- MSVCのバージョンの新しいもの(執筆時点で MSVC 2015)

- 64bit版であること

### PyQt5のインストール

Qt5のインストールが完了するのを待ってからPyQt5をインストールする。PyQt5はQt5に依存しているので、Qt5のインストールを待たなくてはいけない。

```
activate glvis
pip install PyQt5
```

- PyQt5 (5.7) のインストール場所: `envs/glvis/Lib/site-packages/PyQt5`

- pyqt5 (5.6.0) のインストール場所: どこだ？？？

PyQt5がきちんとインストールされたことを確認するために`glvis`環境でPythonを起動し、以下を実行してみる。

```
from PyQt5 import QtCore
QtCore.QT_VERSION_STR
```

`'5.7.0'`のように意図どおりのバージョン番号が表示されればよい。

# 非標準モジュール群のインストールとサイトパッケージへの設定

## `pyqtgl`リポジトリの入手

`Git Bash`を用いる。

```
mkdir -p /c/wakita/src
cd /c/wakita/src
git clone https://github.com/wakita/pyqtgl
```

## SymPy開発版の入手

SymPyにはバグが多く、安定版はかなりひどいので開発版を利用すること。スタートメニューから`Git Bash`を起動し、以下のように開発版を`git clone`する。

```
cd /mnt/c/wakita
mkdir -p src
cd src
git clone https://github.com/sympy/sympy.git
```

## 非標準モジュールへのパスのサイトパッケージへの追加

ここに展開されたディレクトリは、現時点ではPythonインタプリタは感知しない場所なので、なんらかの方法でPythonに知らせなくてはいけない。そこで、まずはPythonを起動して、ユーザ用のサイトパッケージの場所を調べる。

```
import site
site.getusersitepackages()
```

ここで表示されたディレクトリが目的の場所だが、普通はこの時点では存在していないので作成する必要がある。`cmd.exe`は`AppData`のような隠しフォルダのアクセスには不便なので、ここでも`Git Bash`を起動して作業する。

```
mkdir /c/Users/wakita_000/AppData/Roaming/Python/Python35/site-packages
```

ここで作成した`site-packages`フォルダのなかに以下の一行が書かれている、`glvis.pth`という名前のテキストファイルを作成する。

```
c:\wakita\src\sympy
c:\wakita\Dropbox (smartnova)\work\pyqtgl\lib
```

ここでの設定がうまくいったことを確認するために`glvis`環境でPythonを起動して以下を実行する。

```
import sympy
import sn
```

エラーが出なければめでたし。エラーが出た場合はそれぞれの設定項目を再度確認すること。

## `pyqtgl`のテスト

ここまでの作業が終われば`pyqtgl`のデモが動作するはず。`cmd.exe`で`pyqtgl/kw`に移動して以下を実行する。

```
python kw1.py
```

# 開発環境: IntelliJを入手

JetBrainsのIntelliJ IDEA Ultimate版は学生に無償で提供されているので、[申し込むとよい](https://www.jetbrains.com/student/)。どうしても嫌なら、Pythonに特化したPyCharmを使う。

## Settings > Plugins

インストールできたら、非標準のプラグインを追加する。

- Python: Python用のプラグイン。これがないとIntelliJでPythonの開発はできない。PyCharmと同じ機能を提供している。

- Markdown用のプラグイン。いくつか提供されているので人気の高いものから選ぶとよい。変換器はSwing版よりもJavaFX版を設定しておくと見た目がきれい。

## Settings > Tools >

Pythonの非標準モジュールについてドキュメントと連携する機能を設定しておくと、ソースコードを編集しているときに簡単にドキュメントにアクセスできる。ソースコードでカーソルを調べたいメソッドの上に移動し`F1`を押せばそのメソッドのドキュメントが表示できる。

- Python External Documentation

    - PyQt5: `http://pyqt.sourceforge.net/Docs/PyQt5/api/{class.name.lower}.html#{function.name}`

        慣れてきたらPyQt5のドキュメントではなく、C++向けのQt5のドキュメントと関連づけた方が便利かもしれない。

    - PyOpenGL: `PyOpenGLはろくなドキュメントを提供していないので、OpenGLの本家のドキュメントに連携するとよい。調べておきます。`

# Create new project (pyqtgl):

- Anaconda glvis SDK
- File Menu > Project Structure
    - Modules
        Add Content Root: `$DROPBOX/work/pyqt as sources`
