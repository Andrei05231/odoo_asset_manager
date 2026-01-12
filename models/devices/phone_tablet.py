from odoo import models, fields

class AssetPhone(models.Model):
    _name="assets_phone"
    _inherit = ['assets_inventory_mixin']

    name = fields.Char()
    model = fields.Char()

    phone_number = fields.Char()
    details = fields.Text()

    serial = fields.Char()
    inventory_code = fields.Char(
        string="Inventory Code",
        related='inventory_number_id.code',
        readonly=True,
        store=True
    )

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

    asset_status = fields.Selection([
        ('odered',"Ordered"),
        ('arrived',"Arrived"),
        ('active', "Active")
    ],
        string="Asset Status")

