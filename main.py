import discord
from discord.ext import commands
import sys
import pathlib
import sqlite3

token = 'MTIwODQyNjYyODczMzIwNjY0MA.GSUMNb.HSukolFELqAoBI83ZeMINDQ961r1vSSZnm3Tw4'
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='!')
script_path = pathlib.Path(sys.argv[0]).parent
sql = sqlite3.connect(script_path / 'users.db')
db = sql.cursor()

@bot.event
async def on_ready():
    print(f'Бот запущен!')
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot is True:
                pass
            else:
                cursor = db.execute(f'SELECT id FROM users WHERE id = {member.id}')
                if cursor.fetchone()==None:
                    db.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', (member.id, '`не введено`', '`не введено', 0))
                    sql.commit()

@bot.event
async def on_member_join(member: discord.Member):
    if member.bot is True:
        pass
    else:
        cursor = db.execute(f'SELECT id FROM users WHERE id = {member.id}')
        if cursor.fetchone()==None:
            db.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', (member.id, '`не введено`', '`не введено', 0))
            sql.commit()

@bot.event
async def on_guild_join(guild: discord.Guild):
    for member in guild.members:
        if member.bot is True:
            pass
        else:
            cursor = db.execute(f'SELECT id FROM users WHERE id = {member.id}')
            if cursor.fetchone()==None:
                db.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', (member.id, '`не введено`', '`не введено', 0))
                sql.commit()

@bot.command(name='юзер')
async def user(ctx: commands.Context, user: discord.Member = None):
    if not user:
        for name in db.execute(f'SELECT name FROM users WHERE id = {ctx.author.id}'):
            for city in db.execute(f'SELECT city FROM users WHERE id = {ctx.author.id}'):
                for balance in db.execute(f'SELECT balance FROM users WHERE id = {ctx.author.id}'):
                    embed=discord.Embed(title='Информация о Вас', description=f'Имя: {name[0]}\nГород: {city[0]}\nБаланс: {balance[0]}')
                    await ctx.reply(embed=embed)
    if user:
        check = db.execute(f'SELECT id WHERE id = {user.id}')
        if check.fetchone()!=None:
            for name in db.execute(f'SELECT name FROM users WHERE id = {user.id}'):
                for city in db.execute(f'SELECT city FROM users WHERE id = {user.id}'):
                    for balance in db.execute(f'SELECT balance FROM users WHERE id = {user.id}'):
                        embed=discord.Embed(title=f'Информация о {user}', description=f'Имя: {name[0]}\nГород: {city[0]}\nБаланс: {balance[0]}')
                        await ctx.reply(embed=embed)
        else:
            await ctx.reply(f'Пользователь не найден, возможно он бот.')

@bot.command(name='изменить')
async def change(ctx: commands.Context, name: str, city: str):
    await ctx.reply(f'Успешно.')
    db.execute(f'UPDATE users SET name = ? WHERE id = ?', (name, ctx.author.id))
    db.execute(f'UPDATE users SET city = ? WHERE id = ?', (city, ctx.author.id))
    sql.commit()



bot.run(token)

