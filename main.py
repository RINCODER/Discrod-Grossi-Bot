import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from config import *
import time
from nextcord.ui import Button, View
import random
import json
bd = {} #Локальная база чата ЛС

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix= "/", intents = intents)


def update_db():
    global bd
    try:
        with open('DB.txt', 'r', encoding='utf-8') as file:  # Заполнение данных в переменную
            d1 = json.load(file)
            bd.update(d1)  # Обновление данных
    except json.decoder.JSONDecodeError:
        pass


def write_db():
    global bd
    open('DB.txt', 'w').close()
    with open('DB.txt', 'w', encoding='utf-8') as file:  # Выгрузка данных в txt файл
        json.dump(bd, file, indent=3, ensure_ascii=False)

@client.event
async def on_ready():
    links = ["https://i.gifer.com/2GU.gif","https://i.gifer.com/HIhn.gif","https://i.gifer.com/Fdfb.gif","https://i.gifer.com/2oT.gif","https://i.gifer.com/C6Gq.gif","https://i.gifer.com/6YZS.gif","https://i.gifer.com/3DIi.gif","https://i.gifer.com/11tY.gif"]
    embed = nextcord.Embed(colour= nextcord.Color.random())
    update_db()
    if (bd["сумма контрактов за прошлую неделю"] > bd['сумма контрактов за неделю']):
        result = f"📉| В этот раз мы заработали меньше на {bd['сумма контрактов за прошлую неделю'] - bd['сумма контрактов за неделю']}"
    elif (bd["сумма контрактов за прошлую неделю"] < bd['сумма контрактов за неделю']):
        result = f"📈| В этот раз мы заработали больше на {bd['сумма контрактов за неделю'] - bd['сумма контрактов за прошлую неделю']}"
    else:
        result = f"🍀| В этот раз мы заработали {bd['сумма контрактов за неделю']} прибыль стабильна."

    update_db()
    embed.add_field(name=f"⏰ {time.strftime('%A, %d %B %y %H:%M:%S')}",value=f"📆 Новая неделя, новая отчетность! За работу братья\n\n💰 За эту неделю было заработано с контрактов: {bd['сумма контрактов за неделю']}\n\n{result}")
    embed.set_thumbnail(links[random.randint(0, 7)])
    embed.set_footer(text="С любовью от руководства семьи Grossi")
    print(f'///////////////////////////////////////////\n  [{time.strftime("%H:%M:%S")}][Инфо] Бот успешно запущен\n///////////////////////////////////////////')
    channel = client.get_channel(chanelTime)
    print(time.strftime("%A"),time.strftime("%H:%M"))

    if (time.strftime("%A") == "Monday"):
        update_db()
        bd['сумма контрактов за прошлую неделю'] = bd['сумма контрактов за неделю']
        bd['сумма контрактов за неделю'] = 0
        write_db()
        await channel.send(embed=embed)

@client.slash_command(name="ping",description="Проверка работоспособности бота" ,guild_ids=[id])
async def ping(interaction: Interaction):
    await interaction.response.send_message("```😜 Я здесь, все работает```")

