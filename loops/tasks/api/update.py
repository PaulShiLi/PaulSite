from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

import asyncio
import json
from resource.info import PATH, site
from pkgs.event import event
import aiofiles

# Update every 1 seconds
async def delay():
    targetSeconds = 1
    await asyncio.sleep(targetSeconds)

class handler:
    
    async def update():
        while True:
            try:
                async with aiofiles.open(PATH.API.api, mode='r') as f:
                    api = json.loads(await f.read())
                break
            except json.decoder.JSONDecodeError:
                continue
        
        for key in api.keys():
            for key2 in api[key].keys():
                try:
                    async with aiofiles.open(os.path.join(site.STATIC, "api", key, key2 + ".json"), mode='r') as f:
                        loadData = json.loads(await f.read())
                    if loadData != api[key][key2]:
                        async with aiofiles.open(os.path.join(site.STATIC, "api", key, key2 + ".json"), mode='w') as f:
                            await f.write(json.dumps(api[key][key2], indent=4))
                        event.post(
                            toPrint= "Json API files updated",
                            evtType= "loop",
                            filePath= __file__
                        )
                except Exception as e:
                    try:
                        async with aiofiles.open(os.path.join(site.STATIC, "api", key, key2 + ".json"), mode='w') as f:
                            await f.write(json.dumps(api[key][key2], indent=4))
                        event.post(
                            toPrint= "Json API files updated",
                            evtType= "loop",
                            filePath= __file__
                        )
                    except Exception as e:
                        event.post(
                            toPrint= f"Error updating {key} {key2} json file\nError: {e}",
                            evtType= "error",
                            filePath= __file__
                        )
        
        del api

async def run():
    while True:
        await handler.update()
        await delay()