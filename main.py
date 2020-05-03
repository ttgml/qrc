from fastapi import FastAPI,Body, HTTPException, Header, File, UploadFile, Response
from fastapi.responses import FileResponse
from datetime import time,datetime,timedelta
from pydantic import BaseModel
from uuid import UUID,uuid4
import qrcode_terminal
import redis
from typing import List
from configparser import ConfigParser
from pathlib import Path
import hashlib

config = ConfigParser()
config.read('setting.cfg')

app = FastAPI()
redis = redis.Redis(host=config.get("redis","host"),port=config.getint("redis","port"))
upload_path = Path(config.get("base","upload_path"))

def out_md5(src):
    m = hashlib.md5()
    m.update(src)
    return m.hexdigest()

@app.post("/")
async def post_file( user_agent: str = Header(None), file: UploadFile = File(None)):
    if "curl" in user_agent:
        if file != None:
            fuid = str(uuid4()).split("-")[0]
            print(type(file.file))
            file_content = await file.read()
            with open(upload_path.joinpath(fuid), "wb") as f:
                f.write(file_content)
            md5_str = out_md5(file_content)
            redis.set(fuid,file.filename)
            furl = config.get('base','url') + fuid + "/info"
            qr = qrcode_terminal.qr_terminal_str(furl)
            return Response(
                qr + "\n- - - - - -\n"
                + "File Name: " + file.filename + "\n"
                + "File Info URL: " + furl+ "\n"
                + "md5: " + md5_str + "\n"
                + "- - - - - -\n")
        return {"msg":"ohh my god"}
    else:
        return {"are you ok"}

@app.get("/")
async def get_root( user_agent: str = Header(None)):
    return {
        "Hello": "World!",
        "msg": {
            "/help": "display this help",
            "/version": "output version information",
            "/debug": "echo some info",
            "/": "curl -F 'file=@demo.py' " + config.get('base','url')
        }
    }

@app.get("/debug")
def echo_ua(user_agent: str = Header("unknown")):
    return {"ua":user_agent} 

@app.get("/version")
def echo_version():
    return {"version":"0.1"}

@app.get('/{fuid}/info')
def get_info_by_uuid(fuid: str = None):
    p = upload_path.joinpath(fuid)
    if (not p.exists()) or (not redis.exists(fuid)):
        raise HTTPException(404)
    with open(upload_path.joinpath(fuid),"rb") as f:
        md5_str = out_md5(f.read())
    return {
        'UID':fuid,
        'File Name': redis.get(fuid).decode('utf-8'),
        'File Size': str(int(p.stat().st_size)/1024) + " kb",
        'MD5': md5_str,
        'Download URL': config.get('base','url') + fuid + "/down"
        }

@app.get('/{fuid}/down')
def download_file_by_uuid(fuid: str = None):
    p = upload_path.joinpath(fuid)
    print(p)
    if (not p.exists()) or (not redis.exists(fuid)):
        raise HTTPException(404)
    file_name = redis.get(fuid)
    return FileResponse(p.resolve(),media_type='text/plain', filename=file_name)

@app.get('/{fuid}/del')
def del_file_by_uuid(fuid: str = None):
    p = upload_path.joinpath(fuid)
    if (not p.exists()) or (not redis.exists(fuid)):
        raise HTTPException(404)
    p.unlink(missing_ok=True)
    redis.delete(fuid)
    return {"msg":"delete success"}