class DropDown(nextcord.ui.Select):
    def __init__(self):
        SelectOptions = [
            nextcord.SelectOption(label="на монеты", description="Оповестить всех о взятии контракта на монеты",emoji="🪙"),
            nextcord.SelectOption(label="на урожай", description="Оповестить всех о взятии контракта на урожай",emoji="🍇"),
            nextcord.SelectOption(label="на ограбление магазинов", description="Оповестить всех о взятии контракта на ограбление магазинов", emoji="🏪"),
            nextcord.SelectOption(label="на рыбу", description="Оповестить всех о взятии контракта на рыбу",emoji="🎣"),
        ]
        super().__init__(placeholder="📄 Выберите один из пунктов", min_values=1,max_values=1,options=SelectOptions)

    async def callback(self, ctx):
        await ctx.message.delete()
        CloseContract = Button(label="Контракт завершен", emoji="✅", style= nextcord.ButtonStyle.secondary)
        channel = client.get_channel(idChatContract)
        async def CloseContractCallBack(interactions):
            print(f"Селектор выбора: {self.values[0]}")
            update_db()
            if self.values[0] == "на монеты":
                bd["сумма контрактов за неделю"] += 300000
                await channel.send(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n-----------------------+300.000$------------------------------")
                await interactions.response.send_message(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n-----------------------+300.000$------------------------------")
            elif self.values[0] == "на урожай":
                bd["сумма контрактов за неделю"] += 300000
                await channel.send(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n-----------------------+300.000$------------------------------")
                await interactions.response.send_message(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n-----------------------+300.000$------------------------------")
            elif self.values[0] == "на ограбление магазинов":
                bd["сумма контрактов за неделю"] += 1700000
                await channel.send(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n---------------------+1.700.000$------------------------------")
                await interactions.response.send_message(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n---------------------+1.700.000$------------------------------")
            elif self.values[0] == "на рыбу":
                bd["сумма контрактов за неделю"] += 2500000
                await channel.send(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n---------------------+2.500.000$------------------------------")
                await interactions.response.send_message(f"----------------<@&{notification}>-----------------------\n             🔒 Контракт был успешно завершен\n---------------------+2.500.000$------------------------------")
            write_db()

        CloseContract.callback = CloseContractCallBack
        myview = View(timeout=None)
        myview.add_item(CloseContract)
        await ctx.send(f'<@&{notification}> | Внимание был активирован контракт  {self.values[0]} | Активировал: {ctx.user.mention}\n*☁ После выполнения условия контракта нажмите на кнопку ниже*',view = myview)
        await channel.send(f'<@&{notification}> | Внимание был активирован контракт  {self.values[0]} | Активировал: {ctx.user.mention}\n*⌚ У вас есть 12 часов на выполнение контракта, выполняйте быстрее 😉*')


class DropDownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropDown())

@client.slash_command(name="contract",description="Оповещение о взятии контракта" ,guild_ids=[id])
async def contract(interaction: Interaction):
    view = DropDownView()
    await interaction.response.send_message("📄 Какой контракт активирован?",view=view)

@client.slash_command(name="clear",description="Это команда работает только для администраторов",default_member_permissions=8,guild_ids=[id],)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit = amount+2)
    await ctx.response.send_message(f"🗑️( Удалено {amount} сообщений | Активировал: {ctx.user.mention}")


class FormAcess(nextcord.ui.Modal):

    def __init__(self):
        super().__init__("Форма регистрации на сервер",)

        self.emNickName = nextcord.ui.TextInput(label= "Ваш ник",min_length=5,max_length=30,required=True,placeholder= "Введите свой ник")
        self.add_item(self.emNickName)

        self.emCID = nextcord.ui.TextInput(label="Ваш CID",min_length=2,max_length=10,required=True,placeholder="Введите ваш CID на сервере")
        self.add_item(self.emCID)

        self.emAccount = nextcord.ui.TextInput(label="Ваш банковский счет",min_length=3,max_length=25,required=True,placeholder="Введите ваш банковский счет")
        self.add_item(self.emAccount)

        self.emRealName = nextcord.ui.TextInput(label="Ваше реальное имя",min_length=3,max_length=25,required=True,placeholder="Введите ваше реальное имя, не стесняйтесь 😉")
        self.add_item(self.emRealName)

        self.emScreen = nextcord.ui.TextInput(label="Скриншот статистики",min_length=5,max_length=400,required=True,placeholder="Ссылка на igmur или yapix")
        self.add_item(self.emScreen)

    async def callback(self, interaction: Interaction) -> None:
        try:
            Nickname = self.emNickName.value
            CID = self.emCID.value
            Account = self.emAccount.value
            RealName = self.emRealName.value
            screen = self.emScreen.value
            if ((screen[-3:] != "png") and (screen[-3:] != "peg") and (screen[-3:] != "jpg")):
                raise IOError("Not image URL: Ссылка не является картинкой")
            em = nextcord.Embed(title=f"**🫂Новый участник: {RealName}**",description=f"**🗒️ Ник: {Nickname}\n\n🔢 CID: {CID}\n\n💳 Банковский счет: {Account}\n\n🖼️ Скриншот статистики: {screen}**",colour=nextcord.Color.random())
            em.set_thumbnail(screen)
            userid = interaction.user
            await userid.edit(nick=f"{RealName} ({Nickname})")
            if ((Nickname.lower()).find("grossi")) != -1:
                setRole = nextcord.utils.get(userid.guild.roles,id = GrossiRole)
            else:
                setRole = nextcord.utils.get(userid.guild.roles, id=OtherRole)
            RoleEvent = nextcord.utils.get(userid.guild.roles,id = notification)
            await userid.add_roles(RoleEvent)
            await userid.add_roles(setRole)
            return await interaction.response.send_message(embed = em)
        except:
            return await interaction.response.send_message(
                "```❌ Вы ввели не ссылку на изображение, введите ссылку на изображение (Правой клавишей мышки по изображению и скопировать адрес изображения)``` https://i.imgur.com/FiXzx1a.png)",ephemeral=True)

@client.slash_command(name="reg",description="Запрос доступа на сервер",guild_ids=[id])
@commands.has_permissions(change_nickname=True)
async def reg(interaction:Interaction):
    await interaction.response.send_modal(FormAcess())

@client.slash_command(name="ping",description="Проверка работоспособности бота" ,guild_ids=[id])
async def ping(interaction: Interaction):
    await interaction.response.send_message(f"```[PING: {round(client.latency * 1000)}ms] 😜 Я здесь, все работает```")

@client.slash_command(name="clearallrole",description="Обнуляет всем роли",default_member_permissions=8,guild_ids=[id])
async def clearallrole(interaction):
  for member in interaction.guild.members:
    if member.id == interaction.guild.me.id:
      continue

    to_replace = [role for role in member.roles if (role.is_integration() or role.is_default() or role.is_bot_managed())]
    try:
      await member.edit(roles=to_replace)
      print(f"Removed all roles from {member} ({member.id})")
    except Exception as err:
      print(f"{err}\nFailed to remove all roles from {member} ({member.id})")


class FormInvite(nextcord.ui.Modal):

    def __init__(self):
        super().__init__("Форма приглашения нового участника",)

        self.emNickName = nextcord.ui.TextInput(label= "Ваш ник",min_length=5,max_length=30,required=True,placeholder= "Введите свой ник")
        self.add_item(self.emNickName)

        self.emAddUser = nextcord.ui.TextInput(label="Ник приглашенного",min_length=3,max_length=25,required=True,placeholder="Введите ник приглашенного")
        self.add_item(self.emAddUser)

        self.emUrl = nextcord.ui.TextInput(label="Ссылка на форму приглашенного (от бота /reg)",min_length=5,max_length=400,required=True,placeholder="Скопируйте ссылку формы от бота")
        self.add_item(self.emUrl)

    async def callback(self, interaction: Interaction) -> None:
        Nickname = self.emNickName.value
        user = self.emAddUser.value
        url = self.emUrl.value
        em = nextcord.Embed(title=f"**🫂{Nickname} пригласил нового участника**",description=f"**🗒️ Ник нового участника: {user}\n\n🔗 Ссылка на форму от бота (/reg){url}**",colour=nextcord.Color.random())
        em.set_thumbnail("https://cdn-icons-png.flaticon.com/512/1177/1177443.png")
        return await interaction.response.send_message(embed = em)

@client.slash_command(name="inv",description="Форма о приглашонном новом участнике",guild_ids=[id])
async def inv(interaction:Interaction):
    await interaction.response.send_modal(FormInvite())


class FormQuest(nextcord.ui.Modal):

    def __init__(self):
        super().__init__("Форма отчета по ежедневкам",)

        self.emNick = nextcord.ui.TextInput(label= "Ваш ник",min_length=5,max_length=25,required=True,placeholder= "Введите сюда свой ник")
        self.add_item(self.emNick)

        self.emSecret = nextcord.ui.TextInput(label= "Секретная поссылка",min_length=2,max_length=10,required=True,placeholder= "Выполнен или нет")
        self.add_item(self.emSecret)

        self.emCrime = nextcord.ui.TextInput(label="Криминальный груз",min_length=2,max_length=10,required=True,placeholder="Выполнен или нет")
        self.add_item(self.emCrime)


    async def callback(self, interaction: Interaction) -> None:
        Nick = self.emNick.value
        Secret = self.emSecret.value
        Crime = self.emCrime.value
        em = nextcord.Embed(title=f"**☑ {Nick} отправил отчет о контракте**",description=f"**📦 Секретная поссылка: {Secret}\n\n🚚 Криминальный груз: {Crime}**",colour=nextcord.Color.random())
        em.set_thumbnail("https://cdn-icons.flaticon.com/png/512/5545/premium/5545099.png?token=exp=1655654681~hmac=0dcc157bd4e3e75392db9c4346eea6dd")
        return await interaction.response.send_message(embed = em)

@client.slash_command(name="quest",description="Отчет о ежедневках",guild_ids=[id])
async def quest(interaction:Interaction):
    await interaction.response.send_modal(FormQuest())


class FormAFK(nextcord.ui.Modal):

    def __init__(self):
        super().__init__("Форма отчета о неактиве",)

        self.emNick = nextcord.ui.TextInput(label= "Ваш ник",min_length=5,max_length=30,required=True,placeholder= "Впишите сюда свой ник")
        self.add_item(self.emNick)

        self.emReason = nextcord.ui.TextInput(label="Причина",min_length=5,max_length=30,required=True,placeholder="Впишите сюда причину")
        self.add_item(self.emReason)

        self.emTime = nextcord.ui.TextInput(label="Время отсутствия",min_length=5,max_length=30,required=True,placeholder="Пример: 01.01.2001 - 02.02.2002")
        self.add_item(self.emTime)

    async def callback(self, interaction: Interaction) -> None:
        Nick = self.emNick.value
        Reason = self.emReason.value
        time = self.emTime.value
        em = nextcord.Embed(title=f"**💤 {Nick} заполнил заявку на неактив**",description=f"**📄 Ник: {Nick}\n\n🛌 Причина: {Reason}\n\n🗓️ Дата отсутствия:{time}**",colour=nextcord.Color.random())
        em.set_thumbnail("https://cdn-icons-png.flaticon.com/512/852/852534.png")
        return await interaction.response.send_message(embed = em)

@client.slash_command(name="afk",description="Заявка на неактив",guild_ids=[id])
async def afk(interaction:Interaction):
    await interaction.response.send_modal(FormAFK())

@client.slash_command(name="checkdb",description="Информация в БД",default_member_permissions=8,guild_ids=[id],)
async def checkdb(ctx):
    update_db()
    await ctx.response.send_message(f"```♨️База данных:\nCумма контрактов за неделю: {bd['сумма контрактов за неделю']}\nCумма контрактов за прошлую неделю: {bd['сумма контрактов за прошлую неделю']}\n----------------------------------------```")

print("UPDATE ПРОШЕЛ УСПЕШНО| V 22.06.2022")
client.run(token)