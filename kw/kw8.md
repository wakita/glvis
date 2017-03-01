# 準備

- `ui/dialogue.ui`: Qt Designer を用いて設計された GUI 画面

- `ui/dialogue.py`: `dialogue.ui` から uic (User Interface Compiler) を用いて生成された Python コード

# GUI の表示

1. `kw8a.py`: アプリケーションのなかから `ui/dialogue.py` を読み込み表示する例題

1. `kw8b.py`: `QDialog` を継承して利用する例題

1. `kw8c.py`: `QDialog`, `dialog.Ui_Dialog` を多重継承して利用する例題

# 参考にしたサイト

- [Using Qt Designer](http://pyqt.sourceforge.net/Docs/PyQt5/designer.html)