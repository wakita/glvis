- Uniform変数を設定するときは事前にprogram.use()すること。 (geometry.test.point)
     これを怠った場合には、GL_INVALID_OPERATION (= 1282) エラーとなる。おそらく、引き金となっているのは[glUniformのマニュアル](https://www.khronos.org/opengles/sdk/docs/man/xhtml/glUniform.xml)の次の記述に該当するものと思われる --- `GL_INVALID_OPERATION` is generated if there is no current program object.
