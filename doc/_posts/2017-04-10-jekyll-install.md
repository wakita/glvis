---
layout: post
title:  "Jekyll のインストール方法 (BoW 版)"
date:   2017-04-11
categories: jekyll
---

朝、起きて「Bash on Windows で Jekyllを動かしたいなぁ」と思いたってちょこちょこやったら動きました。若干の紆余曲折があるので、無駄な部分、足りない部分があるかもしれません。Bash on Windows 環境なので、普通の Windows 環境や macOS では最初のあたりがすこし異なるはずです。

1. ひとまず必要なソフトをまとめてインストールします。

    ```
    sudo apt install build-essential rbenv rbenv-build pandoc
    sudo apt install libssl-dev libreadline-dev zlib1g-dev
    ```

    bundler は不要？

1. `rbenv` の環境を設定しているに違いない。でも、何やっているのかわかっていない。

    ```
    git clone git@github.com:rbenv.git .rbenv
    mkdir -p .rbenv/plugins; cd .rbenv/plugins
    git clone git@github.com:rbenv/rbenv-gem-rehash.git
    git clone git@github.com:sstephenson/ruby-build.git

    cd
    echo "$(rbenv init -)"' >> ~/.bash_profile

    ~/.rbenv/bin/rbenv install 2.4.1
    ~/.rbenv/bin/rbenv global 2.4.1
    ```

    最後の方のコマンドで `rbenv` をフルパスで指定しているのは、これをしないと `/usr/bin/rbenv` が起動してしまい、それが APT がインストールした Ruby 1.9.3-p484 を利用していて、2.x 系の Ruby をインストールできなかったからです。いつの間に Ruby 1.9.3 がインストールされたんだろう。もしかしたら、`~/.bash_profile` を書き換えたあとで、それを読み込めばフルパスで指定しなくてもよかったのかも。

    あるいは一般ユーザ向けには以下のようにやるらしい。

    ```
    rbenv init
    echo "$(rbenv init -)"' >> ~/.bash_profile

    ~/.rbenv/bin/rbenv install 2.4.1
    ~/.rbenv/bin/rbenv global 2.4.1
    ```

1. Jekyll のインストール
    ```
    ~/.rbenv/bin/bundler install bundler jekyll
    ```

1. Jekyll プロジェクトの作成

    ```
    cd ~/work/glvis
    bundle exec jekyll new doc
    cd doc
    bundle exec jekyll serve --force_polling --incremental
    ```

    できた！なお、Anniversary Update 版の BoW は、ファイル更新を検知する syscall に対応していないために、`jekyll serve` がこけます。`--force_polling` はたぶん Jekyll がファイルを積極的に監視するための古いオプションなんでしょう。

    近日中に公開される Creators Update 版はファイル更新を検知する syscall に対応するようなので、そうすればこのオプションとはおさらばできるはず。
