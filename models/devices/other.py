from odoo import models, fields
from odoo.exceptions import UserError  # type: ignore

class Other(models.Model):
    _name = "assets_other"
    _inherit = ["assets_inventory_mixin"]

    name = fields.Char(string="Name")
    inventory = fields.Char(string="Inventory Number")

    inventory_code = fields.Char(
        string="Inventory Code",
        related='inventory_number_id.code',
        readonly=True,
        store=True
    )


    serial = fields.Char(string="Serial Number")
    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                 related='project_id.company_id',
                                 store=True,
                                 readonly=True,
                                 string="Company")
    details = fields.Text(string="Description")

    asset_status = fields.Selection([
        ('odered',"Ordered"),
        ('arrived',"Arrived"),
        ('active', "Active")
    ],
        string="Asset Status")
    