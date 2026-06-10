from odoo import fields, models 

class Server(models.Model):
    _name = "assets.server"
    _description = "Server related asset"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'assets_inventory_mixin']


    name = fields.Char()
    details = fields.Text()

    usage = fields.Char()
    
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
                'default_asset': f'assets.server,{self.id}'
            }
        }
    def _compute_history_ids(self):
        for record in self:
            histories = self.env['assets_history'].search([
                ('asset', '=', f'assets.server,{record.id}')
            ], order='id desc', limit=5)

            record.history_ids = histories


