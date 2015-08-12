var registrationUtils = require('js/registrationUtils');
var RegistrationEditor = registrationUtils.RegistrationEditor;
var $ = require('jquery');
var $osf = require('js/osfHelpers');

$(document).ready(function() {

	var params = context[0];
	// TODO: add approve, reject, and request revision urls
	var draftEditor = new RegistrationEditor({
	    schemas: '/get-schemas/',
	    update: '/update-draft/{draft_pk}/',
	    approve: '/approve-draft/{draft_pk}/',
	    //update_approval: '/update-approval/{approval_pk}/',
	    home: '/prereg/'
	    //get: node.urls.api + 'draft/{draft_pk}/'
	}, 'registrationEditor');

	var draft = new registrationUtils.Draft(params);
	draftEditor.init(draft);
	window.draftEditor = draftEditor;
	$osf.applyBindings(draftEditor, '#draftRegistrationScope');

});
