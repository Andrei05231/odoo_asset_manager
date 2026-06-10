from odoo import models, fields

class AssetPhone(models.Model):
    _name="assets_phone"
    _inherit = ['assets_mixin', 'mail.thread', 'mail.activity.mixin']

    
    model = fields.Char()

    phone_number = fields.Char()

    serial = fields.Char()

    user_id = fields.Many2one('hr.employee', string="Assigned User", tracking=True)
    department_id = fields.Many2one('hr.department', string="Department", related='user_id.department_id', store=True, readonly=True)
    
    device_type = fields.Selection([
        ('phone', "Phone"),
        ('tables', "Tablet")
    ], string = "Type")

       
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
                'default_asset': f'assets_phone,{self.id}'
            }
        }
    def _compute_history_ids(self):
        for record in self:
            histories = self.env['assets_history'].search([
                ('asset', '=', f'assets_phone,{record.id}')
            ], order='id desc', limit=5)

            record.history_ids = histories


