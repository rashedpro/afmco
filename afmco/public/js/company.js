frappe.ui.form.on("Company", {
	setup: function(frm) {
        frm.set_query('default_jv_debit_account_cf', () => {
            return {
                filters: {
                    is_group: 0
                }
            }
        })
        frm.set_query('default_jv_credit_account_cf', () => {
            return {
                filters: {
                    is_group: 0
                }
            }
        })        
    }
})