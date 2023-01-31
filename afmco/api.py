import frappe
from frappe import _
from frappe.utils import flt,today,get_link_to_form
import erpnext

def update_expense_request_jv_status(self,method):
    if self.expense_request_cf:
        if method=='validate':
            frappe.db.set_value('Expense Request Afmco', self.expense_request_cf, 'jv_status', 'JV Created')
            msg =_("Expencse Request {0} , JV status is updated to <b>JV Created</b>".format(frappe.bold(get_link_to_form('Expense Request Afmco',self.expense_request_cf))))
            frappe.msgprint(msg, title=_("Expense Request"),alert=1)
        elif method=='on_cancel' or  method=='on_trash':
            frappe.db.set_value('Expense Request Afmco', self.expense_request_cf, 'jv_status', 'JV Not Created')
            msg =_("Expencse Request {0} , JV status is updated to <b>JV Not Created</b>".format(frappe.bold(get_link_to_form('Expense Request Afmco',self.expense_request_cf))))
            frappe.msgprint(msg, title=_("Expense Request"),alert=1)            

def create_journal_entry(self,method):
    enable_jv_creation_on_sales_invoice_submit_cf = frappe.db.get_value('Company', self.company, 'enable_jv_creation_on_sales_invoice_submit_cf')
    if enable_jv_creation_on_sales_invoice_submit_cf==1:
        default_jv_debit_account_cf=frappe.db.get_value('Company', self.company, 'default_jv_debit_account_cf')
        default_jv_credit_account_cf=frappe.db.get_value('Company', self.company, 'default_jv_credit_account_cf')
        precision = frappe.get_precision("Sales Invoice", "net_total")
        accounts = []
        # credit entry
        accounts.append({
            "account": default_jv_credit_account_cf,
            "credit_in_account_currency": flt(self.net_total, precision),
            "cost_center": self.get("items")[0].cost_center or ''
        })
        # debit entry
        accounts.append({
            "account": default_jv_debit_account_cf,
            "debit_in_account_currency": flt(self.net_total, precision),
            "cost_center": self.get("items")[0].cost_center or ''
        })
        user_remark="It is auto created on submit of Sales Invoice {0}".format(self.name)
        journal_entry = frappe.new_doc('Journal Entry')
        journal_entry.voucher_type = 'Journal Entry'
        journal_entry.user_remark =user_remark
        journal_entry.company = self.company
        journal_entry.posting_date = self.jv_due_date_cf
        journal_entry.set("accounts", accounts)
        journal_entry.jv_based_on_submitted_si_cf=self.name
        journal_entry.save(ignore_permissions = True)				
        journal_entry.submit()	
        msg = _('Journal Entry {0} is created.'.format(frappe.bold(get_link_to_form('Journal Entry',journal_entry.name))))   
        frappe.msgprint(msg)	 