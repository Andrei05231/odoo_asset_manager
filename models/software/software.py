from odoo import models, fields

class Software(models.Model):
    _name = "assets_software"

    name = fields.Char()
    computer_id = fields.Many2many("assets_computer", string="Installed On")
    license_id = fields.Many2one("assets_license", string="Licenses")