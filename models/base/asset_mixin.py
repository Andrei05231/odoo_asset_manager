from odoo import models, fields

class AssetMixin(models.Model):
    _name="assets_mixin"
    _inherit=['assets_inventory_mixin']
    
    name = fields.Char()

    note = fields.Text(string='Notes')

    inventory_code = fields.Char(
        string="Inventory Code",
        related='inventory_number_id.code',
        readonly=True,
        store=True
    )

    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                string='Company',
                                related='project_id.company_id',
                                store = True,
                                readonly = True)
    
    asset_status = fields.Selection([
        ('odered',"Ordered"),
        ('arrived',"Arrived"),
        ('active', "Active")
    ],
        string="Asset Status")
