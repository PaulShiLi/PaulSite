from pathlib import Path
import os
import sys
sys.path.insert(1, os.path.join(Path(__file__).resolve().parent.parent.parent.parent))

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
from paul_site_app.scripts import markup2html, fileManager
from resource.info import site
# Import datetime for unix epoch conversion
from datetime import datetime

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = {
        "tools": [
            {
                "name": "Linux Cheatsheet",
                "html": markup2html.convert(os.path.join(site.FILES, "Linux_Cheat_sheet.md"), "Linux Cheatsheet"),
                "desc": "A cheatsheet for Linux commands",
                "id": "linux-cheatsheet",
                "icon": """<i class="fab fa-linux d-flex justify-content-center icon heading" style="font-size: 28px;color: #e6b303;"></i>"""
            },
            {
                "name": "Base 64 Encoder/Decoder",
                "html": """
                <div class="card cardColor cardSpace box-3 appendSectionSpace" style="width: 100%;margin-right: 0px;margin-left: 0px;min-width=400px;">
                    <div class="card-body">
                        <div class="container d-flex flex-row justify-content-center align-items-start btn-group btn-group-toggle" id="b64_Form" data-bs-toggle="buttons" style="background: #ffffff;padding-right: 0px;padding-left: 0px;margin-bottom: 10px;"><label class="form-label btn btn-outline-primary active" id="encodeButton_b64" style="margin-bottom: 0px;">Encode<input type="radio" id="decode_b64" name="b64_Form" style="visibility:hidden;" onclick="encodeToggle(&#39;b64&#39;)"></label><label class="form-label btn btn-outline-primary" id="decodeButton_b64" style="margin-bottom: 0px;">Decode<input type="radio" id="encode_b64" class="" style="visibility:hidden;" name="b64_Form" onclick="decodeToggle(&#39;b64&#39;)"></label></div><textarea id="input_b64" oninput="auto_grow(this)" style="width: 100%;border-radius: 10px;color:#000000;"></textarea>
                        <div class="d-flex justify-content-center" style="width: 100%;"><button id="submit_b64" class="offset" onclick="submitToggle('b64')">Submit</button></div>
                    </div>
                </div>
                <div class="card cardColor cardSpace box-3 appendSectionSpace" id="result_b64" style="width: 100%;margin-right: 0px;margin-left: 0px;" hidden="">
                    <div class="card-body">
                        <h3 class="text-center heading text-xl">Your Result:</h3>
                        <p class="text-center text" id="resultContent_b64" style="margin-top: 10px; text-wrap: initial; max-width: 90vw;">None</p>
                        <div class="flex justify-center" style="padding-top:10px;">
                            <button id="submit_b64" class="offset" onclick="copy('b64')">Copy Result</button>
                        </div>
                        
                    </div>
                </div>
                """,
                "desc": "An encoder and decoder for Base 64 encoding",
                "id": "b64",
                "icon": """<i class="la la-codepen d-flex justify-content-center icon heading" style="font-size: 28px;color: #abe603;"></i>"""
            }
        ]
    }
    return HttpResponse(template.render(context, request))

def notFound_404(request):
    return render(request, '404.html')

def fileskudasai(request):
    template = loader.get_template('files_kudasai.html')
    context = fileManager.structure()
    return HttpResponse(template.render(context, request))
