from odoo import models, fields

class Computer(models.Model):
    _name="assets_computer"
    
    name = fields.Char()
    is_used = fields.Boolean()
    inventoryNumber = fields.Char()
    serialNumber = fields.Char()
    user = fields.Many2one('hr.employee', string="Assigned User")
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



