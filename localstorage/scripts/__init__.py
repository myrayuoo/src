import os
from colorama import Fore as c
import json
import requests
import sys

#CONFIGURATION-------------
primary = c.LIGHTBLUE_EX
secondary = c.LIGHTWHITE_EX
version = "1.1-BlueMod"

base_name = "Xello.Blue"
font = "slant"
debug = True
#--------------------------


class script:
    def __init__(self):
        self.index = 0
        self.path = ""
        self.display = ""
        self.code = ""
        self.update_url = ""


def get_packages(script):
    try:
        data = json.loads(open(f"localstorage/scripts/scripts/{script.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    except FileNotFoundError: raise Exception(f"Unable to load packages for {script}, {script.replace('.py', '')}.meta.json is missing")
    except Exception as err: raise UserWarning(f"Caught an unknown error ({err})") 
    
    packages = ""
    
    for p in data["packages"]:
        try:
            c = open(f"localstorage/scripts/packages/{p}.pack.py", "r", encoding="utf-8").read()
        except FileNotFoundError: raise UserWarning(f"Package '{p}.pack.py' was not found")
        except Exception as err: raise UserWarning(f"Caught an unknown error ({err})") 

        packages += c+"\n"
    return packages


def validate_script(name):
    try:
        data = json.loads(open(f"localstorage/scripts/scripts/{name.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    except:
        return False
    
    for var in ["packages", "update_url", "display_name"]:
        try: data[var]
        except: return False
    return True
    
def load_scripts():
    scripts = []
    i = 0
    for x in os.listdir("localstorage/scripts/scripts"):
        if validate_script(x):
            packages = get_packages(x)
            if packages == None: packages = ""
            meta = get_script_meta(x)
            
            i +=1
            s = script()
            s.index = i
            s.path = "localstorage/scripts/scripts/"+x
            s.display = meta["display_name"]
            s.code = packages+"\n"+open(f"localstorage/scripts/scripts/{x}", "r", encoding="utf-8").read()
            s.update_url = meta["update_url"]
            scripts.append(s)
            
        elif debug and x.endswith(".py"):
            print(f"[WARN] Failed to load '{x}' - meta data is missing or is corrupted")
            
    return scripts

def get_script_meta(na):
    if validate_script(na):
        return json.loads(open(f"localstorage/scripts/scripts/{na.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    else:
        return {
    "packages": [""],
    "update_url": "https://github.com/xellu/scriptbase/wiki/Meta-data-&-configs#script-meta-data",
    "display_name": "Invalid meta data" 
}

def get_script(na):
    for x in load_scripts():
        if x.display == na:
            return x
        
def is_script_index(n: int):
    try: int(n)
    except: return False
    
    if len(load_scripts()) >= int(n):
        return True
    return False

def update_scripts():
    for s in load_scripts():
        if s.update_url != "":
            r = requests.get(s.update_url)
            if r.status_code in [200, 201, 202]:
                if r.content != s.code:
                    open(s.path, "wb").write(r.content)
                    print(f" {primary}[i] {secondary}Updated {s.display}")


def get_config():
    return json.loads(open("localstorage/scripts/config.json", "r").read())



def process_builtin_commands(s):
    if get_config()["allow_integrated_commands"] == False: return
    if s in ["commands", "help"]:
        print(f"""
   {primary}[i] {secondary}Command list
    {primary}|  Help{secondary} Shows the command list
    {primary}|  Scripts{secondary} List of scripts
    {primary}|  Version{secondary} Shows the version of scriptbase

              """)
        return True
    
    if s in ["scripts", "list"]:
        for s in load_scripts():
            print(f"{primary}[{s.index}] {secondary}{s.display}")
    
    if s in ["version"]:
        print(f"{primary}Running ScriptBase v{version}")
        
        
def run(selection):
    scripts = load_scripts()
    script = get_script(selection)

    if not process_builtin_commands(selection):
        
        if script != None:
            exec(script.code)
        if is_script_index(selection):
            for x in scripts:
                if x.display.lower() == selection.lower() or x.index == int(selection):
                    exec(x.code)