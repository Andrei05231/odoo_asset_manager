from odoo import models, fields

class Printer(models.Model):
    _name = "assets_printer"

    ip = fields.Char(string="IP Address")
    name = fields.Char(string="Name")
    model = fields.Char(string="Model")
    inventory = fields.Char(string="Inventory Number")
    serial = fields.Char(string="Serial Number")
    status = fields.Selection(
        [
            ('active', 'Active'),
            ('defect',"Defect"),
            ('offline','Offline')
        ],
        string="Status"
    )
    project_id = fields.Many2one('assets_project', string='Project')
    company_id = fields.Many2one('res.company',
                                  related="project_id.company_id",
                                  store=True,
                                  readonly=True,
                                  string="Company")
    