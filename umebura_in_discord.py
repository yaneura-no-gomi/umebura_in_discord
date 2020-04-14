# インストールした discord.py を読み込む
import discord
import argparse
from termcolor import cprint

all_stages = ['0:戦場','1:終点','2:ポケスタ2','3:すま村','4:村と街','5:ライラットクルーズ','6:カロスポケモンリーグ']

def make_stage_list(stage_idx,reply):
    print('now_stage:', stage_idx)
    updated_idx = [i for i in stage_idx if i!=int(reply.content)]
    print(updated_idx)
    updated_stages = [all_stages[i] for i in updated_idx]

    return updated_idx, updated_stages

def display_stages(stages):
    message = ''
    for s in stages:
        message += s + ', '

    return message[:-2]

def next_step_check(m):
    return (m.content in ['/ok', '/next'])

def starter_stage_check(m):
    return (m.content in [str(i) for i in range(5)])


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
        
        # 1戦目
        if message.content == '/start' or message.content=='/reset':
            await message.channel.send('はじめていきましょーーーー！！（キシル）')
            step = 0 # 選択ステップ

            # step0: ファイター選択
            await message.channel.send('ファイターを選択してください')
            reply = await client.wait_for("message", check=next_step_check)
            print('step:',step)
            
            # step1: じゃんけん
            step = next_step(step, reply)
            await message.channel.send('じゃんけんを行ってください: さいしょはグー、じゃんけん…')
            reply = await client.wait_for("message", check=next_step_check)
            print('step:',step)
            
            # step2: ステージ選択1
            step = next_step(step, reply)
            stage_idx = list(range(5))
            stages = [all_stages[i] for i in stage_idx]
            await message.channel.send('勝者は以下の5ステージから拒否するステージを1つ選択し、番号を入力してください')
            await message.channel.send(display_stages(stages))
            reply = await client.wait_for("message", check=starter_stage_check)
            await message.channel.send('{} が拒否されました'.format(stages[int(reply.content)]))
            print('step:',step)

            # step3: ステージ選択2
            step = next_step(step, reply)
            stage_idx, stages = make_stage_list(stage_idx, reply)
            await message.channel.send('敗者は以下の4ステージから拒否するステージを2つ選択してください')


            await message.channel.send(display_stages(stages))
            await message.channel.send('拒否するステージを選択(1つ目)')
            reply = await client.wait_for("message", check=starter_stage_check)
            await message.channel.send('{} が拒否されました'.format(stages[int(reply.content)]))

            stage_idx, stages = make_stage_list(stage_idx, reply)
            await message.channel.send('残りステージ')
            await message.channel.send(display_stages(stages))
            await message.channel.send('拒否するステージを選択(2つ目)')
            reply = await client.wait_for("message", check=starter_stage_check)
            await message.channel.send('{} が拒否されました'.format(stages[int(reply.content)]))
            

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
    