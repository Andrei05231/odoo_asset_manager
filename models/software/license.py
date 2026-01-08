from odoo import models, fields

class License(models.Model):
    _name = "assets_license"

    name = fields.Char()
    software_id=fields.Many2one("assets_software", string="Software")
    license_type = fields.Selection([
            ('key',"Key"),
            ('account', "Account"),
            ('server', "License Server"),
            ('other',"Other"),
        ],string="Type")
    licence_linked_acount = fields.Char()
    licence_server = fields.Char()
    licence_key= fields.Char()
    inventory_number = fields.Char()
    notes = fields.Text(string="Notes(optional)")
    computer_id = fields.Many2many("assets_computer", string="Computer")
    user_id = fields.Many2one("hr.employee",
            related="computer_id.user_id",
            store=True,
            readonly=True,            
            string="Assigned User"          
        )
    finance_project_id = fields.Many2one("assets_project", string="Financing Project")
    company_id = fields.Many2one("res.company", 
            related="finance_project_id.company_id",
            store=True,
            readonly=True,
            string="Company"                         
        )
    
