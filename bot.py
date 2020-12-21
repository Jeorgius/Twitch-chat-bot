import os  # for importing env vars for the bot to use
from twitchio.ext import commands

from events.factory import EventFactory

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

bot_name = os.environ['BOT_NICK'].lower()
event_factory = EventFactory(bot_name)


@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me Mwhahahahaha!")


@bot.event
async def event_message(ctx):
    """Runs every time a message is sent in chat."""

    msg = ctx.content
    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == bot_name:
        return

    # await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)
    answer = event_factory.produce_event(ctx).get_answer()

    if answer != '':
        await ctx.channel.send(answer.format(author=ctx.author.name))


@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')


if __name__ == "__main__":
    bot.run()
