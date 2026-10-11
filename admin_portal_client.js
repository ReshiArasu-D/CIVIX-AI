api.controller = function($scope, $http, $window, spUtil) {
  var c = this;

  // Active module navigation (default: Operations Dashboard)
  c.currentTab = 'dashboard';
  c.ticketSubTab = 'all';
  c.caseSubTab = 'all';
  c.iotSubTab = 'overview';
  c.assetSubTab = 'assets';
  c.zoneSubTab = 'op_zones'; // 'op_zones' | 'states' | 'districts' | 'municipal_zones'

  // National Geographic Cascading Hierarchy Filter
  c.geoFilter = {
    opZone: '',
    state: '',
    district: '',
    localBody: '',
    municipalZone: '',
    ward: ''
  };

  // Geographic Search & View Models
  c.zoneSearch = '';
  c.stateSearch = '';
  c.stateZoneFilter = '';
  c.stateTypeFilter = '';
  c.districtSearch = '';
  c.localBodySearch = '';
  c.selectedOpZone = null;
  c.showOpZoneDetailModal = false;
  c.selectedState = null;
  c.showReassignStateModal = false;
  c.targetReassignZone = '';
  c.reassignReason = '';

  // Header State
  c.showNotifDrawer = false;
  c.showUserMenu = false;
  c.showProfileModal = false;
  c.showConfigModal = false;

  // Chat Assistant State
  c.showChatAssistant = false;
  c.chatInput = '';
  c.chatMessages = [
    {
      sender: 'bot',
      text: 'Hello Commissioner. I am your <strong>CIVIX Operations Copilot</strong>. How can I assist with municipal incidents, IoT telemetry, crew dispatches, or SLA metrics today?',
      time: 'Just now'
    }
  ];

  // Search & Filter Models
  c.search = {
    ticket: '',
    ticketCat: '',
    ticketZone: '',
    ticketStatus: '',
    case: '',
    caseStatus: '',
    citizen: '',
    citizenWard: '',
    iot: '',
    wo: '',
    audit: ''
  };

  // Modals Data
  c.selectedTicket = null;
  c.selectedCase = null;
  c.selectedCitizen = null;
  c.selectedWorkOrder = null;
  c.selectedAlert = null;
  c.rejectionReason = '';
  c.duplicatePrimaryCase = '';
  c.caseNotes = '';
  c.verificationNotes = '';
  c.zoneModalData = {};

  // Explainable Deterministic Priority Calculator Model
  c.priorityCalc = {
    severity: 4,
    peopleCount: 45,
    peopleFactor: 0.4,
    urgency: 0.8,
    essentialService: 0.9,
    confidence: 0.95,
    calculatedScore: 0,
    calculatedPriority: 'P2',
    targetSLA: '24 Hours'
  };

  // Crew Fit Scoring Model
  c.crewFitModalData = {
    workOrder: null,
    recommendations: []
  };

  // Flash / Toast alert
  c.toast = {
    show: false,
    type: 'success',
    message: ''
  };

  function showToast(msg, type) {
    c.toast.message = msg;
    c.toast.type = type || 'success';
    c.toast.show = true;
    setTimeout(function() {
      c.toast.show = false;
      $scope.$apply();
    }, 4000);
  }

  // --- NAVIGATION ---
  c.setTab = function(tabName) {
    c.currentTab = tabName;
    c.showNotifDrawer = false;
    c.showUserMenu = false;
    $window.scrollTo(0, 0);
  };

  // --- HEADER ACTIONS ---
  c.toggleNotifDrawer = function() {
    c.showNotifDrawer = !c.showNotifDrawer;
    c.showUserMenu = false;
  };

  c.toggleUserMenu = function() {
    c.showUserMenu = !c.showUserMenu;
    c.showNotifDrawer = false;
  };

  c.openProfileModal = function() {
    c.showProfileModal = true;
    c.showUserMenu = false;
  };

  c.closeProfileModal = function() {
    c.showProfileModal = false;
  };

  c.openConfigModal = function() {
    c.showConfigModal = true;
    c.showUserMenu = false;
  };

  c.closeConfigModal = function() {
    c.showConfigModal = false;
  };

  c.signOut = function() {
    $window.location.href = '?id=civix_portal_select';
  };

  c.markNotifRead = function(item) {
    if (item.u_is_read === 'true') return;
    item.u_is_read = 'true';
    if (c.data.unreadNotificationCount > 0) c.data.unreadNotificationCount--;
    c.server.get({ action: 'mark_notif_read', sys_id: item.sys_id });
  };

  c.markAllRead = function() {
    c.server.get({ action: 'mark_all_read' }).then(function(r) {
      if (c.data.notifications) {
        c.data.notifications.forEach(function(n) { n.u_is_read = 'true'; });
      }
      c.data.unreadNotificationCount = 0;
      showToast('All notifications marked as read', 'success');
    });
  };

  c.saveConfiguration = function() {
    c.server.get({ action: 'save_config', configs: c.data.configs }).then(function(r) {
      c.closeConfigModal();
      showToast('Municipal SLA & Threshold configurations saved and audited.', 'success');
    });
  };

  // --- CHAT ASSISTANT (CIVIX COPILOT) ---
  c.toggleChatAssistant = function() {
    c.showChatAssistant = !c.showChatAssistant;
  };

  c.openChatAssistant = function() {
    c.showChatAssistant = true;
  };

  c.closeChatAssistant = function() {
    c.showChatAssistant = false;
  };

  c.sendQuickChat = function(query) {
    c.chatInput = query;
    c.sendChatMessage();
  };

  c.sendChatMessage = function() {
    if (!c.chatInput || !c.chatInput.trim()) return;
    var userText = c.chatInput.trim();
    var nowStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    c.chatMessages.push({
      sender: 'user',
      text: userText,
      time: nowStr
    });
    c.chatInput = '';

    // Scroll chat feed
    setTimeout(function() {
      var feed = document.getElementById('civixChatFeed');
      if (feed) feed.scrollTop = feed.scrollHeight;
    }, 50);

    // Intelligent Bot Response Parser
    setTimeout(function() {
      var botResponse = '';
      var lower = userText.toLowerCase();

      if (lower.indexOf('p1') !== -1 || lower.indexOf('critical') !== -1 || lower.indexOf('emergency') !== -1) {
        botResponse = '<strong>Emergency P1 Incidents:</strong> Found <strong>1 Critical Incident</strong>:<br>&bull; <code>CIV-2026-00101</code>: Deep asphalt collapse on 1st Main Rd, Adyar (Ward 172). Target SLA: 4 Hours. Crew dispatch recommended immediately.';
      } else if (lower.indexOf('flood') !== -1 || lower.indexOf('sensor') !== -1 || lower.indexOf('iot') !== -1) {
        botResponse = '<strong>IoT Telemetry Status:</strong><br>&bull; <code>SEN-FL-179</code> (Thiruvanmiyur Sump): <strong>Water Level 850mm</strong> (Threshold: 600mm). Alert <code>ALT-2026-00041</code> is unacknowledged.<br>&bull; 4 other telemetry nodes (AQI, Waste Bins, Streetlights) are operating normally.';
      } else if (lower.indexOf('crew') !== -1 || lower.indexOf('work order') !== -1 || lower.indexOf('recommend') !== -1) {
        botResponse = '<strong>Crew Dispatch Recommendation:</strong><br>For <code>WO-2026-00105</code> (Adyar Roads):<br>&bull; <strong>Top Fit:</strong> Crew 1 - Rapid Pothole Patching Team (Fit Score: <strong>89/100</strong>, Lead: M. Kumar, Zone 13).<br>&bull; Skill Match: 95%, Proximity: High, Active Orders: 2.';
      } else if (lower.indexOf('sla') !== -1 || lower.indexOf('compliance') !== -1) {
        botResponse = '<strong>SLA Compliance Summary:</strong><br>&bull; Overall Corporation Compliance: <strong>' + (c.data.kpis ? c.data.kpis.slaCompliance : 80) + '%</strong>.<br>&bull; Total Incidents: ' + (c.data.kpis ? c.data.kpis.totalTickets : 5) + '<br>&bull; Overdue: 1 Case (<code>WO-2026-00105</code> breached 24-hr resolution window).';
      } else if (lower.indexOf('audit') !== -1 || lower.indexOf('log') !== -1) {
        botResponse = '<strong>Audit Trail Snapshot:</strong><br>Last recorded action: <em>Ticket Triage Approval</em> by Admin S. Ramanathan, IAS on <code>CIV-2026-00101</code>. All 6 administrative events are securely hashed and stored.';
      } else if (lower.indexOf('zone') !== -1 || lower.indexOf('ward') !== -1) {
        botResponse = '<strong>Administrative Division Status:</strong><br>Currently monitoring <strong>5 Corporation Zones</strong> (Adyar, T. Nagar, Royapuram, Anna Nagar, Kodambakkam) spanning 6 active administrative wards.';
      } else {
        botResponse = 'I can help you monitor live civic cases, query sensor breaches, check crew fitness rankings, and review SLA compliance. Try asking <em>"Show P1 critical cases"</em> or <em>"Check IoT flood sensor status"</em>.';
      }

      c.chatMessages.push({
        sender: 'bot',
        text: botResponse,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
      $scope.$apply();

      setTimeout(function() {
        var feed = document.getElementById('civixChatFeed');
        if (feed) feed.scrollTop = feed.scrollHeight;
      }, 50);
    }, 400);
  };

  // --- TICKET MANAGEMENT ACTIONS ---
  c.openAcceptModal = function(ticket) {
    c.selectedTicket = ticket;
    c.showAcceptModal = true;
  };

  c.confirmAcceptTicket = function() {
    if (!c.selectedTicket) return;
    c.server.get({
      action: 'accept_ticket',
      sys_id: c.selectedTicket.sys_id,
      category: c.selectedTicket.u_category
    }).then(function(r) {
      c.selectedTicket.u_state = 'Under Review';
      c.showAcceptModal = false;
      showToast('Ticket ' + c.selectedTicket.u_number + ' accepted into active investigation workflow.', 'success');
    });
  };

  c.openRejectModal = function(ticket) {
    c.selectedTicket = ticket;
    c.rejectionReason = '';
    c.showRejectModal = true;
  };

  c.confirmRejectTicket = function() {
    if (!c.selectedTicket || !c.rejectionReason) {
      showToast('Please provide a mandatory reason for ticket rejection.', 'error');
      return;
    }
    c.server.get({
      action: 'reject_ticket',
      sys_id: c.selectedTicket.sys_id,
      reason: c.rejectionReason
    }).then(function(r) {
      c.selectedTicket.u_state = 'Rejected';
      c.showRejectModal = false;
      showToast('Ticket ' + c.selectedTicket.u_number + ' rejected with audit reason logged.', 'warning');
    });
  };

  c.openDuplicateModal = function(ticket) {
    c.selectedTicket = ticket;
    c.duplicatePrimaryCase = '';
    c.showDuplicateModal = true;
  };

  c.confirmDuplicate = function() {
    if (!c.selectedTicket || !c.duplicatePrimaryCase) {
      showToast('Please specify the primary Case reference.', 'error');
      return;
    }
    c.server.get({
      action: 'mark_duplicate',
      sys_id: c.selectedTicket.sys_id,
      primaryCase: c.duplicatePrimaryCase
    }).then(function(r) {
      c.selectedTicket.u_state = 'Duplicate';
      c.showDuplicateModal = false;
      showToast('Ticket linked as duplicate of ' + c.duplicatePrimaryCase, 'info');
    });
  };

  // --- CASE MANAGEMENT ACTIONS ---
  c.openCaseDetails = function(kase) {
    c.selectedCase = kase;
    c.caseNotes = kase.u_resolution_notes || '';
    c.showCaseModal = true;
  };

  c.updateCaseStatus = function(newState) {
    if (!c.selectedCase) return;
    c.server.get({
      action: 'update_case_status',
      sys_id: c.selectedCase.sys_id,
      newState: newState,
      notes: c.caseNotes,
      reason: 'Administrative case review action'
    }).then(function(r) {
      c.selectedCase.u_state = newState;
      c.showCaseModal = false;
      showToast('Case ' + c.selectedCase.u_number + ' updated to ' + newState, 'success');
    });
  };

  // Priority Scoring Engine Calculation
  c.calculatePriority = function() {
    var pCount = parseInt(c.priorityCalc.peopleCount, 10) || 1;
    var pf = 0.1;
    if (pCount > 500) pf = 1.0;
    else if (pCount > 50) pf = 0.7;
    else if (pCount > 5) pf = 0.4;
    c.priorityCalc.peopleFactor = pf;

    // Formula: Priority Score = 30 * (Severity / 5) + 25 * People Factor + 20 * Urgency + 15 * Essential Service + 10 * Confidence
    var sevPart = 30 * (parseFloat(c.priorityCalc.severity) / 5.0);
    var peoPart = 25 * pf;
    var urgPart = 20 * parseFloat(c.priorityCalc.urgency);
    var essPart = 15 * parseFloat(c.priorityCalc.essentialService);
    var conPart = 10 * parseFloat(c.priorityCalc.confidence);

    var score = Math.round(sevPart + peoPart + urgPart + essPart + conPart);
    c.priorityCalc.calculatedScore = score;

    if (score >= 70) {
      c.priorityCalc.calculatedPriority = 'P1 - Critical';
      c.priorityCalc.targetSLA = '4 Hours (Immediate Escalation)';
    } else if (score >= 50) {
      c.priorityCalc.calculatedPriority = 'P2 - High';
      c.priorityCalc.targetSLA = '24 Hours';
    } else if (score >= 30) {
      c.priorityCalc.calculatedPriority = 'P3 - Medium';
      c.priorityCalc.targetSLA = '72 Hours';
    } else {
      c.priorityCalc.calculatedPriority = 'P4 - Low';
      c.priorityCalc.targetSLA = '168 Hours (7 Days)';
    }
  };

  c.openPriorityCalculator = function(kase) {
    c.selectedCase = kase || c.selectedCase;
    c.calculatePriority();
    c.showPriorityCalcModal = true;
  };

  c.applyCalculatedPriority = function() {
    if (!c.selectedCase) return;
    c.selectedCase.u_priority = c.priorityCalc.calculatedPriority;
    c.showPriorityCalcModal = false;
    showToast('Applied deterministic score ' + c.priorityCalc.calculatedScore + ' (' + c.priorityCalc.calculatedPriority + ') to case.', 'success');
  };

  // --- CITIZEN MANAGEMENT ---
  c.openCitizenDossier = function(citizen) {
    c.selectedCitizen = citizen;
    c.showCitizenModal = true;
  };

  // --- IOT MONITORING ACTIONS ---
  c.acknowledgeAlert = function(alertItem) {
    c.server.get({ action: 'acknowledge_alert', sys_id: alertItem.sys_id }).then(function(r) {
      alertItem.u_state = 'Acknowledged';
      alertItem.u_acknowledged_by = c.data.currentUser.name;
      if (c.data.kpis && c.data.kpis.unackAlerts > 0) c.data.kpis.unackAlerts--;
      showToast('IoT Alert ' + alertItem.u_alert_id + ' marked as Acknowledged.', 'success');
    });
  };

  c.convertAlertToCase = function(alertItem) {
    c.server.get({ action: 'convert_alert_to_case', sys_id: alertItem.sys_id }).then(function(r) {
      alertItem.u_state = 'Dispatched';
      showToast(r.data.actionResult.message || 'Alert converted to Civic Case.', 'success');
      c.server.refresh();
    });
  };

  // --- WORK ORDERS & CREW RECOMMENDATION ENGINE ---
  c.openCrewRecommendationModal = function(wo) {
    c.crewFitModalData.workOrder = wo;
    var recs = [];
    if (c.data.crews && c.data.crews.length > 0) {
      c.data.crews.forEach(function(cr) {
        var skillMatch = 0.9;
        var avail = (cr.u_status === 'Active' || cr.u_status === 'Available') ? 1.0 : 0.5;
        var prox = (cr.u_zone === wo.u_zone) ? 1.0 : 0.6;
        var workL = Math.min(parseInt(cr.u_active_jobs || 1, 10) / 5.0, 1.0);

        // Formula: Crew Fit = 35 * Skill Match + 25 * Availability + 20 * Proximity + 20 * (1 - Workload)
        var fitScore = Math.round(35 * skillMatch + 25 * avail + 20 * prox + 20 * (1 - workL));

        recs.push({
          crew_id: cr.u_crew_id,
          name: cr.u_crew_name,
          leader: cr.u_leader_name,
          skills: cr.u_skills,
          zone: cr.u_zone,
          active_jobs: cr.u_active_jobs,
          fitScore: fitScore
        });
      });
      recs.sort(function(a, b) { return b.fitScore - a.fitScore; });
    }
    c.crewFitModalData.recommendations = recs;
    c.showCrewFitModal = true;
  };

  c.assignCrewToWo = function(crew) {
    if (!c.crewFitModalData.workOrder) return;
    c.crewFitModalData.workOrder.u_worker_name = crew.name + ' (' + crew.leader + ')';
    c.crewFitModalData.workOrder.u_state = 'Assigned';
    c.showCrewFitModal = false;
    showToast('Crew ' + crew.name + ' recommended (Score: ' + crew.fitScore + ') and assigned to ' + c.crewFitModalData.workOrder.u_number, 'success');
  };

  c.openVerifyModal = function(wo) {
    c.selectedWorkOrder = wo;
    c.verificationNotes = '';
    c.showVerifyModal = true;
  };

  c.confirmVerification = function(approved) {
    if (!c.selectedWorkOrder) return;
    c.server.get({
      action: 'verify_work_order',
      sys_id: c.selectedWorkOrder.sys_id,
      approved: approved,
      notes: c.verificationNotes
    }).then(function(r) {
      if (approved) {
        c.selectedWorkOrder.u_state = 'Completed';
        c.selectedWorkOrder.u_verification_status = 'Approved';
        showToast('Work Order verified and approved. Incident closed.', 'success');
      } else {
        c.selectedWorkOrder.u_state = 'In Progress';
        c.selectedWorkOrder.u_verification_status = 'Rejected / Re-execute';
        showToast('Work Order returned to In Progress for rework.', 'warning');
      }
      c.showVerifyModal = false;
    });
  };

  // --- NATIONAL GEOGRAPHIC HIERARCHY & ZONE MANAGEMENT ---
  c.setZoneSubTab = function(sub) {
    c.zoneSubTab = sub;
  };

  c.openOpZoneDetail = function(oz) {
    c.selectedOpZone = oz;
    c.showOpZoneDetailModal = true;
  };

  c.toggleOpZoneStatus = function(oz) {
    c.server.get({
      action: 'toggle_op_zone_status',
      sys_id: oz.sys_id
    }).then(function(r) {
      oz.u_status = (oz.u_status === 'Active') ? 'Inactive' : 'Active';
      showToast(r.data.actionResult.message || 'Operational Zone status updated.', 'success');
    });
  };

  c.openReassignStateModal = function(st) {
    c.selectedState = st;
    c.targetReassignZone = st.u_op_zone_code;
    c.reassignReason = '';
    c.showReassignStateModal = true;
  };

  c.confirmReassignState = function() {
    if (!c.selectedState || !c.targetReassignZone) return;
    if (c.targetReassignZone === c.selectedState.u_op_zone_code) {
      showToast('Target zone is identical to currently assigned zone.', 'info');
      return;
    }
    c.server.get({
      action: 'reassign_state_zone',
      sys_id: c.selectedState.sys_id,
      target_zone_code: c.targetReassignZone,
      reason: c.reassignReason
    }).then(function(r) {
      if (r.data.actionResult && r.data.actionResult.status === 'error') {
        showToast(r.data.actionResult.message, 'error');
      } else {
        showToast(r.data.actionResult.message || 'State reassigned successfully.', 'success');
        c.showReassignStateModal = false;
        c.server.refresh();
      }
    });
  };

  // Cascading Dropdown Filter Handlers
  c.onGeoZoneChange = function() {
    c.geoFilter.state = '';
    c.geoFilter.district = '';
    c.geoFilter.localBody = '';
    c.geoFilter.municipalZone = '';
    c.geoFilter.ward = '';
  };

  c.onGeoStateChange = function() {
    c.geoFilter.district = '';
    c.geoFilter.localBody = '';
    c.geoFilter.municipalZone = '';
    c.geoFilter.ward = '';
  };

  c.onGeoDistrictChange = function() {
    c.geoFilter.localBody = '';
    c.geoFilter.municipalZone = '';
    c.geoFilter.ward = '';
  };

  c.onGeoLocalBodyChange = function() {
    c.geoFilter.municipalZone = '';
    c.geoFilter.ward = '';
  };

  c.resetGeoFilters = function() {
    c.geoFilter = {
      opZone: '',
      state: '',
      district: '',
      localBody: '',
      municipalZone: '',
      ward: ''
    };
  };

  c.getStatesForZone = function(zoneNameOrCode) {
    if (!c.data.states) return [];
    if (!zoneNameOrCode) return c.data.states;
    return c.data.states.filter(function(s) {
      return s.u_op_zone_code === zoneNameOrCode || s.u_op_zone_name === zoneNameOrCode;
    });
  };

  c.getDistrictsForState = function(stateName) {
    if (!c.data.districts) return [];
    if (!stateName) return c.data.districts;
    return c.data.districts.filter(function(d) {
      return d.u_state_name === stateName;
    });
  };

  c.getLocalBodiesForDistrict = function(distName) {
    if (!c.data.localBodies) return [];
    if (!distName) return c.data.localBodies;
    return c.data.localBodies.filter(function(lb) {
      return lb.u_district_name === distName;
    });
  };

  c.getMunicipalZonesForLocalBody = function(lbName) {
    if (!c.data.zones) return [];
    if (!lbName) return c.data.zones;
    return c.data.zones.filter(function(z) {
      return z.u_local_body_name === lbName || z.u_local_body === lbName;
    });
  };

  c.filterWardsByGeo = function(w) {
    if (c.geoFilter.opZone && w.u_op_zone && w.u_op_zone !== c.geoFilter.opZone) return false;
    if (c.geoFilter.state && w.u_state_name && w.u_state_name !== c.geoFilter.state) return false;
    if (c.geoFilter.district && w.u_district_name && w.u_district_name !== c.geoFilter.district) return false;
    if (c.geoFilter.localBody && w.u_local_body_name && w.u_local_body_name !== c.geoFilter.localBody) return false;
    if (c.geoFilter.municipalZone && w.u_zone && w.u_zone !== c.geoFilter.municipalZone && w.u_municipal_zone !== c.geoFilter.municipalZone) return false;
    if (c.search.citizenWard) {
      var q = c.search.citizenWard.toLowerCase();
      return (w.u_ward_name && w.u_ward_name.toLowerCase().indexOf(q) !== -1) ||
             (w.u_ward_code && w.u_ward_code.toLowerCase().indexOf(q) !== -1);
    }
    return true;
  };

  c.filterCasesByGeo = function(k) {
    if (c.geoFilter.opZone && k.u_op_zone && k.u_op_zone !== c.geoFilter.opZone) return false;
    if (c.geoFilter.state && k.u_state_name && k.u_state_name !== c.geoFilter.state) return false;
    if (c.geoFilter.district && k.u_district_name && k.u_district_name !== c.geoFilter.district) return false;
    if (c.geoFilter.localBody && k.u_local_body_name && k.u_local_body_name !== c.geoFilter.localBody) return false;
    if (c.geoFilter.municipalZone && k.u_zone && k.u_zone !== c.geoFilter.municipalZone) return false;
    if (c.geoFilter.ward && k.u_ward && k.u_ward.indexOf(c.geoFilter.ward) === -1) return false;
    return true;
  };

  c.filterIotByGeo = function(s) {
    if (c.geoFilter.opZone && s.u_op_zone && s.u_op_zone !== c.geoFilter.opZone) return false;
    if (c.geoFilter.state && s.u_state_name && s.u_state_name !== c.geoFilter.state) return false;
    if (c.geoFilter.district && s.u_district_name && s.u_district_name !== c.geoFilter.district) return false;
    if (c.geoFilter.localBody && s.u_local_body_name && s.u_local_body_name !== c.geoFilter.localBody) return false;
    if (c.geoFilter.ward && s.u_ward && s.u_ward.indexOf(c.geoFilter.ward) === -1) return false;
    return true;
  };

  // --- MUNICIPAL ZONE ACTIONS ---
  c.openAddZoneModal = function() {
    c.zoneModalData = {
      isNew: true,
      code: 'Z-' + (c.data.zones.length + 1),
      name: '',
      description: '',
      engineer: '',
      phone: '',
      status: 'Active'
    };
    c.showZoneModal = true;
  };

  c.openEditZoneModal = function(z) {
    c.zoneModalData = {
      isNew: false,
      sys_id: z.sys_id,
      code: z.u_zone_code,
      name: z.u_zone_name,
      description: z.u_description,
      engineer: z.u_executive_engineer,
      phone: z.u_contact_phone,
      status: z.u_status || 'Active'
    };
    c.showZoneModal = true;
  };

  c.saveZone = function() {
    if (!c.zoneModalData.name || !c.zoneModalData.code) {
      showToast('Please provide Zone Code and Zone Name.', 'error');
      return;
    }
    c.server.get({
      action: 'save_zone',
      sys_id: c.zoneModalData.sys_id,
      code: c.zoneModalData.code,
      name: c.zoneModalData.name,
      description: c.zoneModalData.description,
      engineer: c.zoneModalData.engineer,
      phone: c.zoneModalData.phone,
      status: c.zoneModalData.status
    }).then(function(r) {
      c.showZoneModal = false;
      showToast('Zone ' + c.zoneModalData.name + ' saved successfully.', 'success');
      c.server.refresh();
    });
  };

  // --- ANALYTICS & CSV EXPORT ---
  c.exportReportCSV = function() {
    var rows = [
      ['Metric', 'Value', 'Source / Department'],
      ['Total Tickets', c.data.kpis.totalTickets, 'Citizen Portal & Triage'],
      ['Active Cases', c.data.kpis.openCases, 'Civic Operations'],
      ['Resolved Cases', c.data.kpis.resolvedCases, 'Field Service Verification'],
      ['Overdue Cases', c.data.kpis.overdueCases, 'SLA Enforcement Engine'],
      ['Active Work Orders', c.data.kpis.activeWorkOrders, 'Engineering Crews'],
      ['IoT Telemetry Sensors', c.data.kpis.activeSensors + ' Online / ' + c.data.kpis.totalSensors + ' Registered', 'Smart City Telemetry'],
      ['Unacknowledged Alerts', c.data.kpis.unackAlerts, 'SCADA Sentinel Grid'],
      ['SLA Compliance Target', c.data.kpis.slaCompliance + '%', 'Municipal Benchmark (Target >= 90%)']
    ];

    var csvContent = "data:text/csv;charset=utf-8," + rows.map(function(e) { return e.join(","); }).join("\n");
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "CIVIX_Operations_Report_" + new Date().toISOString().slice(0, 10) + ".csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Analytics summary exported as CSV successfully.', 'success');
  };

  // Close modals on Escape key
  $window.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      c.showAcceptModal = false;
      c.showRejectModal = false;
      c.showDuplicateModal = false;
      c.showCaseModal = false;
      c.showPriorityCalcModal = false;
      c.showCitizenModal = false;
      c.showCrewFitModal = false;
      c.showVerifyModal = false;
      c.showZoneModal = false;
      c.showProfileModal = false;
      c.showConfigModal = false;
      c.showNotifDrawer = false;
      c.showUserMenu = false;
      c.showChatAssistant = false;
      $scope.$apply();
    }
  });
};
