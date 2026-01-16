from odoo import models, fields, api
import logging

from ..utils.computer_helpers import _process_computer_update,_calculate_summary, _process_monitor_data


_logger = logging.getLogger(__name__)

class Computer(models.Model):
    _name="assets_computer"
    
    name = fields.Char()
    is_used = fields.Boolean()
    inventoryNumber = fields.Char()
    serialNumber = fields.Char()
    user_id = fields.Many2one('hr.employee', string="Assigned User")
    department_id = fields.Many2one('hr.department', string="Department", related='user_id.department_id', store=True, readonly=True)
    details = fields.Text()

    tag_ids = fields.Many2many('assets_tag', string="Tags")

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string="Price", currency_field='currency_id')
    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                string='Company',
                                related='project_id.company_id',
                                store = True,
                                readonly = True)
    computer_type = fields.Selection([
                                    ('desktop', 'Desktop'),
                                    ('notebook', 'Notebook'),
                                    ('tower','Tower'),
                                    ('mini', "Mini Tower")
                                ],string="Type")
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

    manual_complete = fields.Boolean(string="Complete Data")

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
    

    @api.model
    def batch_update(self, payload):
        """
        Expected payload format:

        {
            "computers": [
                {
                    "serialNumber": "ABC123",
                    "name": "PC-01",
                    "cpu": "i7",
                    "gpu": "RTX 3070",
                    "memory": 32
                }
            ]
        }
        """

        if not isinstance(payload, dict):
            return {
                'success': False,
                'error': 'Payload must be a JSON object'
            }

        computers_data = payload.get('computers', [])

        if not computers_data:
            return {
                'success': False,
                'error': 'No computers provided'
            }

        Computer = self.env['assets_computer']
        Monitor = self.env['assets_monitor']
        results = []

        for computer_data in computers_data:
            if not isinstance(computer_data, dict):
                results.append({
                    'status': 'error',
                    'error': 'Invalid computer payload'
                })
                continue

            result = _process_computer_update(
                Computer,
                computer_data,
                _logger,
            )

            monitor_results = _process_monitor_data(Monitor, Computer, computer_data)
            results.append(result)

        return {
            'success': True,
            'results': results,
            'computer_summary': _calculate_summary(results),
            'monitor_summary': monitor_results
            
        }
