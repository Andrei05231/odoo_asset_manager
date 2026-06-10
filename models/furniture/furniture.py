from odoo import fields, models 

class Furniture(models.Model):
    _name = "assets.furniture"
    _description = "Furniture stuff"
    
    _inherit = ['mail.thread', 'mail.activity.mixin', 'assets_inventory_mixin']

    name = fields.Char()

    furniture_type = fields.Char()

    details = fields.Text()
    

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
                'default_asset': f'assets.furniture,{self.id}'
            }
        }
    def _compute_history_ids(self):
        for record in self:
            histories = self.env['assets_history'].search([
                ('asset', '=', f'assets.furniture,{record.id}')
            ], order='id desc', limit=5)

            record.history_ids = histories



