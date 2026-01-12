from odoo import models, fields

class AssetPhone(models.Model):
    _name="assets_phone"
    _inherit = ['assets_mixin']

    
    model = fields.Char()

    phone_number = fields.Char()

    serial = fields.Char()

    user_id = fields.Many2one('hr.employee', string="Assigned User")
    department_id = fields.Many2one('hr.department', string="Department", related='user_id.department_id', store=True, readonly=True)
    
    device_type = fields.Selection([
        ('phone', "Phone"),
        ('tables', "Tablet")
    ], string = "Type")

