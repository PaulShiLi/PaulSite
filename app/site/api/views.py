from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))
from resource.info import PATH, ENV

from rest_framework.request import Request
# import local data
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import renderer_classes
from django.http.response import JsonResponse

from adrf.decorators import api_view

from datetime import datetime
import json
import aiofiles
import asyncio

def getKey(key):
    if type(key) == int:
        return f"{key}"
    else:
        return f"'{key}'"

class API:
    
    class fetch:
        async def json(path: str) -> dict:
            while True:
                try:
                    async with aiofiles.open(path, mode="r") as f:
                        return json.loads(await f.read())
                except json.decoder.JSONDecodeError:
                    await asyncio.sleep(0.1)
    
    class write:
        async def json(path: str, body: dict, keys: list = None, keyOverride: bool = False) -> dict:
            """Write dictionary to a json file
            Pass param like this:\n
            payload = {
                "content": {
                    "list": [
                        {"el": 0},
                        "1"
                    ]
                },
                "auth": {
                    "username": "sub01",
                    "passwd": "P0704++--."
                }
            }
            print(API.write.json(PATH.API.SPOTIFY.STATUS, payload, keys=["status", "childList", 2], keyOverride=True))
            
            Args:
                path (str): Path to json file
                body (dict): Response Body
                keys (list | None, optional): Keys to update in json file of arg path. Defaults to None.
                keyOverride (bool, optional): Create new keys if key nonexistent. Defaults to False.

            Returns:
                dict: Dictionary status of result with status code
            """
            try:
                content = body["content"]
                passwd = body["auth"]["passwd"]
                username = body["auth"]["username"]
            except KeyError:
                return {
                    "error": "Invalid Dictionary Format!",
                    "resp": "Dictionary must contain 'content' and 'auth' keys!",
                    "status": 500
                }
            if passwd != ENV["django"]["api"]["passwd"] or ENV["django"]["api"]["username"] != username:
                return {
                    "error": "Invalid Credentials!",
                    "resp": "Invalid Username or Password!",
                    "status": 401
                }
            toEval = None
            # Check if keys are all the same as original dict
            while True:
                try:
                    async with aiofiles.open(path, mode="r") as f:
                        original = json.loads(await f.read())
                    break
                except json.decoder.JSONDecodeError:
                    await asyncio.sleep(0.1)
            if keys != None:
                toEval = "original"
                for key in keys:
                    toEval += f"[{getKey(key)}]"
                try:
                    eval(f"{toEval}.update({content})")
                except AttributeError:
                    exec(f"{toEval} = {content}")
                except KeyError and IndexError:
                    toEval = "original"
                    prevKey = "original"
                    for i in range(len(keys)):
                        key = keys[i]
                        if (len(keys) - 1) != i:
                            toEval += f"[{getKey(key)}]"
                        try:
                            eval(toEval)
                        except KeyError:
                            if not keyOverride:
                                return {
                                    "error": "Invalid Dictionary Format!",
                                    "resp": f"Key {key} does not exist!",
                                    "status": 500
                                }
                            elif ((len(keys) - 1) != i):
                                eval(f"{prevKey}.update(" + "{" + f"{getKey(key)}: " + "{}})")
                        if (len(keys) - 1) != i:
                            prevKey += f"[{getKey(key)}]"
                            # print(f"[{getKey(key)}]")
                        else:
                            try:
                                eval(f"{toEval}.update(" + "{" + f"{getKey(key)}:{content}" + "})")
                            except AttributeError:
                                try:
                                    exec(f"{toEval}[{getKey(key)}] = {content}")
                                except IndexError:
                                    for i in range(key+1):
                                        try:
                                            eval(f"{toEval}[{i}]")
                                        except IndexError:
                                            eval(f"{toEval}.append(None)")
                                    exec(f"{toEval}[{getKey(key)}] = {content}")
            if toEval == None:
                if original.keys() != content.keys() and keyOverride == False:
                    return {
                        "error": "Invalid Dictionary Format!",
                        "resp": f"Keys do not match! Expected {original.keys()}",
                        "status": 500
                    }
            else:
                if eval(toEval).keys() != content.keys() and keyOverride == False:
                    # print(eval(toEval))
                    return {
                        "error": "Invalid Dictionary Format!",
                        "resp": f"Keys do not match! Expected {eval(toEval).keys()}",
                        "status": 500
                    }
            # Check if username and password are correct
            async with aiofiles.open(path, mode="w") as f:
                await f.write(json.dumps(original, indent=4))
                return {
                    "resp": "Success",
                    "status": 200
                }

class site:
    @renderer_classes((JSONRenderer))
    @api_view(['GET', 'POST'])
    async def base(request: Request):
        if request.method == "GET":
            return JsonResponse(await API.fetch.json(PATH.API.api), safe=False)
        elif request.method == "POST":
            api_data = request.data
            return JsonResponse(await API.write.json(PATH.API.api, api_data), safe=False)

class discord:
    @renderer_classes((JSONRenderer))
    @api_view(['GET', 'POST'])
    async def base(request: Request):
        if request.method == "GET":
            payload = await API.fetch.json(PATH.API.api)
            return JsonResponse(payload["discord"], safe=False)
        elif request.method == "POST":
            api_data = request.data
            return JsonResponse(await API.write.json(PATH.API.api, api_data, keys=["discord"]), safe=False)
    
    @renderer_classes((JSONRenderer))
    @api_view(['GET', 'POST'])
    async def status(request: Request):
        if request.method == "GET":
            payload = await API.fetch.json(PATH.API.DISCORD.STATUS)
            return JsonResponse(payload, safe=False)
        elif request.method == "POST":
            api_data = request.data
            return JsonResponse(await API.write.json(PATH.API.api, api_data, keys=["discord", "status"]), safe=False)

class spotify:
    @renderer_classes((JSONRenderer))
    @api_view(['GET', 'POST'])
    async def base(request: Request):
        if request.method == "GET":
            payload = await API.fetch.json(PATH.API.api)
            return JsonResponse(payload["spotify"], safe=False)
        elif request.method == "POST":
            api_data = request.data
            return JsonResponse(await API.write.json(PATH.API.api, api_data, keys=["spotify"]), safe=False)
        
    @renderer_classes((JSONRenderer))
    @api_view(['GET', 'POST'])
    async def status(request: Request):
        if request.method == "GET":
            payload = await API.fetch.json(PATH.API.SPOTIFY.STATUS)
            return JsonResponse(payload, safe=False)
        elif request.method == "POST":
            api_data = request.data
            return JsonResponse(await API.write.json(PATH.API.api, api_data, keys=["spotify", "status"]), safe=False)
    
    @renderer_classes((JSONRenderer))
    @api_view(['GET', 'POST'])
    async def history(request: Request):
        if request.method == "GET":
            payload = await API.fetch.json(PATH.API.SPOTIFY.HISTORY)
            return JsonResponse(payload, safe=False)
        elif request.method == "POST":
            api_data = request.data
            return JsonResponse(await API.write.json(PATH.API.api, api_data, keys=["spotify", "history"]), safe=False)
    