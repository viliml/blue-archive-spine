import json
import os
from io import StringIO

import requests

from getModelsChina import downloadFile, getConfig

data = {}

# 1 for offline, 0 for online but cors issue
_type = 1

option = {
    "skipExisting": True
}

if not (os.path.isdir("./data")):
    os.mkdir("./data")

if __name__ == "__main__":
    config = getConfig()
    baseUrl = config["AddressablesCatalogUrlRoots"][0]
    manifestBaseUrl = baseUrl + "/Manifest/MediaResources/" + config["MediaVersion"]
    mediaBaseUrl = baseUrl + "/pool/MediaResources"
    resUrl = manifestBaseUrl + "/MediaManifest"
    # print(resUrl)
    # https://prod-clientpatch.bluearchiveyostar.com/r47_1_22_46zlzvd7mur326newgu8_2 + /MediaResources/MediaCatalog.json
    with StringIO(requests.get(resUrl).text) as f:
        keys = ["path", "crc", "kind", "size", "null"]
        res = [dict(zip(keys, line.strip().split(","))) for line in f]
    for asset in res:
        # print(asset)
        if asset["path"].startswith("audio/voc_") and "memoriallobby" in asset["path"]:
            lang = asset["path"].removeprefix("audio/voc_").split('/')[0]
            keyEvent = asset["path"].split("/")[-1] + "." + lang
            fname = keyEvent + ".ogg"
            url = mediaBaseUrl + "/" + asset["crc"][:2] + "/" + asset["crc"]

            # download ver
            if _type:
                path = f"./assets/audio/{fname}"
                print("="*30)
                print(fname)
                if os.path.isfile(path):
                    print("Already downloaded. Skipping.")
                    data[keyEvent] = path
                    continue
                if not (os.path.isdir("./assets/audio")):
                    os.mkdir("./assets/audio/")
                downloadFile(url, path)
                data[keyEvent] = path
            else:
                # online ver (cors ?)
                data[keyEvent] = url

    print(data)
    with open("./data/audio.json", "w") as f:
        json.dump(data, f, indent=4)
    print("="*30)
    print("Done!")
