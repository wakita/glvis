# SB05A

- VAOをbindすること
    glVertexAttribPointerを実行する場合は事前にVAOをbindしておかなくてはならない．
    
    これを怠ったときのエラーコードは1282．

- glVertexAttribPointerの引数には十分に注意．非常にわかりにくい．glDraw\*がsegmentation Faultをおこす場合は，これを疑え．

- 複数のVBOを用いるときはglEnableVertexAttribArrayの設定を忘れないこと．デフォルトで最後にbindしたバッファは有効化されているような気がする．それ以前にbindしたものについては明示的にenableしておかないと無視されるようだ．（仕様書で要確認）
