from odoo import models, fields

class Peripheral(models.Model):
    _name = "assets_peripheral"
    _inherit = ["assets_inventory_mixin", "mail.thread", "mail.activity.mixin"]
    _description = "Computer Peripheral"

    name = fields.Char(required=True, tracking=True)

    peripheral_type = fields.Selection([
        ('mouse', 'Mouse'),
        ('keyboard', 'Keyboard'),
        ('combo','Mouse + Keyboard Kit'),
        ('headset', 'Headset'),
        ('webcam', 'Webcam'),
        ('speaker', 'Speaker'),
        ('other', 'Other'),
    ], string="Type", required=True, tracking=True)

    is_used = fields.Boolean(default=False)

    computer_id = fields.Many2one(
        'assets_computer',
        string="Computer",
        tracking=True
    )

    serial_number = fields.Char()
    inventory_number = fields.Char()
    model = fields.Char()
    manufacturer = fields.Char()
    details = fields.Char()

    user_id = fields.Many2one(
        'hr.employee',
        string="Assigned User",
        related='computer_id.user_id',
        store=True,
        readonly=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    price = fields.Monetary(
        string="Price",
        currency_field='currency_id'
    )

    project_id = fields.Many2one(
        'assets_project',
        string="Project"
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='project_id.company_id',
        store=True,
        readonly=True
    )

    asset_date = fields.Date()

    history_ids = fields.One2many(
        'assets_history',
        compute='_compute_history_ids',
        string='History'
    )

    def action_create_history(self):
        self.ensure_one()
        return {
            'name': 'New History',
            'type': 'ir.actions.act_window',
            'res_model': 'assets_history',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_asset': f'assets_peripheral,{self.id}'
            }
        }

    def _compute_history_ids(self):
        for record in self:
            record.history_ids = self.env['assets_history'].search([
                ('asset', '=', f'assets_peripheral,{record.id}')
            ], order='id desc', limit=5)
