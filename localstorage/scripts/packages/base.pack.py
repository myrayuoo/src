import os

def get_input(text):
    return input(f" {primary}[>] {secondary}{text}: ")
    
def get_int_input(text, fail_msg="Please enter a valid integer"):
    while True:
        a = input(f" {primary}[>] {secondary}{text}: ")
        try: int(a)
        except: print("Error:"+str(fail_msg))
        else: return int(a)

def cls():
    os.system("cls")
    os.system("clear")