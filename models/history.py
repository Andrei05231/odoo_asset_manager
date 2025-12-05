from odoo import models, fields 

class Hystory(models.Model):
    _name = "assets_history"

    history_type = fields.Selection([
            ('maintanace', "Maintenance"),
            ('upgrade', "Upgrade"),
            ('other', 'Other'),
        ],                            
        string="Type")
    notes = fields.Text()
    asset = fields.Reference(
        selection=[
            ('assets_computer',"Computer"),
            ('assets_monitor',"Monitor")
        ],
        string='Related Asset'
    )
    expense_id = fields.Many2one('hr.expense', string = 'Expense')