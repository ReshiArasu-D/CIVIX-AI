import re
import deploy_ui16_highlevel_worker_portal as m

with open('deploy_ui16_highlevel_worker_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove the dynamic record button from the sidebar
sidebar_btn_pattern = r'<!-- 3\. Active Job Record -->\s*<button type="button" class="sidebar-nav-link".*?</button>'
if re.search(sidebar_btn_pattern, code, re.DOTALL):
    code = re.sub(sidebar_btn_pattern, '<!-- Active Job Record removed from sidebar to keep nav clean -->', code, flags=re.DOTALL)
    print("Removed dynamic Active Job Record from sidebar!")
else:
    print("Sidebar button pattern not found directly, checking manual replacement...")

# Also update the active state on Assigned Work Orders button
old_nav_jobs = 'class="sidebar-nav-link" ng-class="{\'active\': c.currentTab === \'jobs\'}"'
new_nav_jobs = 'class="sidebar-nav-link" ng-class="{\'active\': c.currentTab === \'jobs\' || c.currentTab === \'detail\'}"'
# Note f-string double braces:
old_nav_jobs_f = "class=\"sidebar-nav-link\" ng-class=\"{{'active': c.currentTab === 'jobs'}}\""
new_nav_jobs_f = "class=\"sidebar-nav-link\" ng-class=\"{{'active': c.currentTab === 'jobs' || c.currentTab === 'detail'}}\""
if old_nav_jobs_f in code:
    code = code.replace(old_nav_jobs_f, new_nav_jobs_f)
    print("Updated Assigned Work Orders nav active class for detail view!")

# 2. Update the Back button in detail view to go back cleanly
old_back = '&larr; Back to Dashboard'
new_back = '&larr; Back to Work Orders'
if old_back in code:
    code = code.replace(old_back, new_back)
    print("Updated Back button text!")

old_back_click = "ng-click=\"c.setTab('dashboard')\""
new_back_click = "ng-click=\"c.setTab(c.prevTab || 'jobs')\""
if old_back_click in code:
    code = code.replace(old_back_click, new_back_click, 1) # only in record header
    print("Updated Back button ng-click!")

# 3. Update breadcrumbs in top header
old_crumbs = """        <span class="crumb-current" ng-if="c.currentTab === 'detail'">Work Order &bull; {{{{c.selectedWo.u_number}}}}</span>"""
new_crumbs = """        <span class="crumb-link" ng-if="c.currentTab === 'detail'" ng-click="c.setTab('jobs')">Assigned Work Orders</span>
        <span class="crumb-arrow" ng-if="c.currentTab === 'detail'">/</span>
        <span class="crumb-current font-mono" ng-if="c.currentTab === 'detail'">{{{{c.selectedWo.u_number}}}}</span>"""
if old_crumbs in code:
    code = code.replace(old_crumbs, new_crumbs)
    print("Updated breadcrumbs for detail view!")

# 4. In client script, set c.prevTab when selecting job
old_select_job = """  c.selectJob = function(wo) {
    c.selectedWo = wo;
    c.currentTab = 'detail';"""
new_select_job = """  c.selectJob = function(wo) {
    c.prevTab = c.currentTab;
    c.selectedWo = wo;
    c.currentTab = 'detail';"""
if old_select_job in code:
    code = code.replace(old_select_job, new_select_job)
    print("Updated selectJob to track prevTab!")

with open('deploy_ui16_highlevel_worker_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated deploy_ui16_highlevel_worker_portal.py!")
