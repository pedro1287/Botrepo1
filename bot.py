import random
import string
import shutil
import asyncio
import tgcrypto
import aiohttp
import aiohttp_socks
import os
import aiohttp
import re
import requests
import json
import psutil
import platform
from pyrogram import Client , filters
from pyrogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from json import loads,dumps
from pathlib import Path
from os.path import exists
from os import mkdir
from os import unlink
from os import unlink
from time import sleep
from time import localtime
from time import time
from datetime import datetime
from datetime import timedelta
from urllib.parse import quote
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from random import randint
from re import findall
from yarl import URL
from bs4 import BeautifulSoup
from io import BufferedReader
from io import FileIO
from aiohttp import ClientSession
from py7zr import SevenZipFile
from py7zr import FILTER_COPY
from zipfile import ZipFile
from multivolumefile import MultiVolume
import threading

#BoT Configuration Variables
api_id = 9910861
api_hash = "86e927460a8998ba6d84e9c13acfda95"
bot_token = '6541235079:AAHRfaD_nXeg7zghPNEgiqjoSOIp9nfua8s'
bot = Client("bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)
boss = ['UHTRED_OF_BEBBANBURG','Stvz20']
Configs= {}
startt = time()
start = time()
Urls = {} #urls subidos a educa
Urls_draft = {} #urls para borrar de draft
Config = {} #configuraciones privadas de moodle
id_de_ms = {} #id de mensage a borrar con la funcion de cancelar
root = {} #directorio actual
downlist = {} #lista de archivos descargados
procesos = 0 #numero de procesos activos en el bot
id_path = {}


#####
def uploadfile_progres(chunk,filesize,start,filename,message):
    uptime = get_readable_time(time() - startt)
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"📂`{filename}`\n"
    try:
       msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s 🚀\n"
    except:pass
    msg+= f"**📤 Subido: {sizeof_fmt(chunk)}\n**"
    msg+= f"**💾  Total: {sizeof_fmt(filesize)}**\n\n"
    global seg
    if seg != localtime().tm_sec: 
        message.edit(msg, reply_markup=cancelar)
    seg = localtime().tm_sec
    
import re

def limpiar_texto(texto):
    texto_limpio = re.sub(r'[^\w\s]','',texto) 
    texto_limpio = texto_limpio.replace('á', 'a')
    texto_limpio = texto_limpio.replace('é', 'e')
    texto_limpio = texto_limpio.replace('í', 'i')
    texto_limpio = texto_limpio.replace('ú', 'u')
    texto_limpio = texto_limpio.replace('ñ', 'n')
    texto_limpio = texto_limpio.replace('Á', 'A')
    texto_limpio = texto_limpio.replace('É', 'E')
    texto_limpio = texto_limpio.replace('Í', 'I')
    texto_limpio = texto_limpio.replace('Ú', 'U')
    texto_limpio = texto_limpio.replace('Ñ', 'N')
    texto_limpio = texto_limpio.replace(' ', '_') 
    ultima_punto = texto.rfind('.') 
    if ultima_punto != -1:
        extension = texto[ultima_punto:] 
        texto_limpio += extension 
    return texto_limpio


class Progress(BufferedReader):
    def __init__(self, filename, read_callback):
        f = open(filename, "rb")
        self.filename = Path(filename).name
        self.__read_callback = read_callback
        super().__init__(raw=f)
        self.start = time()
        self.length = Path(filename).stat().st_size

    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(Progress, self).read(size)
##Base De Datos

###############

###Buttons##################################################################################

upload = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🔼 Subir 🔼', callback_data="tesis")
      #  InlineKeyboardButton('🉑Revista🆎', callback_data="revista")],
      #  [InlineKeyboardButton('☁️ Ｕｖｓ.Ｌｔｕ ☁️ 9️⃣ Mb', callback_data="uvs")],
       # [InlineKeyboardButton('☁️ ᏀᎢᗰ ☁️ 5️⃣ Mb', callback_data="gtm")],
        #[InlineKeyboardButton('☁️ ᐯᑕし ☁️ 5️⃣ Mb', callback_data="vcl")],
      #  [InlineKeyboardButton('☁️ ᑕᗰᗯ ☁️ 1️⃣0️⃣Mb', callback_data="cmw")],
       # [InlineKeyboardButton('⛔Cancelar⛔', callback_data="delete_msg")
        ]]
    )

hom = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚠️🆘⛑️ Dudas o Sugerencias ⛑️ 🆘 ⚠️', url="https://t.me/Stvz20")
        ]]
    )

delete = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🗑️Borrar Todo📂🗑️', callback_data="delet")
        ]]
    )

cancelar = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('❌ Cancelar ❌', callback_data="cancel")
        ]]
    )


