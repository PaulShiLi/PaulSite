from pathlib import Path
import os
import sys

sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent))

from app.bot.scripts import embed, fileManager
from resource.info import site, ENV, PATH

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import asyncio
import aiofiles
import aiohttp
import shutil
from requests.utils import requote_uri
from textwrap import dedent
from datetime import datetime
import filetype


def limiter(fileName: str, relPath: str, marginalError: int = 2, maxLen: int = 100):
    if "./" == relPath[:2]:
        relPath = relPath[2:]
    elif "/" == relPath[:0]:
        relPath = relPath[1:]
    totalLen = maxLen - marginalError
    if "." in fileName:
        ext = fileName.split(".")[-1]
        totalLen -= len(ext) + len(relPath + "/" if relPath != "" else "") + 1
        title = ".".join(fileName.split(".")[:-1])[:totalLen]
        return f"{relPath}{'/' if relPath != '' else ''}{title}.{ext}"
    else:
        totalLen -= len(relPath + "/" if relPath != "" else "")
        title = fileName[:totalLen]
        return f"{relPath}{'/' if relPath != '' else ''}{title}"


class interact(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command()
    async def api(self, interaction: Interaction):
        pass

    @api.subcommand(description="Retrieves the public IP address of the server")
    async def ip(self, interaction: Interaction, service: str = SlashOption(required=False, default="httpbin.org")):
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
        # Make a request to httpbin.org and get the IP address
        async with aiohttp.ClientSession() as session:
            async with session.get(services[service]["url"]) as resp:
                ip = (await resp.json())[services[service]["key"]]
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title="Public IP Address",
                description=dedent(
                    f"""
                    Site used to retrieve IP: {services[service]["url"]}
                    ```yaml\n{ip}```
                    """
                ),
                timestampFooter=True,
            ),
            ephemeral=True,
        )
    
    @ip.on_autocomplete("service")
    async def ip_auto(self, interaction: Interaction, service: str):
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
        if not service:
            await interaction.response.send_autocomplete(services.keys())
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in services.items()
                if key.startswith(service)
            }
        )

    @api.subcommand(description="Retrieves folder structure of files")
    async def filetree(
        self,
        interaction: Interaction,
        folder: str = SlashOption(
            name="folder",
            default="",
            description="Which folder would you want to see?",
        ),
    ):
        tree = "```yaml\n"
        paths = fileManager.DisplayablePath.make_tree(
            Path(os.path.join(site.FILES, folder))
        )
        for path in paths:
            tree += f"{path.displayable()}\n"
        tree += "```"
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title=f"File Tree of `./{folder.replace(PATH.PARENT_DIR, '')}`",
                description=tree,
                timestampFooter=True,
            ),
            ephemeral=True,
        )

    # Autocomplete for filetree
    @filetree.on_autocomplete("folder")
    async def filetree_auto(self, interaction: Interaction, folder: str):
        if not folder:
            await interaction.response.send_autocomplete(fileManager.folder())
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in fileManager.folder().items()
                if key.startswith(folder)
            }
        )

    @api.subcommand(description="Uploads a file to the website")
    async def upload(
        self,
        interaction: Interaction,
        file: nextcord.Attachment = SlashOption(required=True),
        custom_name: str = SlashOption(required=False, default=""),
        relpath: str = SlashOption(
            name="folder",
            default="",
            description="Which folder would you want to save to?",
        ),
    ):
        if custom_name == "":
            filename = file.filename
        else:
            filename = f"{custom_name}{'.' + file.filename.split('.')[-1] if '.' in file.filename else ''}"

        filePath = os.path.join(
            site.FILES,
            limiter(fileName=filename, relPath=relpath, marginalError=2, maxLen=100),
        )
        # print(
        #     f"{len(relpath)} RelPath: {relpath} |{len(filename)} Filename: {filename}"
        # )
        # print(
        #     len(
        #         limiter(fileName=filename, relPath=relpath, marginalError=2, maxLen=100)
        #     ),
        #     limiter(fileName=filename, relPath=relpath, marginalError=2, maxLen=100),
        # )
        async with aiohttp.ClientSession() as session:
            async with session.get(url=file.url) as resp:
                async with aiofiles.open(filePath, mode="wb") as f:
                    await f.write(await resp.read())
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title=f"`{filename}` saved",
                description=dedent(
                    f"""
                    Access your file @
                    {requote_uri(f"{ENV['site']['siteAddress']}{filePath.replace(PATH.PARENT_DIR, '')}")}
                    """
                ),
                footer=f"Requested by {interaction.user.name}",
            ),
            ephemeral=True,
        )

    # Autocomplete for upload
    @upload.on_autocomplete("relpath")
    async def upload_auto(self, interaction: Interaction, relPath: str):
        if not relPath:
            await interaction.response.send_autocomplete(fileManager.folder())
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in fileManager.folder().items()
                if key.startswith(relPath)
            }
        )

    @api.subcommand(description="Deletes a file from the website")
    async def delete(
        self,
        interaction: Interaction,
        filepath: str = SlashOption(
            name="file",
            description="Which file would you want to delete?",
            required=True,
        ),
    ):
        try:
            os.remove(os.path.join(site.FILES, filepath))
        except FileNotFoundError:
            os.remove(os.path.join(site.FILES, filepath[1:]))
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title=f"`{filepath.split(os.sep)[-1]}` deleted",
                description=dedent(
                    f"""
                    `{filepath.split(os.sep)[-1]}` has been deleted from `{os.sep.join(filepath.split(os.sep)[:-1]).replace(site.FILES, '') if '' != os.sep.join(filepath.split(os.sep)[:-1]).replace(site.FILES, '') else '.'}`
                    """
                ),
            ),
            ephemeral=True,
        )

    # Autocomplete for delete
    @delete.on_autocomplete("filepath")
    async def delete_auto(self, interaction: Interaction, filepath: str):
        if not filepath:
            await interaction.response.send_autocomplete(
                fileManager.structure(dictReturn=False, safe=True)
            )
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in fileManager.structure(dictReturn=False, safe=True).items()
                if key.startswith(filepath)
            }
        )

    @api.subcommand(description="Creates a folder to the website")
    async def mkdir(
        self,
        interaction: Interaction,
        name: str,
        folder: str = SlashOption(name="folder", default=site.FILES, description="Which folder would you want to create the folder in?"),
    ):
        os.mkdir(os.path.join(site.FILES, folder, name))
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title=f"`{name}` created",
                description=dedent(
                    f"""
                    Access your folder @ {requote_uri(f"{ENV['site']['siteAddress']}{(os.path.join(folder, name).replace(PATH.PARENT_DIR, '') if os.path.join(folder, name).replace(PATH.PARENT_DIR, '')[0] == '/' else '/' + os.path.join(folder, name).replace(PATH.PARENT_DIR, ''))}")}
                    """
                ),
            ),
            ephemeral=True,
        )

    # Autocomplete for mkdir
    @mkdir.on_autocomplete("folder")
    async def mkdir_auto(self, interaction: Interaction, folder: str):
        if not folder:
            await interaction.response.send_autocomplete(fileManager.folder())
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in fileManager.folder().items()
                if key.startswith(folder)
            }
        )

    @api.subcommand(description="Deletes a folder from the website")
    async def rmdir(
        self,
        interaction: Interaction,
        folder: str = SlashOption(
            name="folder",
            description="Which folder would you want to delete?",
            required=True,
        ),
    ):
        shutil.rmtree(os.path.join(site.FILES, folder), ignore_errors=True)
        await interaction.response.send_message(
            embed=embed.createEmbed(
                title=f"`{folder.split(os.sep)[-1]}` deleted",
                description=dedent(
                    f"""
                    Your folder has been deleted in: ```./{os.path.join(folder).replace(PATH.PARENT_DIR, '')}```
                    """
                ),
            ),
            ephemeral=True,
        )

    # Autocomplete for rmdir
    @rmdir.on_autocomplete("folder")
    async def rmdir_auto(self, interaction: Interaction, folder: str):
        if not folder:
            await interaction.response.send_autocomplete(
                fileManager.folder(ignoreBase=True)
            )
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in fileManager.folder(ignoreBase=True).items()
                if key.startswith(folder)
            }
        )

    @api.subcommand(description="Retrieves a file from the website")
    async def retrieve(
        self,
        interaction: Interaction,
        filepath: str = SlashOption(
            name="file",
            description="Which file would you want to retrieve?",
            required=True,
        ),
    ):
        path = (
            os.path.join(site.FILES, filepath)
            if os.path.isfile(os.path.join(site.FILES, filepath))
            else os.path.join(site.FILES, filepath[1:])
        )

        fileStat = os.stat(path)
        with open(path, "rb") as f:
            await interaction.response.send_message(
                embed=embed.createEmbed(
                    title=f"`{filepath.split(os.sep)[-1]}` retrieved",
                    description=dedent(
                        f"""
                        Access your file @ {requote_uri(f"{ENV['site']['siteAddress']}{path.replace(PATH.PARENT_DIR, '')}")}
                        
                        ```md
                        File Info:
                        
                        Size:   {f'{str(fileStat.st_size)} bytes' if (fileStat.st_size < 1024) else (f'{str(round(fileStat.st_size/1024, 2))} kilobytes' if (fileStat.st_size < 1024 ** 2) else (f'{str(round(fileStat.st_size/(1024**2), 2))} megabytes' if (fileStat.st_size < 1024 ** 3) else (f'{str(round(fileStat.st_size/(1024**3), 2))} gigabytes' if (fileStat.st_size < 1024 ** 4) else ("N/A"))))}
                        Creation Date:  {datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%m/%d/%Y')} @ {str(int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H')) - 12) if (int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H')) > 12) else (str(int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H'))))}:{datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%M:%S')} {'PM' if (int(datetime.utcfromtimestamp(int(fileStat.st_mtime)).strftime('%H')) > 12) else ('AM')}
                        ```
                        """
                    ),
                    image=requote_uri(
                        f"{ENV['site']['siteAddress']}{path.replace(PATH.PARENT_DIR, '')}"
                    )
                    if filetype.is_image(f)
                    else None
                ),
                ephemeral=True,
            )
            nextcordFile = nextcord.File(f)
            nextcordFile.filename = filepath.split(os.sep)[-1]
            await interaction.followup.send(
                file=nextcordFile,
                ephemeral=True
            ) if fileStat.st_size < 8388608 else await interaction.followup.send(
                requote_uri(
                    f"{ENV['site']['siteAddress']}{path.replace(PATH.PARENT_DIR, '')}"
                ),
                ephemeral=True
            )

    # Autocomplete for retrieve
    @retrieve.on_autocomplete("filepath")
    async def retrieve_auto(self, interaction: Interaction, filepath: str):
        if not filepath:
            await interaction.response.send_autocomplete(
                fileManager.structure(dictReturn=False)
            )
            return
        await interaction.response.send_autocomplete(
            {
                key: item
                for key, item in fileManager.structure(dictReturn=False).items()
                if key.startswith(filepath)
            }
        )


def setup(client):
    client.add_cog(interact(client))
