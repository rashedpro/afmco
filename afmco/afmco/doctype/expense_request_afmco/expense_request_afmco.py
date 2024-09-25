# Copyright (c) 2023, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext import get_default_company
from frappe.utils import  money_in_words
import datetime
import json
class ExpenseRequestAfmco(Document):
	def validate(self):
		if self.amount:
			self.amount_in_words=money_in_words(self.amount,frappe.get_cached_value("Company", get_default_company(), "default_currency"))

@frappe.whitelist()
def create_journal_entry(doc):
	tax_account=""
	tax_amount=0
	paid_amount=0
	accounts = []
	doc=json.loads(doc)
	if doc["is_taxable"]:
		tax_account=get_purchase_tax()
		tax_amount=(doc["amount"]/100)*15
		paid_amount=doc["amount"]-tax_amount
		accounts.append({
        "account":tax_account,
        "credit_in_account_currency":tax_amount,
		"cost_center":doc["cost_center"]})
	else:
		paid_amount=doc["amount"]
	
	journal_entry = frappe.new_doc("Journal Entry")
	journal_entry.voucher_type = "Journal Entry"
	journal_entry.naming_series="ACC-JV-.YYYY.-"
	journal_entry.user_remark = doc["remark"]
	journal_entry.expense_request_cf=doc["name"]
	
	journal_entry.company=frappe.defaults.get_global_default("company")
	journal_entry.posting_date=datetime.date.today()
	accounts.append({
        "account":doc["paid_account"],
        "credit_in_account_currency":paid_amount,
		"cost_center":doc["cost_center"]
    })

	accounts.append({
        "account":doc["expense_account"],
        "debit_in_account_currency":doc["amount"],
		"cost_center":doc["cost_center"]
    })
	journal_entry.set("accounts", accounts)  
	journal_entry.total_debit=doc["amount"]
	journal_entry.total_credit=doc["amount"]
	journal_entry.posting_date=doc["date"]
	journal_entry.save()
	journal_entry.submit()
	frappe.db.set_value('Expense Request Afmco', doc["name"],'journal_entry_reference',journal_entry.name)
	



def get_purchase_tax():
	data=frappe.db.sql(""" select account_head from `tabPurchase Taxes and Charges Template`as  ptct 
			   			join `tabPurchase Taxes and Charges` as ptc on ptct.name=ptc.parent
			   			where ptct.is_default=1 """,as_dict=True)[0]
	
	return data["account_head"]