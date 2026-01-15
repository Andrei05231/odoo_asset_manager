from odoo import fields, models

class ComponentScore(models.Model):
    _name = "assets_component_score"

    name = fields.Char()
    score = fields.Float()

    component_type = fields.Selection([
        ('gpu',"GPU"),
        ('cpu',"CPU")
    ],
        string = "Type")