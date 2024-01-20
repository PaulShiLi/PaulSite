from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent))

from pkgs.event import event
import asyncio
import importlib.util

evtLoop = asyncio.new_event_loop()

def setLoop():
    loops = []
    for data in os.walk(os.path.join(Path(__file__).resolve().parent, 'tasks'), topdown=False):
        dirName, subDir, files = data
        for filename in files:
            if filename.endswith(".py"):
                loops.append((filename[:-3], dirName))
    
    for loop in loops:
        modName, modDir = loop
        moduleSpec = importlib.util.spec_from_file_location(modName, os.path.join(modDir, f"{modName}.py"))
        module = importlib.util.module_from_spec(moduleSpec)
        moduleSpec.loader.exec_module(module)
        
        evtLoop.create_task(
            module.run()
        )
        event.post(
            toPrint= f"{loop[0].title()} loop started",
            evtType= "loop",
            filePath= os.path.join(modDir, f"{modName}.py")
        )
        
setLoop()
evtLoop.run_forever()