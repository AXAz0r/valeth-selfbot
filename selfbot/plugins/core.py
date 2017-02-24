import discord
from discord.ext import commands

import inspect
import subprocess


def setup(bot):
    bot.add_cog(Core(bot))
    setup_events(bot)


def setup_events(bot):
    @bot.event
    async def on_ready():
        print(f"logged in as {bot.user.name}\n")

        game = discord.Game(name=bot.config['bot']['game'])

        # status = discord.Status.idle
        await bot.change_presence(game=game)


class Core(object):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def game(self, *, message: str):
        self.config['bot']['game'] = message
        self.config.save('game', message)
        game = discord.Game(name=message)

        await self.bot.change_presence(game=game)

    @commands.command()
    async def avatar(self, member: discord.Member):
        if member is None:
            member = self.bot.user

        url = member.avatar_url

        await self.bot.say(url)

    @commands.command(name='evaluate', aliases=['eval', 'python', 'py'],
                      pass_context=True, hidden=True)
    async def _evaluate(self, ctx, *, code: str):
        code = code.strip('` ')
        result = None

        if code.startswith('py'):
            code = code.partition('\n')[2]

        env = {
            'bot':     self.bot,
            'ctx':     ctx,
            'message': ctx.message,
            'server':  ctx.message.server,
            'channel': ctx.message.channel,
            'author':  ctx.message.author
        }

        env.update(globals())

        try:
            result = eval(code, env)

            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            result = f'{type(e).__name__}: {str(e)}'

        await self.bot.say(f'```py\n{result}\n```')

    @commands.command(name='system', hidden=True)
    async def _system(self, *, cmd):
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = proc.stdout.read().decode()
        await self.bot.say(f'```\n{out}\n```')
