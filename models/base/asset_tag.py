from odoo import fields, models
from random import randint

class AssetTag(models.Model):
    _name="assets_tag"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name')
    color = fields.Integer(string='Color', default=_get_default_color,
        help="Transparent tags are not visible in the kanban view of your projects and tasks.")