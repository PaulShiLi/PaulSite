import markdown as mkd
import os


def convert(markdownPath: str, name: str):
    with open(markdownPath, "r") as f:
        markdownFile = f.read()
    return mkd.markdown(markdownFile, extensions=[
        'markdown.extensions.tables',
        'nl2br',
        'sane_lists'
    ])