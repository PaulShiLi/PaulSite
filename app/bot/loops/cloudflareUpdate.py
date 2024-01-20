from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from resource.info import PATH, ENV
from pkgs.event import event
from pkgs.wrappers.discordWrapper import Console
from app.bot.scripts import embed

from nextcord.ext import commands
from textwrap import dedent
import asyncio
import aiohttp
import json

# Check every 1 minute
async def delay():
    await asyncio.sleep(60)

class handler:
    
    async def validateHostIP(client: commands.Bot ):
        console = Console(commands.Bot)
        
        services = {
            "httpbin.org": {
                "url": "http://httpbin.org/ip",
                "key": "origin"
            },
            "ipify.org": {
                "url": "https://api.ipify.org?format=json",
                "key": "ip"
            },
            "ip-api.com": {
                "url": "http://ip-api.com/json",
                "key": "query"
            },
            "ipinfo.io": {
                "url": "https://ipinfo.io/json",
                "key": "ip"
            },
            "jsonip.com": {
                "url": "https://jsonip.com",
                "key": "ip"
            }
        }
        errors = []
        
        serviceKeys = list(services.keys())
        ip = None
        # Make a request to httpbin.org and get the IP address
        for service in serviceKeys:
            async with aiohttp.ClientSession() as session:
                # Iterate through the services and stop if one of them works
                async with session.get(services[service]["url"]) as resp:
                    if resp.status == 200:
                        ip = (await resp.json())[services[service]["key"]]
                        break
                    else:
                        errors.append(resp)
        if ip == None:
            errors = "\n".join(errors)
            event.post(
                toPrint=f"Failed to get IP address",
                evtType="error",
                filePath=__file__
            )
            await console.error(
                dedent(
                    f"""
                    File: {__file__}
                    
                    Reason:
                    Failed to retrieve Host Public IP address
                    
                    Log:
                    ```json
                    {errors}
                    ```
                    """
                ),
                title="Failed to get IP address"
            )
            return False
        else:
            oldIP = None
            recordID = None
            async with aiohttp.ClientSession() as session:
                # Get existing IP address on cloudflare
                async with session.get(f"https://api.cloudflare.com/client/v4/zones/{ENV['cloudflare']['zone_identifier']}/dns_records?type=A&name={ENV['cloudflare']['record_name']}", headers={
                    "X-Auth-Email": ENV['cloudflare']['auth_email'],
                    f"{'X-Auth-Key' if ENV['cloudflare']['auth_method'] == 'global' else 'Authorization'}": f"{ENV['cloudflare']['auth_key'] if ENV['cloudflare']['auth_method'] == 'global' else 'Bearer ' + ENV['cloudflare']['auth_key']}",
                    "Content-Type": "application/json"
                }) as resp:
                    res = await resp.json()
                    if resp.status == 200:
                        oldIP = res["result"][0]["content"]
                    else:
                        event.post(
                            toPrint=f"Failed to update IP Address on Cloudflare",
                            evtType="error",
                            filePath=__file__
                        )
                        await console.error(
                            dedent(
                                f"""
                                File: {__file__}
                                
                                Reason:
                                IP Address update failed on Cloudflare
                                
                                Log:
                                ```md
                                {res}
                                ```
                                """
                            ),
                            title="Cloudflare IP Address Update Failed"
                        )
            if oldIP != ip:
                async with aiohttp.ClientSession() as session:
                    session.headers.update({
                        "X-Auth-Email": ENV['cloudflare']['auth_email'],
                        f"{'X-Auth-Key' if ENV['cloudflare']['auth_method'] == 'global' else 'Authorization'}": f"{ENV['cloudflare']['auth_key'] if ENV['cloudflare']['auth_method'] == 'global' else 'Bearer ' + ENV['cloudflare']['auth_key']}",
                        "Content-Type": "application/json"
                    })
                    async with session.patch(
                        f"https://api.cloudflare.com/client/v4/zones/{ENV['cloudflare']['zone_identifier']}/dns_records/{recordID}",
                        json={
                            "type": "A",
                            "name": ENV['cloudflare']['record_name'],
                            "content": ip,
                            "ttl": ENV['cloudflare']['ttl'],
                            "proxied": ENV['cloudflare']['proxy']
                        }
                    ):
                        res = await resp.json()
                event.post(
                    toPrint=f"IP Address changed from {oldIP} to {ip}",
                    evtType="info",
                    filePath=__file__
                )
                await console.alert(
                    dedent(
                        f"""
                        IP changed from {oldIP} to {ip}
                        Please update your login credentials for any remote connections!
                        """
                    ),
                    title="Host IP Change Detected",
                )
            else:
                event.post(
                    toPrint=f"IP Address is still {ip}",
                    evtType="info",
                    filePath=__file__
                )

async def run(client: commands.Bot):
    while True:
        await delay()
        await handler.validateHostIP(client)

asyncio.run(handler.validateHostIP())