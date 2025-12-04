from odoo import models, fields 

class project(models.Model):
    _name = "assets_project"

    name = fields.Char()
    date = fields.Date()

    company_id = fields.Many2one(
        'res.company',
        string = "Company",
        required = True
    )

    finance_type = fields.Selection( [ 
                ('pnrr','PNRR'),
                ('adr','ADR'),
                ('por','POR'),
                ('self','Self Financing')
             ],
            string="Type",
            )
