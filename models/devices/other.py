from odoo import models, fields

class Other(models.Model):
    _name = "assets_other"

    name = fields.Char(string="Name")
    inventory = fields.Char(string="Inventory Number")
    serial = fields.Char(string="Serial Number")
    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                 related='project_id.company_id',
                                 store=True,
                                 readonly=True,
                                 string="Company")
    details = fields.Text(string="Description")