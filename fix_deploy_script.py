import re
import subprocess

with open('deploy_ui16_highlevel_worker_portal.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the line 1934
bad_line = 'reply = "I understand you are asking: <em>\\"" + query + "\\"</em>. As Karthik Selvam (EMP-9021), your shift is active until 03:30 PM. All actions log directly to the Greater Chennai Corporation CIVIX core.";'
good_line = "reply = 'I understand you are asking: <em>' + query + '</em>. As Karthik Selvam (EMP-9021), your shift is active until 03:30 PM. All actions log directly to the Greater Chennai Corporation CIVIX core.';"

if bad_line in content:
    content = content.replace(bad_line, good_line)
    print("Replaced bad line in deploy script!")
else:
    print("bad_line not found exactly, searching by fragment...")
    frag = 'I understand you are asking: <em>'
    for line in content.splitlines():
        if frag in line:
            print("Found line:", line)
            content = content.replace(line, "        " + good_line)
            print("Replaced!")

with open('deploy_ui16_highlevel_worker_portal.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated deploy_ui16_highlevel_worker_portal.py.")
