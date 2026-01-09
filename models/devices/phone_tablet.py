from odoo import models, fields

class AssetPhone(models.Model):
    __name__="assets.phone"

    name = fields.Char()
    model = fields.Char()

    phone_number = fields.Char()
    details = fields.Text()

    inventory = fields.Char()
    serial = fields.Char()

    user_id = fields.Many2one('hr.employee', string="Assigned User")
    department_id = fields.Many2one('hr.department', string="Department", related='user_id.department_id', store=True, readonly=True)

    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                string='Company',
                                related='project_id.company_id',
                                store = True,
                                readonly = True)
    
    device_type = fields.Selection([
        ('phone', "Phone"),
        ('tables', "Tablet")
    ], string = "Type")

