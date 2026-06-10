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
            ('assets_monitor',"Monitor"),
            ('assets_printer',"Printer"),
            ('assets_phone',"Telefon/Tableta"),
            ('assets_other',"Echipamente ingineresti"),
            ('assets.furniture',"Mobilier"),
            ('assets.server',"Server"),
        ],
        string='Related Asset'
    )
    expense_id = fields.Many2one('hr.expense', string = 'Expense')
