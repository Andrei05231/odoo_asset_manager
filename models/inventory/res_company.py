from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    code = fields.Char(
        string="Company Code",
        required=False
    )
