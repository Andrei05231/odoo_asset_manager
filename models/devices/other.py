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
    
    def action_create_history(self):
        self.ensure_one()
        return {
            'name': 'New History',
            'type': 'ir.actions.act_window',
            'res_model': 'assets_history',
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
            'context': {
                'default_asset': f'assets_other,{self.id}'
            }
        }
    def _compute_history_ids(self):
        for record in self:
            histories = self.env['assets_history'].search([
                ('asset', '=', f'assets_other,{record.id}')
            ], order='id desc', limit=5)

            record.history_ids = histories


