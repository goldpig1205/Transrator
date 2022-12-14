from discord.app_commands import Choice
from discord.ext import commands
from discord.ui import *
from discord import app_commands, SelectOption
import discord
import requests
import openpyxl


bot = commands.Bot(command_prefix="=", intents=discord.Intents.all(), help_command=None)
tree = bot.tree


def check_info(key: str, target: str = 'B'):
    openxl = openpyxl.load_workbook('lang.xlsx')
    wb = openxl.active

    for i in range(2, 20):
        if wb['A' + str(i)].value == key:
            return wb[target + str(i)].value


def setup_choices(input_t: bool):
    openxl = openpyxl.load_workbook('lang.xlsx')
    wb = openxl.active

    return_list = []

    if input_t is True:
        return_list.append(Choice(name="ð ì¸ì´ ê°ì§", value="sr"))

    for i in range(2, 20):
        if wb['A' + str(i)].value is not None:
            return_list.append(Choice(name=f"{wb['C' + str(i)].value} {wb['B' + str(i)].value}", value=wb['A' + str(i)].value))

    return return_list


@bot.event
async def on_guild_join(guild):
    await bot.get_channel(int(831444237596753920)).send(f"{str(guild)} | ìë²ì ì°¸ê°íìµëë¤.\níì¬ ìë² : {len(bot.guilds)}")
    return


@bot.event
async def on_guild_remove(guild):
    await bot.get_channel(int(831444237596753920)).send(f"{str(guild)} | ìë²ìì ëê°ìµëë¤.\níì¬ ìë² : {len(bot.guilds)}")
    return


@bot.event
async def on_ready():
    await tree.sync()
    game = discord.Game("'/ë²ì­ ë¬¸ì¥' ëªë ¹ì´ë¥¼ ì¬ì©í´ë³´ì¸ì.")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f"ííê³  APIë¥¼ ì´ì©í ë²ì­ê¸° ê°ë")


@tree.context_menu(name="ð í´ë¹ ë©ì¸ì§ ë²ì­")
async def translate_this_message(interaction: discord.Interaction, message: discord.Message):
    _client_id = "ì¸ì´ ê°ì§ API ID"
    _client_secret = "ì¸ì´ ê°ì§ API Secret"

    _url = "https://openapi.naver.com/v1/papago/detectLangs"
    _headers = {"X-Naver-Client-Id": _client_id,
                "X-Naver-Client-Secret": _client_secret}

    _data = {'query': message.content.encode('utf-8')}

    _res = requests.post(_url, data=_data, headers=_headers)

    client_id = "ííê³  ë²ì­ API ID"
    client_secret = "ííê³  ë²ì­ API Secret"

    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {"X-Naver-Client-Id": client_id,
               "X-Naver-Client-Secret": client_secret}

    data = {'source': _res.json()['langCode'],
            'target': 'ko',
            'text': message.content.encode('utf-8')}

    res = requests.post(url, data=data, headers=headers)
    try:
        embed = discord.Embed(title=f"{bot.user.name} / ë²ì­ ê²°ê³¼", description=f"\â ë²ì­ì´ ìë£ëììµëë¤.", color=0x00FFBF)
        embed.add_field(name=f"{check_info(_res.json()['langCode'], 'C')} {check_info(_res.json()['langCode'])}", value=f"```\n{message.content}```",
                    inline=False)
        embed.add_field(name=f"{check_info('ko', 'C')} {check_info('ko')}", value=f"```\n{res.json()['message']['result']['translatedText']}```",
                    inline=False)
        embed.set_footer(
        text=f"ì  ë¬¸ì¥ : {len(message.content)}ìã£í ë¬¸ì¥ : {len(res.json()['message']['result']['translatedText'])}ì")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    except KeyError:
        await interaction.response.send_message("\â í´ë¹ ë©ì¸ì§ì ì¸ì´ë **íêµ­ì´**ìëë¤.", ephemeral=True)


