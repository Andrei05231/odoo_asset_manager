from odoo import models, fields

class Software(models.Model):
    _name = "assets_software"

    name = fields.Char()
    computer_id = fields.Many2many("assets_computer", string="Installed On")
    license_id = fields.One2many("assets_license", 'software_id',string="Licenses")