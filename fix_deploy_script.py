import re

with open("d:/tcs/deploy_all_pages_redesign.py", "r", encoding="utf-8") as f:
    content = f.read()

# Fix REPORT_TEMPLATE
old_report_start = '''REPORT_TEMPLATE = f"""
<div class="civix-app-shell">
  {get_sidebar_html("report")}

  <main class="civix-main-column">
    {get_topbar_html()}'''

new_report_start = '''REPORT_TEMPLATE = """
<div class="civix-app-shell">
  __SIDEBAR_REPORT__

  <main class="civix-main-column">
    __TOPBAR__'''

if old_report_start in content:
    content = content.replace(old_report_start, new_report_start, 1)
    content = content.replace('REPORT_CSS = BASE_SHELL_CSS', 'REPORT_TEMPLATE = REPORT_TEMPLATE.replace("__SIDEBAR_REPORT__", get_sidebar_html("report")).replace("__TOPBAR__", get_topbar_html())\n\nREPORT_CSS = BASE_SHELL_CSS', 1)
    print("Fixed REPORT_TEMPLATE")
else:
    print("Warning: old_report_start not found directly")

# Fix CASES_TEMPLATE
old_cases_start = '''CASES_TEMPLATE = f"""
<div class="civix-app-shell">
  {get_sidebar_html("complaints")}

  <main class="civix-main-column">
    {get_topbar_html()}'''

new_cases_start = '''CASES_TEMPLATE = """
<div class="civix-app-shell">
  __SIDEBAR_CASES__

  <main class="civix-main-column">
    __TOPBAR__'''

if old_cases_start in content:
    content = content.replace(old_cases_start, new_cases_start, 1)
    content = content.replace('CASES_CSS = BASE_SHELL_CSS', 'CASES_TEMPLATE = CASES_TEMPLATE.replace("__SIDEBAR_CASES__", get_sidebar_html("complaints")).replace("__TOPBAR__", get_topbar_html())\n\nCASES_CSS = BASE_SHELL_CSS', 1)
    print("Fixed CASES_TEMPLATE")
else:
    print("Warning: old_cases_start not found directly")

# Fix TRACK_TEMPLATE
old_track_start = '''TRACK_TEMPLATE = f"""
<div class="civix-app-shell">
  {get_sidebar_html("complaints")}

  <main class="civix-main-column">
    {get_topbar_html()}'''

new_track_start = '''TRACK_TEMPLATE = """
<div class="civix-app-shell">
  __SIDEBAR_TRACK__

  <main class="civix-main-column">
    __TOPBAR__'''

if old_track_start in content:
    content = content.replace(old_track_start, new_track_start, 1)
    content = content.replace('TRACK_CSS = BASE_SHELL_CSS', 'TRACK_TEMPLATE = TRACK_TEMPLATE.replace("__SIDEBAR_TRACK__", get_sidebar_html("complaints")).replace("__TOPBAR__", get_topbar_html())\n\nTRACK_CSS = BASE_SHELL_CSS', 1)
    print("Fixed TRACK_TEMPLATE")
else:
    print("Warning: old_track_start not found directly")

with open("d:/tcs/deploy_all_pages_redesign.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Finished fixing deploy_all_pages_redesign.py")
