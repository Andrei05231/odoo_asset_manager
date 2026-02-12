from odoo import fields, models 

class Furniture(models.Model):
    _name = "assets.furniture"
    _description = "Furniture stuff"

    name = fields.Char()

    furniture_type = fields.Char()

    details = fields.Text()


