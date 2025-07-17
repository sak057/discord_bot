import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json
from sheet_handler import get_sheet_values
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

CONFIG_FILE = 'config.json'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_new_entries.start()
    daily_report.start()

@bot.command()
async def setform(ctx, url: str):
    # URLからsheet_idを抽出
    if "docs.google.com/forms" not in url:
        await ctx.send("正しいGoogleフォームのURLを指定してください")
        return
    await ctx.send("フォームURLを保存しました（シートIDは別途設定が必要です）")

    config = load_config()
    config['form_url'] = url
    save_config(config)

@bot.command()
async def setsheet(ctx, sheet_id: str):
    config = load_config()
    config['sheet_id'] = sheet_id
    save_config(config)
    await ctx.send("スプレッドシートIDを保存しました")

@tasks.loop(minutes=2)
async def check_new_entries():
    config = load_config()
    sheet_id = config.get('sheet_id', '')
    if not sheet_id:
        return

    try:
        new_entries = get_sheet_values(sheet_id)
        if new_entries != config.get('last_entries', []):
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send("【新しい欠席者】\n" + "\n".join(new_entries))
            config['last_entries'] = new_entries
            save_config(config)
    except Exception as e:
        print(f"[check_new_entries] Error: {e}")

@tasks.loop(hours=24)
async def daily_report():
    await bot.wait_until_ready()
    config = load_config()
    sheet_id = config.get('sheet_id', '')
    if not sheet_id:
        return

    try:
        entries = get_sheet_values(sheet_id)
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            today = datetime.now().strftime('%Y/%m/%d')
            await channel.send(f"【{today}の欠席者一覧】\n" + "\n".join(entries))
    except Exception as e:
        print(f"[daily_report] Error: {e}")

bot.run(TOKEN)