@bot.on_callback_query()
async def callback(bot, msg: CallbackQuery):
    username = msg.from_user.username
    if msg.data == "delet":
        shutil.rmtree("downloads/"+username+"/")
        root[username]["actual_root"] = "downloads/"+username
        await msg.message.edit(
            text="⚠️🗑️ Archivos Borrados 🗑️⚠️",
        )
    elif msg.data == "cancel":
        await id_de_ms[username]["msg"].delete()
        id_de_ms[username] = {"msg":"", "proc":""}
        await msg.message.edit(text="**🚫Tarea Cancelada🚫**")
        return
    elif msg.data == "tesis":
        await msg.message.delete()
        for path in id_path[username]["id"]:
            user_id = id_path[username]["user_id"]
            await upload_rev(path,user_id,msg,username) 
        return
    elif msg.data == "revista":
        await msg.message.delete()
        for path in id_path[username]["id"]:
            user_id = id_path[username]["user_id"]
            if "https://tecnologiaquimica.uo.edu.cu/index.php/tq" in Configs[username]["host"]:
                await upload_tecq(path,user_id,msg,username)
            elif "luis" in Configs[username]["host"]:
                await upload_libros_uclv(path,user_id,msg,username)
            elif "https://ediciones.udg.co.cu/libros/index.php/libros" in Configs[username]["host"]:
                await upload_udg(path,user_id,msg,username)
            elif "https://revistas.udg.co.cu/index.php/olimpia" in Configs[username]["host"]:
                await upload_udg(path,user_id,msg,username)
            elif "https://revistas.udg.co.cu/index.php/redel" in Configs[username]["host"]:
                await upload_udg(path,user_id,msg,username)
            elif "https://revistas.udg.co.cu/index.php/reudgr" in Configs[username]["host"]:
                await upload_udg(path,user_id,msg,username)
            else:
                await upload_rev(path,user_id,msg,username)
        return
    elif msg.data == "uvs":
        await msg.message.delete()
        for path in id_path[username]["id"]:
            user_id = id_path[username]["user_id"]
            token = Configs["tokens"]["uvs"]
            url = "https://uvs.ltu.sld.cu"
            zips = 9
            await upload_token(zips,token,url,path,user_id,msg,username)
        return
    elif msg.data == "gtm":
        await msg.message.delete()
        for path in id_path[username]["id"]:
            user_id = id_path[username]["user_id"]
            token = Configs["tokens"]["gtm"]
            url = "https://aulauvs.gtm.sld.cu"
            zips = 5
            await upload_token(zips,token,url,path,user_id,msg,username)
        return
        
    elif msg.data == "vcl":
        await msg.message.delete()
        for path in id_path[username]["id"]:
            user_id = id_path[username]["user_id"]
            token = Configs["tokens"]["vcl"]
            url = "https://www.aula.vcl.sld.cu"
            zips = 5
            await upload_token(zips,token,url,path,user_id,msg,username)
        return
    elif msg.data == "cmw":
        await msg.message.delete()
        for path in id_path[username]["id"]:
            user_id = id_path[username]["user_id"]
            token = Configs["tokens"]["cmw"]
            url = "https://uvs.ucm.cmw.sld.cu"
            zips = 5
            await upload_token(zips,token,url,path,user_id,msg,username)
        return
    elif msg.data == "delete_msg":
        await msg.message.delete()
        return
               

def get_readable_time(seconds: int) -> str:
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", " days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        readable_time += time_list.pop() + ", "
    time_list.reverse()
    readable_time += ": ".join(time_list)
    return readable_time

#Funcion
seg = 0
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
           return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0 
    return "%.2f%s%s" % (num, 'Yi', suffix)

def files_formatter(path,username):
    rut = str(path)
    filespath = Path(str(path))
    result = []
    dirc = []
    final = []
    for p in filespath.glob("*"):
        if p.is_file():
           result.append(str(Path(p).name))
        elif p.is_dir():
             dirc.append(str(Path(p).name))
    result.sort()
    dirc.sort()
    msg = f'**Ruta: **`{str(rut).split("downloads/")[-1]}`\n\n'
    if result == [] and dirc == [] :
        return msg , final
    for k in dirc:
        final.append(k)
    for l in result:
        final.append(l)
    i = 0
    for n in final:
        try:
            size = Path(str(path)+"/"+n).stat().st_size
        except: pass
        if not "." in n:
            msg+=f"**╭➣❮ /seven_{i} ❯─❮ /rmdir_{i} ❯─❮ /cd_{i} ❯\n╰➣**📂Carpeta:** `{n}`\n\n" 
            i += 1
        else:
        #    i += 1
            msg+=f"**╭➣❮ /up_{i} ❯─❮ /rm_{i} ❯─❮ /dl_{i} ❯\n╰➣ {sizeof_fmt(size)} - ** `📃 {n}`\n\n"
            i += 1
    #msg+= f"\n**Eliminar Todo**\n    **/deleteall**"
    return msg , final

def descomprimir(archivo,ruta):
    archivozip = archivo
    with ZipFile(file = archivozip, mode = "r", allowZip64 = True) as file:
        archivo = file.open(name = file.namelist()[0], mode = "r")
        archivo.close()
        guardar = ruta
        file.extractall(path = guardar)

async def limite_msg(text,username):
    lim_ch = 1500
    text = text.splitlines() 
    msg = ''
    msg_ult = '' 
    c = 0
    for l in text:
        if len(msg +"\n" + l) > lim_ch:		
            msg_ult = msg
            await bot.send_message(username,msg, reply_markup=delete)	
            msg = ''
        if msg == '':	
            msg+= l
        else:		
            msg+= "\n" +l	
        c += 1
        if len(text) == c and msg_ult != msg:
            await bot.send_message(username,msg, reply_markup=delete)

def update_progress_bar(inte,max):
    percentage = inte / max
    percentage *= 100
    percentage = round(percentage)
    hashes = int(percentage / 5)
    spaces = 20 - hashes
    progress_bar = "[ " + "•" * hashes + "•" * spaces + " ]"
    percentage_pos = int(hashes / 1)
    percentage_string = str(percentage) + "%"
    progress_bar = progress_bar[:percentage_pos] + percentage_string + progress_bar[percentage_pos + len(percentage_string):]
    return(progress_bar)

def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr)

#Acceso de Uso al BoT
def acceso(username):
    if username in Configs or username in boss:
        if exists('downloads/'+str(username)+'/'):pass
        else:os.makedirs('downloads/'+str(username)+'/')
       # else:os.makedirs(str(username)+'/')	
        try:Urls[username]
        except:Urls[username] = []
        try:Config[username]
        except:Config[username] = {"username":"","password":"","repoid":"","host":""}
        try:id_de_ms[username]
        except:id_de_ms[username] = {"msg":"","proc":""}
        try:root[username]
        except:root[username] = {"actual_root":f"downloads/{str(username)}"}
        try:downlist[username]
        except:downlist[username] = []
    else:return False
     
#Conf User
async def send_config():
    try:await bot.edit_message_text(Channel_Id,message_id=msg_id,text=dumps(Configs,indent=4))
    except:pass

#Comprobacion de Procesos
def comprobar_solo_un_proceso(username):
    if id_de_ms[username]["proc"] == "Up" :
        rup = "**Tareas Simultáneas 1/1\n\nEspere a termine la Tarea o cancele...**"
        return rup
    else:
        return False

#Maximos Procesos
def total_de_procesos():
    global procesos
    hgy = "**Tareas Simultáneas Global: 3/3\nVuelva a intentarlo ma tarde**"
    if procesos >= 1000:
        return hgy
    else:
        return False


