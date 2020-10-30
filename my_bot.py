import asyncio
import discord
import re
import requests
from urllib import parse
from discord.ext import commands
client = commands.Bot(command_prefix='-')

import os
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import warnings
import unicodedata
import json
import time

#시작 로딩
@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)
    print("===========")
    await client.change_presence(activity=discord.Streaming(name="방송",platform="Twitch",details="코겜님이",url="http://twitch.tv/kogame8",type=discord.ActivityType.streaming))

#이벤트 부분
@client.event#필터링
async def on_message(message):
    content = message.content 
    guild = message.guild 
    author = message.author 
    channel = message.channel     
    bad = ['ㅅㅂ','시발','씨발']
    for i in bad:
           if i in content:
               await message.channel.send("바른말 고운말을 사용합시다.")
               await message.delete()
    if content.startswith("!확인"):
        embed=discord.Embed(title=f"서버 확인", description=f"확인용 embed", color=0xf3bb76)
        embed.add_field(name=f"서버이름", value=message.guild,inline=False)
        embed.add_field(name=f"채널이름", value=message.channel,inline=False)
        embed.add_field(name=f"사용자이름", value=message.author,inline=False)
        await message.channel.send(embed=embed)    
    if content.startswith("!배그전적"):
        if len(message.content.split(" ")) == 1:
            await message.channel.send("닉네임을 입력해 주세요")
        elif len(message.content.split(" ")) == 2:
            await message.channel.send("TPP/FPP 를 입력해주세요")
        elif ''.join((message.content).split(' ')[2:]) != "TPP" and ''.join((message.content).split(' ')[2:]) != "FPP" :
            await message.channel.send("TPP/FPP 를 입력해주세요")
        else:
            playerNickname = ''.join((message.content).split(' ')[1])
                            # 'https://dak.gg/profile/Twitch_kogame8/pc-2018-09/steam'
                        # 'https://dak.gg/profile/Twitch_kogame8'
            URL1 = "https://dak.gg/profile/"
            testURL = URL1 + playerNickname
            
            html = urlopen(testURL)
            html = BeautifulSoup(html,'html.parser')


                # 경쟁전 정보가 담겨있는 레이아웃 정보

                 # squad ranked Item : 경쟁전 정보 존재 squad ranked Item not found : 경쟁전 정보 미존재.

                # index 0: fpp 1 : tpp
            rankElements = html.findAll('div',{'class' : re.compile('squad ranked [A-Za-z0-9]')})
            
            if ''.join((message.content).split(' ')[2]) == "FPP":
                fR = rankElements[1]
                if rankElements[1].find('div',{'class' : 'no_record'}) != None: # 인덱스 0 : 경쟁전 fpp -> 정보가 있는지 없는지 유무를 판별한다.
                    await message.channel.send("해당 경쟁전 정보가 존재하지 않습니다.")
                else:
                    tierMedalImage = fR.find('div',{'class' : 'grade-info'}).img['src']
                    tierInfo = fR.find('div',{'class' : 'grade-info'}).img['alt']
                    RPScore = fR.find('div',{'class' : 'rating'}).find('span',{'class' : 'caption'}).text
                    if (fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'rank'}) == None):
                        topRatioRank = "배치중"
                    else:
                        topRatioRank = fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'rank'}).text        
                    mainStatsLayout = fR.find('div',{'class' : 'stats'})                    
                    statsList = mainStatsLayout.findAll('p',{'class' : 'value'})
                    for r in range(0,len(statsList)):
                        statsList[r] = statsList[r].text.strip().split('\n')[0]
                    http = "http:"
                    Medal = http+tierMedalImage
                    embed=discord.Embed(title="배그 전적",description="시즌9 티어.",color=0x00ff56)
                    embed.set_author(name="배그전적",icon_url=Medal)
                    embed.set_thumbnail(url=Medal)
                    embed.add_field(name="티어", value=tierInfo , inline=True)
                    embed.add_field(name="점수", value=RPScore , inline=True)
                    embed.add_field(name="랭킹", value=topRatioRank, inline=False)
                    embed.add_field(name="KDA", value=statsList[0] , inline=True)
                    embed.add_field(name="승률", value=statsList[1] , inline=True)
                    embed.add_field(name="딜량", value=statsList[3] , inline=True)       
                    await message.channel.send(embed=embed)
                    
            elif ''.join((message.content).split(' ')[2]) == "TPP":
                fR = rankElements[0]
                if rankElements[0].find('div',{'class' : 'no_record'}) != None: # 인덱스 0 : 경쟁전 fpp -> 정보가 있는지 없는지 유무를 판별한다.
                    await message.channel.send("해당 경쟁전 정보가 존재하지 않습니다.")
                else:               
                    tierMedalImage = fR.find('div',{'class' : 'grade-info'}).img['src']
                    tierInfo = fR.find('div',{'class' : 'grade-info'}).img['alt']
                    RPScore = fR.find('div',{'class' : 'rating'}).find('span',{'class' : 'caption'}).text
                    if (fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'rank'}) == None):
                        topRatioRank = "배치중"
                    else:
                        topRatioRank = fR.find('p',{'class' : 'desc'}).find('span',{'class' : 'rank'}).text    
                    mainStatsLayout = fR.find('div',{'class' : 'stats'})                    
                    statsList = mainStatsLayout.findAll('p',{'class' : 'value'})
                    for r in range(0,len(statsList)):
                        statsList[r] = statsList[r].text.strip().split('\n')[0]            
                    http = "http:"
                    Medal = http+tierMedalImage
                    embed=discord.Embed(title="배그 전적",description="시즌9 티어.",color=0x00ff56)
                    embed.set_author(name="배그전적",icon_url=Medal)
                    embed.set_thumbnail(url=Medal)
                    embed.add_field(name="티어", value=tierInfo , inline=True)
                    embed.add_field(name="점수", value=RPScore , inline=True)
                    embed.add_field(name="랭킹", value=topRatioRank, inline=False)
                    embed.add_field(name="KDA", value=statsList[0] , inline=True)
                    embed.add_field(name="승률", value=statsList[1] , inline=True)
                    embed.add_field(name="딜량", value=statsList[3] , inline=True)       
                    await message.channel.send(embed=embed)    
    await client.process_commands(message)
           
#@client.event #서버 접속시 메세지
async def on_member_join(member):
    await member.guild.get_channel(758205568858456066).send(member.mention + "님이 새롭게 접속했습니다. 환영해주세요!")
    await member.send('```코겜님이 만든 봇이 서버에서 활동중입니다\n현재 상태 : Test```')

#@client.event #서버 퇴장시 메세지
async def on_member_remove(member):
    await member.guild.get_channel(758205568858456066).send(member.mention + "님이 서버에서 퇴장했습니다....")

#명령어 부분
@client.command(name='입장')
async def voice_join(ctx):
    if(ctx.author.voice==None):
        await ctx.send('채널에 입장후 명령어를 입력해주세요')
    else:
        channel=ctx.author.voice.channel
        if(ctx.voice_client==None):
            await channel.connect()
        else:
            await ctx.send('봇이 이미 접속중이에요')  

@client.command(name='퇴장')
async def voice_leave(ctx):
    if(ctx.voice_client==None):
       await ctx.send('봇이 접속중이 아니라 나가질 못해요')
    else:
        await ctx.voice_client.disconnect()

@client.command(name='청소')
async def _clear(ctx, *, amount=0):
    if(1 < amount < 100):
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send("2~99위 숫자를 입력해주세요")
            
client.run(os.environ[`token`])