class ë²ì­(app_commands.Group):
    @app_commands.command(name="ë¬¸ì¥", description="ìë ¥ë ë¬¸ì¥ì ë²ì­íë ëªë ¹ì´")
    @app_commands.describe(input_ì¸ì´="ë²ì­í  ë¬¸ì¥ì ì¸ì´ë¥¼ ì ííì¸ì.", output_ì¸ì´="ë²ì­ë  ë¬¸ì¥ì ì¸ì´ë¥¼ ì íí´ì£¼ì¸ì.")
    @app_commands.choices(input_ì¸ì´=setup_choices(True), output_ì¸ì´=setup_choices(False))
    async def translate(self, interaction: discord.Interaction, input_ì¸ì´: Choice[str], output_ì¸ì´: Choice[str]):
        class words(Modal, title=f"{bot.user.name} / ë¬¸ì¥ ë²ì­"):
            content = TextInput(
                label=f"{input_ì¸ì´.name} -> {output_ì¸ì´.name}",
                min_length=1,
                max_length=1000,
                required=True,
                placeholder="ë²ì­í  ë¬¸ì¥ì ìë ¥íì¸ì.",
                style=discord.TextStyle.long
            )

            async def on_submit(self, inter: discord.Interaction):
                def input_():
                    if input_ì¸ì´.value == "sr":
                        _client_id = "ì¸ì´ ê°ì§ API ID"
                        _client_secret = "ì¸ì´ ê°ì§ API Secret"

                        _url = "https://openapi.naver.com/v1/papago/detectLangs"
                        _headers = {"X-Naver-Client-Id": _client_id,
                                    "X-Naver-Client-Secret": _client_secret}

                        _data = {'query': self.content.value.encode('utf-8')}

                        _res = requests.post(_url, data=_data, headers=_headers)

                        return _res.json()['langCode']

                    else:
                        return input_ì¸ì´.value

                client_id = "ííê³  ë²ì­ API ID"
                client_secret = "ííê³  ë²ì­ API Secret"

                url = "https://openapi.naver.com/v1/papago/n2mt"
                headers = {"X-Naver-Client-Id": client_id,
                           "X-Naver-Client-Secret": client_secret}

                data = {'source': input_(),
                        'target': output_ì¸ì´.value,
                        'text': self.content.value.encode('utf-8')}

                res = requests.post(url, data=data, headers=headers)

                try:
                    embed = discord.Embed(title=f"{bot.user.name} / ë²ì­ ê²°ê³¼", description=f"\â ë²ì­ì´ ìë£ëììµëë¤.", color=0x00FFBF)
                    embed.add_field(name=f"{check_info(input_(), 'C')} {check_info(input_())}", value=f"```\n{self.content.value}```", inline=False)
                    embed.add_field(name=f"{output_ì¸ì´.name}", value=f"```\n{res.json()['message']['result']['translatedText']}```", inline=False)
                    embed.set_footer(text=f"ì  ë¬¸ì¥ : {len(self.content.value)}ìã£í ë¬¸ì¥ : {len(res.json()['message']['result']['translatedText'])}ì")
                    await inter.response.send_message(embed=embed, ephemeral=True)
                
                except Exception as e:
                    await inter.response.send_message(f"\â ì¤ë¥ ë°ì, ë¤ì ìëí´ì£¼ì¸ì.\n```\n- {e}```")

        await interaction.response.send_modal(words())


    @app_commands.describe(url="íêµ­ì´ë¡ ë²ì­í  ì¹ì¬ì´í¸ URLì ìë ¥í´ì£¼ì¸ì.")
    @app_commands.command(name="ì¹ì¬ì´í¸", description="ì¹ì¬ì´í¸ ìì²´ë¥¼ ë²ì­íë ëªë ¹ì´")
    async def site(self, interaction: discord.Interaction, url: str):
        if "https://" not in url:
            await interaction.response.send_message("\â ì¬ë°ë¥¸ ì¹ì¬ì´í¸ URLì´ ìëëë¤.", ephemeral=True)

        embed = discord.Embed(description=f"[ì¬ê¸°](https://papago.naver.net/website?locale=ko&source=auto&target=ko&url={url})ë¥¼ í´ë¦­íì¬ ì´ëíì¸ì.", color=0x00FFBF)
        await interaction.response.send_message(embed=embed, ephemeral=True)


tree.add_command(ë²ì­())


bot.run("your token")