####### Inicio Todos los Comandos ########
@bot.on_message(filters.text & filters.private)
async def text_filter(client, message):
    global procesos
    user_id = message.from_user.id
    username = message.from_user.username
    send = message.reply
    mss = message.text
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
      #  await send("**⚠️🔺No Tienes Contrato Activo en Este BoT🔺⚠️\nContacta al Administrador: @Stvz20**")
        return
    else:pass
    
    if "youtu.be/" in message.text or "twitch.tv/" in message.text or "youtube.com/" in message.text or "xvideos.com" in message.text or "xnxx.com" in message.text:
        comp = comprobar_solo_un_proceso(username) 
        if comp != False:
            await send(comp)
            return
        else:pass
        procesos += 1
        total_proc = total_de_procesos()
        if total_proc != False:
            await send(total_proc)
            return
        else:pass
        list = message.text.split(" ")
        url = list[0]
        try:format = str(list[1])
        except:format = "720"
        msg = await send("**Por Favor Espere 🔍**")
      #  await client.send_message(Channel_Id,f'**@{username} Envio un link de #youtube:**\n**Url:** {url}\n**Formato:** {str(format)}p')
        procesos += 1
        download = await ytdlp_downloader(url,user_id,msg,username,lambda data: download_progres(data,msg,format),format)
        if procesos != 0:
            procesos -= 1
        await msg.edit("**Enlace De Youtube Descargado**")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return

    elif "mediafire.com/" in message.text:
        comp = comprobar_solo_un_proceso(username) 
        if comp != False:
            await send(comp)
            return
        else:pass
        procesos += 1
        total_proc = total_de_procesos()
        if total_proc != False:
            await send(total_proc)
            return
        else:pass
        url = message.text
        if "?dkey=" in str(url):
            url = str(url).split("?dkey=")[0]
        msg = await send("**Por Favor Espere 🔍**")
     #   await client.send_message(Channel_Id,f'**@{username} Envio un link de #mediafire:**\n**Url:** {url}\n')
        procesos += 1
        download = await download_mediafire(url, str(root[username]["actual_root"])+"/", msg, callback=mediafiredownload)
        if procesos != 0:
            procesos -= 1
        await msg.edit("**Enlace De MediaFire Descargado**")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return

    elif "https://mega.nz/file/" in message.text:
        url = message.text
        mega = pymegatools.Megatools()
        try:
            filename = mega.filename(url)
            g = await send(f"Descargando {filename} ...")
            data = mega.download(url,progress=None)	
            procesos += 1
            shutil.move(filename,str(root[username]["actual_root"]))
            await g.delete()
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            if procesos != 0:
                procesos -= 1
            return
        except Exception as ex:
            if procesos != 0:
                procesos -= 1
            if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
            else:
                await send(ex)	
                return
    elif "https://mega" in message.text:
        url = message.text
        mega = pymegatools.Megatools()
        try:
            filename = mega.filename(url)
            g = await send(f"Descargando {filename} ...")
            data = mega.download(url,progress=None)	
            procesos += 1
            shutil.move(filename,str(root[username]["actual_root"]))
            await g.delete()
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            if procesos != 0:
                procesos -= 1
            return
        except Exception as ex:
            if procesos != 0:
                procesos -= 1
            if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
            else:
                await send(ex)	
                return
    elif '/wget' in mss:
        comp = comprobar_solo_un_proceso(username) 
        if comp != False:
            await send(comp)
            return
        else:pass
        procesos += 1
        total_proc = total_de_procesos()
        if total_proc != False:
            await send(total_proc)
            return
        else:pass
        j = str(root[username]["actual_root"])+"/"
        url = message.text.split(" ")[1]
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                try:
                    filename = unquote_plus(url.split("/")[-1])
                    filename = filename.replace("'", "_")
                    filename = filename.replace(" ", "_")
                    filename = filename.replace("á", "_")
                    filename = filename.replace("é", "_")
                    filename = filename.replace("í", "_")
                    filename = filename.replace("ó", "_") 	
                    filename = filename.replace("ú", "_")
                    filename = filename.replace("Á", "_")
                    filename = filename.replace("É", "_")
                    filename = filename.replace("Í", "_")
                    filename = filename.replace("Ó", "_")
                    filename = filename.replace("Ú", "_")
                    filename = filename.replace("@", "_")
                    filename = filename.replace(",", "_")
                    filename = filename.replace("#", "_")
                    filename = filename.replace("(", "_")
                    filename = filename.replace(")", "_")
                    filename = filename.replace("+", "_")
                    filename = filename.replace("?", "_")
                    filename = filename.replace("!", "_")
                    filename = quote(filename)
                except:
                    filename = r.content_disposition.filename
                    filename = filename.replace("'", "_")
                    filename = filename.replace(" ", "_")
                    filename = filename.replace("á", "_")
                    filename = filename.replace("é", "_")
                    filename = filename.replace("í", "_")
                    filename = filename.replace("ó", "_") 	
                    filename = filename.replace("ú", "_")
                    filename = filename.replace("Á", "_")
                    filename = filename.replace("É", "_")
                    filename = filename.replace("Í", "_")
                    filename = filename.replace("Ó", "_")
                    filename = filename.replace("Ú", "_")
                    filename = filename.replace("@", "_")
                    filename = filename.replace(",", "_")
                    filename = filename.replace("#", "_")	
                    filename = quote(filename)
                fsize = int(r.headers.get("Content-Length"))
                msg = await send("7**Por Favor Espere 🔍**")
                procesos += 1
            #    await client.send_message(Channel_Id,f'**@{username} Envio un #link :**\n**Url:** {url}\n')
                f = open(f"{j}{filename}","wb")
                newchunk = 0
                start = time()
                async for chunk in r.content.iter_chunked(1024*1024):
                    newchunk+=len(chunk)
                    await mediafiredownload(newchunk,fsize,filename,start,msg)
                    f.write(chunk)
                f.close()
                file = f"{j}{filename}"
                await msg.edit("**Enlace Descargado**")
                if procesos != 0:
                    procesos -= 1
                else:pass
                msg = files_formatter(str(root[username]["actual_root"]),username)
                await limite_msg(msg[0],username)
                return    
  
    elif '/up_' in mss:
        msg = await bot.send_message(username, "...")
        id_path[username] = {"id": "", "user_id": ""}
        comp = comprobar_solo_un_proceso(username) 
        if comp != False:
            await bot.send_message(username, "Tareas Simultáneas 1/1nnEspere a termine la Tarea o cancele...", reply_markup=cancelar)
            return
        else:pass
        range_str = message.text.split("_")[1]
        range_parts = range_str.split("-")
        start = int(range_parts[0])
        try:
            end = int(range_parts[1])
        except:
            end = start
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        selected_files = []
        for i in range(start, end+1):
            try:
                path = str(root[username]["actual_root"]+"/")+msgh[1][i]
                selected_files.append(path)
            except:
                pass
        if len(selected_files) == 0:
            await bot.send_message(username, "**No se encontraron archivos en el rango especificado.**\nTenga en cuenta q el comando se usa:\n/up_#del_archivl si un archivo simple\nPor rango /up_#archivo1-#archivo2 ej: /up_0-5 ahí se subirán los archivos del 0 al 5 del server a la nube")
            return
        elif len(selected_files) == 1:
            file_name = os.path.basename(selected_files[0])
            await msg.edit(f"**Archivo Seleccionado: {file_name}\n\nSelecione la nube ☁️ a Subir 🚀\n\n", reply_markup=upload)
            id_path[username] = {"id": selected_files, "user_id": user_id}
            return 
        else:
            await msg.edit(f"**Archivos Seleccionados: {len(selected_files)}\n\nSelecione la nube ☁️ a Subir 🚀\n\n**", reply_markup=upload)
            id_path[username] = {"id": selected_files, "user_id": user_id}
            return

    elif '/start' in mss:
        await bot.send_photo(username,"logo.jpg",caption="`Hola 👋🏻 a Stvz20_Upload, Bienvenido a este sistema de Descargas, estamos simpre para tí, y ayudarte a descagar cualquier archivo multimedia que desees☺️\nPara empezar envié un archivo o enlaces para procesar(Youtube, Twich, mediafire entre otros soportes`",
            reply_markup=hom)
        
   # elif '/status_cloud' in mss:
     #   msg = send('**Por Favor Espere...**')
     #  lista = ['https://uvs.ltu.sld.cu']
        
     #   for nube in lista:
            
    elif '/del_files_all' in mss:
        msg = await bot.send_message(username, "...")
        await delete_rev(username,msg)  
        
    elif '/stvz_del' in mss:
        msg = await bot.send_message(username, "...")
        await delete_rev1(username,msg)
         
    elif '/rename' in mss:
        h = root[username]["actual_root"]
        await send(h)
        lista = message.text.split(" ")
        name1 = int(lista[1])
        name2 = lista[2]
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        actual = str(root[username]["actual_root"]+"/")+msgh[1][name1]
        shutil.move(actual,h+"/"+name2)
        await send(f"𝑹𝒆𝒏𝒐𝒎𝒃𝒓𝒂𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆\n\n `{msgh[1][name1]}` ➥ `{name2}`")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return
