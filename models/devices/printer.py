from odoo import models, fields

class Printer(models.Model):
    _name = "assets_printer"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'assets_inventory_mixin']

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
    def _compute_history_ids(self):
        for record in self:
            histories = self.env['assets_history'].search([
                ('asset', '=', f'assets_printer,{record.id}')
            ], order='id desc', limit=5)

            record.history_ids = histories


