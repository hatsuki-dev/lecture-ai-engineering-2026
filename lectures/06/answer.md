# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：
- `app.agent`：`search_materials`
- `app.mcp_agent`：`glossary_search_glossary`
- STEP 2 の [tool call]：
 glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：
fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：
aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング'})

aws_aws___search_documentation({'search_phrase': 'Using versioning in S3 buckets', 'topics': ['general']})
- 気づき・疑問：
最初は、MCPを使うと回答が正確になるのかと思った。実行ログを比べると、「宿題の3レベル」に答えられたのは、用語集にその定義があったからだと分かった。MCPはエージェントとサーバーの間で検索の依頼と結果をやり取りする仕組みで、設定ファイルに追記するだけで、Webページの取得やAWSの資料検索も使えるようになった。同じ用語集を、エージェントが直接呼び出す場合とMCP経由で呼び出す場合で比べると、回答内容や応答時間にどんな違いが出るのか気になった。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：
`app/mcp_server.py` に1行追加し、既存の get_lecture_summary 関数をMCPツールとして公開した。「第2回では何を学びますか？」と質問し、`--trace` で呼び出しを確認した。
- 結果：
`glossary_get_lecture_summary` が {'lecture': 2} で呼ばれ、第2回の講義概要が返った。`uv run pytest -q` では21件すべてのテストが通った。
- 気づき・疑問：
エージェントは起動時にMCPサーバーへ「どんなツールが使えますか？」と問い合わせ、その一覧をGeminiに渡すことが分かった。そのため、`app/mcp_server.py` に講義概要ツールを公開する1行を足すだけで、Geminiがそのツールを選べるようになった。実際に「第2回では何を学びますか？」と聞くと、保存前は用語集から関連用語を探していたが、保存後は講義概要を直接取得して答えられた。




- 取り組んだレベル： 実装 
- やったこと：
第3回で作った make_quiz をMCPツールとして公開した。指定した回の用語がない場合は、用語集から出題できる講義回を調べて案内するようにした。
- 結果：
ツール一覧に glossary_make_quiz が追加された。第2回を指定すると「学習率の意味は？」という問題と答えが返り、第99回を指定すると、出題できるのは第1・2・3・4・6回だという案内が返った。テストは21件すべて通過した。
- 気づき・疑問：
最初は、`make_quiz` を tools.py に書いたあと、なぜ mcp_server.py にも1行足すのかが分からなかった。ツール一覧に glossary_make_quiz が表示されたことで、`tools.py` にはクイズを作る処理を書き、`mcp_server.py` ではその処理をエージェントから使えるように登録していると分かった。また、既存のテストが21件通っていても、第2回のクイズを実際に作ると import random の抜けでエラーが出た。この経験から、自分で追加した機能は、具体的な入力を渡して動かしてみることも大切だと分かった。



- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
