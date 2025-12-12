from odoo import models, fields

class Computer(models.Model):
    _name="assets_computer"
    
    name = fields.Char()
    is_used = fields.Boolean()
    inventoryNumber = fields.Char()
    serialNumber = fields.Char()
    user_id = fields.Many2one('hr.employee', string="Assigned User")
    department_id = fields.Many2one('hr.department', string="Department", related='user_id.department_id', store=True, readonly=True)
    details = fields.Text()

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string="Price", currency_field='currency_id')
    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                string='Company',
                                related='project_id.company_id',
                                store = True,
                                readonly = True)

    computer_type = fields.Char()
    model = fields.Char()
    cpu = fields.Char()
    gpu = fields.Char()
    memory = fields.Char()
    ip_address = fields.Char()
    monitor_ids = fields.One2many('assets_monitor','computer_id', string='Monitors', readonly=True)

    history_ids = fields.One2many(
        comodel_name='assets_history',
        inverse_name='id',
        compute='_compute_history_ids',
        string="Last 5 History",
        store=False
    )

    def _compute_history_ids(self):
        for record in self:
            histories = self.env['assets_history'].search([
                ('asset', '=', f'assets_computer,{record.id}')
            ], order='id desc', limit=5)

            record.history_ids = histories

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
                'default_asset': f'assets_computer,{self.id}'
            }
        }

