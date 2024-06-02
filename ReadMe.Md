# 概要

[マイナス 5%ルール](https://news.yahoo.co.jp/articles/d96aa95236c2828e02f663d80058fcdbd3100a6c#:~:text=%E5%85%B7%E4%BD%93%E7%9A%84%E3%81%AB%E3%81%AF%E3%80%81%E6%A0%AA%E4%BE%A1,%E3%81%AE%E6%99%82%E3%81%AB%E3%81%AF%E8%B2%B7%E3%81%84%E3%81%BE%E3%81%9B%E3%82%93%E3%80%82)
というものを読んだので。

Azure Functions で毎週の日曜日朝 10 時に SP500 を先週の金曜日から今週の金曜日にかけて、3%以上の下落があったかを確認します。
結果にかかわらず、Line で通知を行います。

動かすには以下を実施。

- Local の場合：local.settings.json を以下のように作る。

```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "LINE_TOKEN": "{Line Token}"
  }
}
```

- Azure Functions 状の場合：
  Environment Variables に LINE_TOKEN を設定。

<br/>

# 参考リンク

Line Notify

- https://programming-zero.net/line-notify-api-access-token/

Azure Functions

- https://qiita.com/zateon/items/0df15e84c6342f9654f8