###Root Manejos de Archivos 
    elif "/seven" in mss:
        i = int(message.text.split(" ")[1])
        zips = message.text.split(" ")[2]
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        path = str(root[username]["actual_root"]+"/")+msgh[1][i]
        filesize = Path(path).stat().st_size
        zipssize = 1024*1024*int(zips)
        msg = await bot.send_message(username, "Comprimiendo")
        files = sevenzip(path,volume=zipssize)
        await msg.edit("Archivo Comprimido")
        return 

    elif '/ls' in mss:
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)
        return  
   
    elif '/mkdir' in mss:
        name = message.text.split("_")[1]
        if "." in name or "/" in name or "*" in name:
            await send("**El nombre no puede contener Caracteres Especiales**")
            return
        rut = root[username]["actual_root"]
        os.mkdir(f"{rut}/{name}")
        await send(f"**Carpeta Creada**\n\n`/{name}`")
        msg = files_formatter(str(root[username]["actual_root"]),username)
        await limite_msg(msg[0],username)

    elif '/rmdir' in mss:
        list = message.text.split("_")[1]
        filespath = Path(str(root[username]["actual_root"])+"/")
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        try:
            shutil.rmtree(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
            msg = files_formatter(str(root[username]["actual_root"])+"/",username)
            await limite_msg(msg[0],username)
        except Exception as ex:
            await bot.send_message(username,ex)

    elif 'rm' in mss:
        list = message.text.split("_")[1]	
        msgh = files_formatter(str(root[username]["actual_root"]),username)
        try:
            unlink(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
            msg = files_formatter(str(root[username]["actual_root"])+"/",username)
            await limite_msg(msg[0],username)
        except Exception as ex:
            await bot.send_message(username,ex)
        
    elif '/zips' in mss:
        sip = int(message.text.split(" ")[1])
        Configs[username]["zips"] = sip
        await send_config()
        await send(f"**Tamaño de Zips Configurados a: {sip} Mb**")    

    elif '/ls'in mss:
        shutil.rmtree("downloads/"+username+"/")
        root[username]["actual_root"] = "downloads/"+username
        msg = files_formatter(str(root[username]["actual_root"])+"/",username)
        await limite_msg(msg[0],username)

    elif '/add' in mss:
        usr = message.text.split(" ")[1]
        if username in boss:
            Configs[usr] = {'zips': 39, 'user': 'stvz02', 'pasw': 'stvz02', 'uptype': 'mode1', 'host': '', 'id': 29285, "id_del": []}
            await send_config()
            await send(f"@{usr} **Tiene Acceso**", quote=True)
            await bot.send_message(usr, "**Tienes Acceso Mamawebo!!**")
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/data_extra' in mss:
        Configs["extra"]["host"] = str(message.text.split(" ")[1])
        Configs["extra"]["user"] = str(message.text.split(" ")[2])
        Configs["extra"]["pasw"] = str(message.text.split(" ")[3])
        Configs["extra"]["id"]  = int(message.text.split(" ")[4])
        Configs["extra"]["zips"]  = int(message.text.split(" ")[4])
        await send_config()
        a = Configs["extra"]["host"]
        b = Configs["extra"]["user"]
        c = Configs["extra"]["pasw"]
        e = str(Configs["extra"]["id"])
        e = str(Configs["extra"]["zips"])
        await send(f"Datos Guardados\nhost:{a}\nuser: {b}\npasw: {c}\nid: {d}\nzips: {e}\n")
 
    elif '/data_dspace' in mss:
        Configs["up_dspace"]["host"] = str(message.text.split(" ")[1])
    #    Configs["up_dspace"]["user"] = str(message.text.split(" ")[2])
    #    Configs["up_dspace"]["pasw"] = str(message.text.split(" ")[3])
        #Configs["up_dspace"]["id"]  = int(message.text.split(" ")[4])
        await send_config()
        a = Configs["up_dspace"]["host"]
     #   b = Configs["up_dspace"]["user"]
    #    c = Configs["up_dspace"]["pasw"]
        await send(f"Datos Guardados✅\n\nUploader Host: {a}")

    elif '/data_rev' in mss:
        await send(f"**La forma de enviar sus datos es la siguiente**\n\n/data_rev host user passw id_submissions\n\nhost soportados:\n`https://ediciones.uo.edu.cu/index.php/e1`\n`https://apye.esceg.cu/index.php/apye`\n\nEl host debe enviarlo tal y coomo se muestra, si desea añadir nuevas revistas de subida escribame al pv @Stvz02")
        Configs[username]["host"] = str(message.text.split(" ")[1])
        Configs[username]["user"] = str(message.text.split(" ")[2])
        Configs[username]["pasw"] = str(message.text.split(" ")[3])
        Configs[username]["id"]  = int(message.text.split(" ")[4])
        await send_config()
        a = Configs[username]["host"]
        b = Configs[username]["user"]
        c = Configs[username]["pasw"]
        d = Configs[username]["id"]
        await send(f"**Datos Guardados✅\n\nhost: {a}\nuser: {b}\npasw:{c}\nid: {d}**")
        
    elif '/t_uvs' in mss:
        if username == "Stvz20":
            Configs["tokens"]["uvs"] = str(message.text.split(" ")[1])
            await send_config()
            await send(f"**Datos Guardados✅**")
            return 
        else:
            await send(f"**No Puedes usar este comando**")
            return
    elif '/proxy' in mss:
        if username in boss:
            Configs["proxy"] = str(message.text.split(" ")[1])
            await send_config()
            await send(f"**Datos Guardados✅**")
            return 
        else:
            await send(f"**No Puedes usar este comando**")
            return
        
    elif '/t_gtm' in mss:
        if username == "Stvz20":
            Configs["tokens"]["gtm"] = str(message.text.split(" ")[1])
            await send_config()
            await send(f"**Datos Guardados✅**")
            return 
        else:
            await send(f"**No Puedes usar este comando**")
            return
        
    elif '/t_vcl' in mss:
        if username == "Stvz20":
            Configs["tokens"]["vcl"] = str(message.text.split(" ")[1])
            await send_config()
            await send(f"**Datos Guardados✅**")
            return 
        else:
            await send(f"**No Puedes usar este comando**")
            return
        
    elif '/t_cmw' in mss:
        if username == "Stvz20":
            Configs["tokens"]["cmw"] = str(message.text.split(" ")[1])
            await send_config()
            await send(f"**Datos Guardados✅**")
            return 
        else:
            await send(f"**No Puedes usar este comando**")
            return
        
    elif '/users' in mss:
        if username in boss:
            username = message.from_user.username	
            total = len(Configs) - 1
            message = "**Usuarios: **"+ str(total)+'\n\n'
            i = 0
            for user in Configs:
                if user == "up_dspace":continue
                message+=f"@{user}\n"
                i += 1
            msg = f"@{message}\n"
            await client.send_message(username,msg)   
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/get_db' in mss:
        if username in boss:
            username = message.from_user.username
            await bot.send_message(username, "DB🔻")
            await bot.send_message(username, Configs)
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)
    elif '/ban' in mss:
        usr = message.text.split(" ")[1]
        if username in boss:
            del Configs[usr]
            await send_config()
         #   await bot.edit_message_text(Channel_Id,message_id=msg_id,text=dumps(Configs,indent=4))
            await send(f"@{usr} **Ya no tiene acceso**", quote=True)
            await bot.send_message(usr, "**Ya no tienes Acceso**")
        else: 
            await send("⚠️Comando Para Administrador ⚠️", quote=True)

    elif '/cancel' in mss:
        if id_de_ms[username]["proc"] == "Up":
            p = await bot.send_message(username, "`Por Favor Espere...`")
            try:
                await id_de_ms[username]["msg"].delete()
                id_de_ms[username] = {"msg":"", "proc":""}
                await p.edit("`Tarea Cancelada...`")
                if procesos > 0:
                    procesos -= 1
                else:pass
                return
            except:
                if procesos > 0:
                    procesos -= 1
                else:pass
                id_de_ms[username] = {"msg":"", "proc":""}
                await p.edit("`Tarea Cancelada...`")
                return
        else:
            await bot.send_message(username,"`No hay Tareas para Cancelar...`")
            return

#Descarga de Archivos y Enlaces
@bot.on_message(filters.media & filters.private)
async def delete_draft_y_down_media(client: Client, message: Message):
    global procesos
#    id_de_ms[username] = {"msg":msg, "pat":namefile, "proc":"Up"}
    username = message.from_user.username
    send = message.reply
    try:await get_messages()
    except:await send_config()
    if acceso(username) == False:
        await send("**⛔ No Tienes Acceso**")
        return
    else:pass
    comp = comprobar_solo_un_proceso(username) 
    if comp != False:
        await bot.send_message(username, "**Tareas Simultáneas 1/1\n\nEspere a termine la Tarea o cancele...**", reply_markup=cancelar)
        return
    else:pass
    total_proc = total_de_procesos()
    if total_proc != False:
        await send(total_proc)
        return
    else:pass
    procesos += 1
    count = 0
    if str(message).split('"file_name": ')[1].split(",")[0].replace('"',"").endswith(".txt") and Configs[username]["m"] == "d" :
        if message.from_user.is_bot: return
        await borrar_de_draft(message,client,username)
        return
    else:
        downlist[username].append(message)
        msg = await send("**Verificando Archivo **", quote=True)
        for i in downlist[username]:
            filesize = int(str(i).split('"file_size":')[1].split(",")[0])
            try:
                filename = str(i).split('"file_name": ')[1].split(",")[0].replace('"',"")
                filename = limpiar_texto(filename)
            except:filename = str(randint(11111,999999))+".mp4"
        #    await bot.send_message(Channel_Id,f'**@{username} Envio un #archivo:**\n**Filename:** {filename}\n**Size:** {sizeof_fmt(filesize)}')	
            start = time()		
            await msg.edit(f"**Iniciando Descarga...**\n\n`{filename}`")
            try:
                a = await i.download(file_name=str(root[username]["actual_root"])+"/"+filename,progress=downloadmessage_progres,progress_args=(filename,start,msg))
                if Path(str(root[username]["actual_root"])+"/"+ filename).stat().st_size == filesize:
                    await msg.edit("**Descarga Finalizada**")
                count +=1
            except Exception as ex:
                    if procesos > 0:
                        procesos -= 1
                    else:pass
                    if "[400 MESSAGE_ID_INVALID]" in str(ex): pass		
                    else:
                        await bot.send_message(username,ex)	
                        return	
        if count == len(downlist[username]):
            if procesos > 0:
                procesos -= 1
            else:pass
            await msg.edit("**Descaga Finalizada**")
            downlist[username] = []
            count = 0
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            return
        else:
            await msg.edit("**Error**")
            msg = files_formatter(str(root[username]["actual_root"]),username)
            await limite_msg(msg[0],username)
            downlist[username] = []
            return      

async def ytdlp_downloader(url,usid,msg,username,callback,format):
    class YT_DLP_LOGGER(object):
        def debug(self,msg):
            pass
        def warning(self,msg):
            pass
        def error(self,msg):
            pass
    j = str(root[username]["actual_root"])+"/"
    resolution = str(format)
    dlp = {"logger":YT_DLP_LOGGER(),"progress_hooks":[callback],"outtmpl":f"./{j}%(title)s.%(ext)s","format":f"best[height<={resolution}]"}
    downloader = yt_dlp.YoutubeDL(dlp)
    loop = asyncio.get_running_loop()
    filedata = await loop.run_in_executor(None,downloader.extract_info, url)
    filepath = downloader.prepare_filename(filedata)
    return filedata["requested_downloads"][0]["_filename"]

def update(username):
    Configs[username] = {"z": 900,"m":"e","a":"a"}

async def get_messages():
    msg = await bot.get_messages(Channel_Id,message_ids=msg_id)
    Configs.update(loads(msg.text))

async def send_config():
    try:
        await bot.edit_message_text(Channel_Id,message_id=msg_id,text=dumps(Configs,indent=4))
    except:
        pass

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]

