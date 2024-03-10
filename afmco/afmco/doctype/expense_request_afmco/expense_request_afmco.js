// Copyright (c) 2023, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Request Afmco', {
	// setup: function (frm) {
	// 	if (frm.doc.created_by == undefined) {
	// 		frm.set_value('created_by', frappe.session.user)
	// 	}
	// },
	refresh: function (frm) {

		if (frm.doc.created_by == undefined) {
			frm.set_value('created_by', frappe.session.user)
		}

		if (frm.doc.docstatus == 1) {
			if(frm.doc.journal_entry_reference===undefined || frm.doc.journal_entry_reference==='')
			frm.add_custom_button(__("Create JV"), function () {
				frappe.call({
					args: {
						"doc": frm.doc,
					},
					method: "afmco.afmco.doctype.expense_request_afmco.expense_request_afmco.create_journal_entry",
					callback: function(r) {}
				});
				// let journal_entry = frappe.model.get_new_doc("Journal Entry");
				// journal_entry.expense_request_cf = frm.doc.name;
				// frappe.set_route("Form", journal_entry.doctype, journal_entry.name);

			}).addClass('btn-primary');
		}
	}
});