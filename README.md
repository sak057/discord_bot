# discord_bot  

##事前に必要な準備（Google API)  
1.Google Sheets APIを使えるようにする  
2.Google Cloud Consoleでプロジェクトを作成  
3.Google Sheets APIを有効化  
4.サービスアカウントを作成し、JSONキーをダウンロード  
5.回答スプレッドシートの「編集者」にサービスアカウントのメールアドレスを追加

##必要なパッケージ  
discord.py  
google-api-python-client  
google-auth  
google-auth-oauthlib  
google-auth-httplib2  
apscheduler  
python-dotenv  

##テスト方法  
1: .envにトークンとチャンネルIDを記入  
2: service_account.jsonを取得して設置  
3: config.jsonを空データで用意（初回実行で更新）  
4: 以下コマンドで起動：  
```
pip install -r requirements.txt
python bot.py
```
5: Discordで /setsheet <スプレッドシートID> を送信  
