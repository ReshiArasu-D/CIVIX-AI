import re

with open('deploy_ui16_highlevel_worker_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update template bindings for Close Tracker modal
old_backdrop = '<div class="fsm-modal-backdrop" ng-if="c.showCaseTrackingModal" ng-click="c.closeCaseTrackingModal($event)">'
new_backdrop = '<div class="fsm-modal-backdrop" ng-if="c.showCaseTrackingModal" ng-click="c.showCaseTrackingModal = false; c.closeCaseTrackingModal($event)">'
if old_backdrop in code:
    code = code.replace(old_backdrop, new_backdrop)
    print("Updated modal backdrop ng-click!")

old_x_btn = '<button type="button" class="fsm-modal-close-btn" ng-click="c.closeCaseTrackingModal($event)" title="Close">&times;</button>'
new_x_btn = '<button type="button" class="fsm-modal-close-btn" id="btnXCloseCaseTracker" ng-click="c.showCaseTrackingModal = false; c.closeCaseTrackingModal($event)" title="Close">&times;</button>'
if old_x_btn in code:
    code = code.replace(old_x_btn, new_x_btn)
    print("Updated X close button ng-click!")

old_close_btn = '<button type="button" class="btn btn-default" ng-click="c.closeCaseTrackingModal($event)">Close Tracker</button>'
new_close_btn = '<button type="button" class="btn btn-default" id="btnCloseCaseTracker" ng-click="c.showCaseTrackingModal = false; c.closeCaseTrackingModal($event)">Close Tracker</button>'
if old_close_btn in code:
    code = code.replace(old_close_btn, new_close_btn)
    print("Updated Close Tracker button ng-click!")

# 2. Update client script closeCaseTrackingModal implementation
old_client_fn = """  c.closeCaseTrackingModal = function(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    c.showCaseTrackingModal = false;
  };"""

new_client_fn = """  $scope.closeCaseTrackingModal = c.closeCaseTrackingModal = function(e) {
    if (e && e.preventDefault) e.preventDefault();
    if (e && e.stopPropagation) e.stopPropagation();
    c.showCaseTrackingModal = false;
    $scope.showCaseTrackingModal = false;
    $timeout(function() {
      c.showCaseTrackingModal = false;
      $scope.showCaseTrackingModal = false;
      try { if (!$scope.$$phase) $scope.$apply(); } catch(err) {}
    }, 0);
  };"""

if old_client_fn in code:
    code = code.replace(old_client_fn, new_client_fn)
    print("Updated closeCaseTrackingModal function in client script!")
else:
    print("Warning: old_client_fn not found exactly, searching by pattern...")
    frag = "c.closeCaseTrackingModal = function(e)"
    for line in code.splitlines():
        if frag in line:
            print("Found line:", line)

with open('deploy_ui16_highlevel_worker_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated deploy_ui16_highlevel_worker_portal.py!")
