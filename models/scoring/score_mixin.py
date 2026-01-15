from odoo import fields, models

class ScoreMixin(models.AbstractModel):
    _name = "assets_score_mixin"

    name = fields.Char()
    score = fields.Integer()