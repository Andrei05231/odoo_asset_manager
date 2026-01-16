from odoo import models, fields

class Monitor(models.Model):
    _name = "assets_monitor"

    name = fields.Char()
    is_used = fields.Boolean()
    computer_id = fields.Many2one("assets_computer", string="Computer")
    serial_number = fields.Char()
    inventory_number = fields.Char()
    model = fields.Char()
    details = fields.Char()
    user_id = fields.Many2one('hr.employee',
                              string="Assigned User",
                              related='computer_id.user_id',
                              store=True,
                              readonly=True)

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    price = fields.Monetary(string="Price", currency_field='currency_id')
    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                string='Company',
                                related='project_id.company_id',
                                store = True,
                                readonly = True)