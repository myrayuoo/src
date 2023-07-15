removed = 0
for i in invites:
    if i["usedBy"] in [None, ""]:
        invites.remove(i)
        removed += 1
        
print(f"Removed {removed} unused invites")