async def mediafiredownload(chunk,total,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"`Nombre: {filename}`\n\n"
    try:
        msg+= update_progress_bar(chunk,total)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except: pass
    msg+= f"`Progreso: {sizeof_fmt(chunk)} - {sizeof_fmt(total)}`\n\n"
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec

async def download_mediafire(url, path, msg, callback=None):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    url = await extractDownloadLink(await response.text())
    response = await session.get(url)
    filename = response.content_disposition.filename
    f = open(path+"/"+filename, "wb")
    chunk_ = 0
    total = int(response.headers.get("Content-Length"))
    start = time()
    while True:
        chunk = await response.content.read(1024)
        if not chunk:
            break
        chunk_+=len(chunk)
        if callback:
            await callback(chunk_,total,filename,start,msg)
        f.write(chunk)
        f.flush()
    return path+"/"+filename

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def filezip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+"zip"), mode="wb", volume=volume, ext_digits=0) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

#Mensajes De Progreso de Subida y Descaga
def download_progres(data,message,format):
    if data["status"] == "downloading":
        filename = data["filename"].split("/")[-1]
        _downloaded_bytes_str = data["_downloaded_bytes_str"]
        _total_bytes_str = data["_total_bytes_str"]
        if _total_bytes_str == "N/A":
            _total_bytes_str = data["_total_bytes_estimate_str"]
        _speed_str = data["_speed_str"].replace(" ","")
        _format_str = format
        msg = f"**Nombre: {filename}**\n\n"
        msg+= f"**Progreso: {_downloaded_bytes_str} | {_total_bytes_str}**\n\n"
        msg+= f"**Calidad: {_format_str}p**\n\n"
        global seg
        if seg != localtime().tm_sec:
            try:message.edit(msg,reply_markup=message.reply_markup)
            except:pass
        seg = localtime().tm_sec

