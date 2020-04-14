# インストールした discord.py を読み込む
import discord
import argparse
from termcolor import cprint

def next_step_check(m):
    return (m.content in ['/ok', 'next'])

def next_step(step, reply):
    if reply.content == '/ok' or reply.content == '/next':
        return step+1
    else:
        return step

def main(args):
    TOKEN = args.token

    client = discord.Client()

    @client.event
    async def on_ready():
        print('Login succeeded')

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        if message.content == '/neko':
            await message.channel.send('にゃーん')

        if message.content == '/end':
            await message.channel.send('GG')
            exit()
        
        if message.content == '/start' or message.content=='/reset':
            await message.channel.send('はじめていきましょーーーー！！（キシル）')
            game = 0 # 試合数
            step = 0 # 選択ステップ

            if game==0:
                await message.channel.send('ファイターを選択してください')
        
                reply = await client.wait_for("message", check=next_step_check)
                step = next_step(step, reply)
                await message.channel.send('じゃんけんを行ってください: さいしょはグー、じゃんけん…')

                    

    client.run(TOKEN)    

if __name__ == "__main__":
    cprint("-" * 50, "yellow")
    cprint(("Umebura in Discord").center(50), "yellow")
    cprint("-" * 50, "yellow")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--token',
        '-t',
        help ='bot token',
        type=str,
        required=True
    )

    args = parser.parse_args()
    main(args)
    