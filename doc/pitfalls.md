# OpenGL Core Profile のはまりどころ

- (1/10) VAOをbindすること (sb05a)
    glVertexAttribPointerを実行する場合は事前にVAOをbindしておかなくてはならない．

- (1/11) glVertexAttribPointerの引数には十分に注意．非常にわかりにくい．glDraw\*がsegmentation Faultをおこす場合は，これを疑え． (sb05a)

- (1/12) 複数のVBOを用いるときはglEnableVertexAttribArrayの設定を忘れないこと．(sb05a)

- (1/14) Uniform変数を設定するときは事前にprogram.use()すること。 (geometry.test.point)

- (1/14) 図が表示されないバグに出会ったら，まず図の塗り潰し色を有彩色にして，本当に表示されていないか確認すること．単に外形線が画角の外側に出ている可能性がある．(regularpolygon.md)