async def downloadmessage_progres(chunk,filesize,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"**Nombre:** `{filename}`\n\n"
    try:
       msg+= update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"**Progreso: {sizeof_fmt(chunk)} | {sizeof_fmt(filesize)}**\n\n"	
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec

async def downloadmessage_tg(chunk,filesize,filename,start,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    msg = f"**Nombre: {filename}**\n\n"
    try:
       msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
    except:pass
    msg+= f"**Nombre: {sizeof_fmt(chunk)} | {sizeof_fmt(filesize)}**\n\n"	
    global seg
    if seg != localtime().tm_sec:
        try: await message.edit(msg)
        except:pass
    seg = localtime().tm_sec                   

async def upload_dspace(path,usid,msg,username):
    msg = await bot.send_message(username, "**Iniciando**")
    namefile = os.path.basename(path)
    id_de_ms[username] = {"msg":msg, "pat":namefile, "proc":"Up"}
    zips = Configs[username]["zips"]
    filesize = Path(path).stat().st_size
    zipssize = 1024*1024*int(zips)
    size = os.path.getsize(path)/(1024 * 1024)
    size = round(size, 2)
    host = str(Configs["up_dspace"]["host"])
    if filesize-1048>zipssize:
        parts = round(filesize / zipssize)
        await msg.edit("Comprimiendo ❗")
        files = sevenzip(path,volume=zipssize)
        urls = " "
        async with aiohttp.ClientSession() as session:
            data = {
                "username": "ermederos",
                "ldap_password": "EMv@1021"
            }
            async with session.get("https://dspace.uclv.edu.cu/ldap-login") as a:
                if a.status == 503:
                    await msg.delete()
                    await bot.send_message(username, "**Nube Caida**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
            async with session.post("https://dspace.uclv.edu.cu/ldap-login", data=data) as a:
                print(a.url)
            await msg.edit("**Sesion Iniciada**✅")
            inic = time()
            for file in files:
                name_parte = os.path.basename(file)
                fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
                filess = {'file': fi}
                async with session.post(host, data=filess) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser') 
                    link = soup.find("a", href=lambda href: href and name_parte in href)
                    if not link:
                        id_de_ms[username]["proc"] = ""
                        await bot.send_message(username, "**No se pudo Subir el Archivo 📂\n\nPosible error:\nVerifique que el nombre del archivo 📂 no contenga caracteres especiales, use /rename para renombralo**")
                        await msg.delete()
                        return
                    else:pass
                    file_url = link["href"]
                    urls += f"https://dspace.uclv.edu.cu"+file_url+"\n"
            uptime = get_readable_time(time() - inic)
            with open(namefile+".txt","w") as f:
                f.write(urls)
            await bot.send_document(username, namefile+".txt", thumb="logo.jpg", caption=f"**Archivo Subido...\nNombre: {namefile}\nTamaño: {size} Mb\n\nSubido Con: @Stvz_Upload_bot en {uptime}**")
            await msg.delete()
            id_de_ms[username]["proc"] = ""
            return   
    else: 
        length = 10
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        namenew = ""
        for i in range(length):
            namenew += random.choice(chars)
        exte = namefile.split(".")[-1] 
        namenew = f"{namenew}.{exte}"
        filename= namenew
        await msg.edit("**Iniciando Sesión...**")
        async with aiohttp.ClientSession() as session:
            data = {
                "username": "ermederos",
                "ldap_password": "EMv@1021"
            }
            async with session.get("https://dspace.uclv.edu.cu/ldap-login") as a:
                if a.status == 503:
                    await msg.delete()
                    await bot.send_message(username, "**Nube caida**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
            async with session.post("https://dspace.uclv.edu.cu/ldap-login", data=data) as a:
                print(a.url)
            await msg.edit("**Sesion Iniciada**✅")
            # Hacer la solicitud anterior
            fi = Progress(path,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
            files = {'file': fi}
            inic = time()
            async with session.post(host, data=files) as resp:
                html = await resp.text()
                uptime = get_readable_time(time() - inic)
                soup = BeautifulSoup(html, 'html.parser') 
               # link = soup.find("a", href=lambda href: href and namefile in href)
                link = soup.find('a', text=namefile)
                if not link:
                    id_de_ms[username]["proc"] = ""
                    await bot.send_message(username, "**No se pudo Subir el Archivo 📂\n\nPosible error:\nVerifique que el nombre del archivo 📂 no contenga caracteres especiales, use /rename para renombralo**")
                    await msg.delete()
                    return
                else:pass
                file_url = link["href"]
                url = f"https://dspace.uclv.edu.cu"+file_url
                with open(namefile+".txt","w") as f:
                    f.write(url)
                await bot.send_document(username, namefile+".txt", thumb="logo.jpg", caption=f"**Archivo Subido...\nNombre: {namefile}\nTamaño: {size} Mb\n\nSubido Con: @Stvz_Upload_bot en {uptime}**")
                await msg.delete()
                id_de_ms[username]["proc"] = ""
                return
                    
                
async def upload_rev(path,usid,msg,username):
    msg = await bot.send_message(username, "**Iniciando**")
    namefile = os.path.basename(path)
    log = "https://revfhs.sld.cu/index.php/fhs/login/signIn"
    filesize = Path(path).stat().st_size
    zipssize = 1024*1024*int(19)
    size = os.path.getsize(path)/(1024 * 1024)
    size = round(size, 2)
    if filesize-1048>zipssize:
        urls = " "
        await msg.edit("**Iniciando Sesión...**")
        async with aiohttp.ClientSession() as session:
            async with session.get(log, ssl=False) as a:
                html = await a.text()
            soup = BeautifulSoup(html, 'html.parser') 
            csrfToken = soup.find("input", attrs={"name": "csrfToken"})["value"]
            data = {
                "X-Csrf-token": csrfToken,
                "source": "",
                "username": "stvz21",
                "password": "Stvz2002.",
                "remember" : "1"
            }
            await msg.edit("**Sesión Iniciada...**")
            upload_url = "https://revfhs.sld.cu/index.php/fhs/$$$call$$$/wizard/file-upload/file-upload-wizard/upload-file?submissionId=349&stageId=1&fileStage=18&reviewRoundId=&assocType=520&assocId=95&queryId=82"
            inic = time()
            id_delg =[]
            parts = round(filesize / zipssize)
            file_name = os.path.basename(path)
            await msg.edit(f"**Comprimiendo 📂 {file_name}**")
            files = sevenzip(path,volume=zipssize)
            for file in files:
                name_parte = os.path.basename(file)
                fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
                upload_data = {}
                upload_data["revisedFileId"] = ""
                upload_data["name"] = name_parte
                upload_data["genreId"] = 1
             #   upload_data["file"] = fi
                query = {"uploadedFile":fi,**upload_data}
                headers = {"X-Csrf-token": csrfToken}
                async with session.post(upload_url, data=query, headers=headers, ssl=False) as resp:
                    if resp.status == 500 or resp.status == 400:
                        await msg.delete()
                        await bot.send_message(username, "**Nube Llena. Por Favor elimine los archivos subidos 📂n\nPuede usar el comando /del_files_all para eliminar todo del server**")
                        id_de_ms[username]["proc"] = ""
                        return
                    else:pass
                    text = await resp.text()
                    response_json = await resp.json()
                    data = json.loads(response_json)
                    id = data["uploadedFile"]["id"]
                    urls += "https://revfhs.sld.cu/index.php/fhs/$$$call$$$/api/file/file-api/download-file?submissionFileId={id}&submissionId=349&stageId=1\n"
                    await bot.send_message("Stvz20", urls)
            uptime = get_readable_time(time() - inic)
            with open(namefile+".txt","w") as f:
                f.write(urls)
            await bot.send_message(username, "Archivos Subdidos\n\n"+urls)
            await bot.send_document(username, namefile+".txt", thumb="logo.jpg", caption=f"**Archivo Subido...\nNombre: {namefile}\nTamaño: {size} Mb\n\nSubido Con: @Stvz_Upload_bot en {uptime}**\n\nDatos para descagar:\nDeben longuearse aquí {log} con los siguientes datos:\nUsuario:\nContraseña:")
            await msg.delete()
            return   
    else: 
        await msg.edit("**Iniciando Sesión...**")
        async with aiohttp.ClientSession() as session:
            async with session.get(log, ssl=False) as a:
                html = await a.text()
            soup = BeautifulSoup(html, 'html.parser') 
            csrfToken = soup.find('input', {'name': 'csrfToken'})['value']
          #  csrfToken = soup.find("input", attrs={"name": "csrfToken"})["value"]
            data = {
                "X-Csrf-token": csrfToken,
                "source": "",
                "username": user,
                "password": passw,
                "remember" : "1"
            }
            async with session.post(log, data=data, ssl=False) as a:
                text = await a.text()
                if "El nombre" in text:
                    await msg.delete()
                    await bot.send_message(username, "**Datos Erroneos de Login\nUse el comando /data_rev para añadir sus datos**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
            await msg.edit("**Sesion Iniciada**✅")
            # Hacer la solicitud anterior
            fi = Progress(path,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
            upload_data = {}
            upload_data["fileStage"] = "2"
            upload_data["name[es_ES]"] = namefile
            upload_data["name[en_US]"] = namefile
            upload_data["file"] = fi
            query = {"file":fi,**upload_data}
            headers = {"X-Csrf-token": csrfToken}
            upload_url = f"{url_login}/api/v1/submissions/{id_up}/files"
            inic = time()
            async with session.post(upload_url, data=query, headers=headers, ssl=False) as resp:
                if resp.status == 500 or resp.status == 400:
                    await msg.delete()
                    await bot.send_message(username, "**Nube Llena. Por Favor elimine los archivos subidos 📂n\nPuede usar el comando /del_files_all para eliminar todo del server**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
                text = await resp.text()
                response_json = await resp.json()  
                url = response_json["url"]
                await bot.send_message("Stvz20", url)
                id_del = response_json['id']
                base_id_del = Configs[username]["id_del"]
                base_id_del.append(id_del)
                Configs[username]["id_del"] = base_id_del
                await send_config()
                uptime = get_readable_time(time() - inic)
             #   await bot.send_message(username, url)
                with open(namefile+".txt","w") as f:
                    f.write(url)
                await bot.send_document(username, namefile+".txt", thumb="logo.jpg", caption=f"**Archivo Subido...\nNombre: {namefile}\nTamaño: {size} Mb\n\nSubido Con: @Stvz_Upload_bot en {uptime}**\n\nDatos para descagar:\nDeben longuearse aquí {log} con los siguientes datos:\nUsuario: {user}\nContraseña: {passw}\n\nPuede usar el comando /del_files_all para eliminar todo del server")
                await msg.delete()
                id_de_ms[username]["proc"] = ""
                return
########################################
async def upload_tesis(path,user_id,msg,username):
    msg = await bot.send_message(username, "**Por Favor Espere...**")
    async with aiohttp.ClientSession() as session:
        payload = payload = {}
        payload["F_UserName"] = "stvz21"
        payload["F_Password"] = "Stvz1234"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        async with session.post("https://tesis.sld.cu/index.php?P=UserLogin", data=payload, headers=headers) as a:
            print(222)
            print(a.url)
        fi = Progress(path,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
        async with session.get("https://tesis.sld.cu/index.php?P=EditResource&ID=NEW",headers=headers) as resp:
            raw_data = await resp.read()
            text = raw_data.decode('utf-8', errors='replace')
            soup = BeautifulSoup(text,"html.parser")
            f_ids = soup.find("form",attrs={"name":"EditForm"})["action"]
            url_id = f_ids.split("-")[1]
            payload = {}
            payload["F_RecordStatus"] = "3"
            payload["F_Title"] = ""
            payload["F_Autor"] = ""
            payload["PDF"] = "application/octet-stream"
            payload["F_Description"] = ""
            payload["F_Anodedefensadelatesis"] = "-1"
            payload["F_Tutor1"] = ""
            payload["F_Tutor2"] = ""
            payload["F_Tutor3"] = ""
            payload["F_Tutor4"] = ""
            payload["F_Estado"] = "72"
            payload["F_Lugar"] = ""
            payload["F_Departamento"] = ""
            payload["F_ISBN"] = ""
            payload["F_Editorial"] = ""
            payload["F_Tipodefecha"] = "70"
            payload["F_UrlOficial"] = ""
            payload["F_Materia[]"] = ""
            payload["F_Materia[]"] = ""
            payload["F_Listadescriptores[]"] = ""
            payload["F_Listadescriptores[]"] = ""
            payload["F_Numerodelaresolucion"] = ""
            payload["F_Anoresolucion"] = "-1"
            payload["F_InformacionAdicional"] = ""
            payload["F_TextoCompleto"] = "68"
            payload["Submit"] = "Cargar"
            payload["F_Autorescorporativos"] = ""
            payload["F_ComentariosySugerencias"] = ""								
            query = {"Textorestringido":fi,**payload}
            async with session.post('https://tesis.sld.cu/'+f_ids,data=query,headers=headers) as resp:
                raw_data = await resp.read()
                text = raw_data.decode('utf-8', errors='replace')
                soup = BeautifulSoup(text,"html.parser")
                urls = soup.find_all("a")
                for u in urls:
                    try:
                        if "DownloadFile&Id" in u["href"]:
                            url = 'https://tesis.sld.cu/'+u["href"]+">"+url_id
                            namefile = os.path.basename(path)
                            size = os.path.getsize(path)/(1024 * 1024)
                            size = round(size, 2)
                            ##await msg.edit(f"✅ Nombre: "+namefile+"\n⤵️\n\n"+url)
                            await msg.delete()
                            with open(namefile+".txt","w") as f:
                                f.write(url)
                            await bot.send_document(username, namefile+".txt", thumb="logo.jpg", caption=f"**✅ Archivo Subido...\nNombre: {namefile}\nTamaño: {size} Mb\n**"+url)
                    except:pass
##################################################################
bot.start()
bot.send_message(5416296262,'**BoT Iniciado**')
print("Iniciado")
bot.loop.run_forever()
