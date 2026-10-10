import os, requests
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SERVICENOW_INSTANCE_URL', '').rstrip('/')
u = os.getenv('SERVICENOW_USERNAME')
p = os.getenv('SERVICENOW_PASSWORD')
s = requests.Session()
s.auth = (u, p)

# 1. Check civix_home page
page = s.get(f"{url}/api/now/table/sp_page?sysparm_query=id=civix_home").json()['result'][0]
print("Page id:", page['id'], "sys_id:", page['sys_id'], "css:", page.get('css'))

# 2. Check sp_container
conts = s.get(f"{url}/api/now/table/sp_container?sysparm_query=sp_page={page['sys_id']}").json()['result']
for c in conts:
    print("Container:", c['sys_id'], "bootstrap_alt:", c.get('bootstrap_alt'))

# 3. Check portal theme
portal = s.get(f"{url}/api/now/table/sp_portal?sysparm_query=url_suffix=civix").json()['result'][0]
theme_id = portal.get('theme')
theme = s.get(f"{url}/api/now/table/sp_theme/{theme_id}").json()['result']
print("Theme name:", theme.get('name'))
print("Theme CSS Variables:\n", theme.get('css_variables'))
