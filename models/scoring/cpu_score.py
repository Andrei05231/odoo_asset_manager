from odoo import fields, models

class CpuScore(models.Model):
    _name = "assets_cpu_score"
    _inherit = ["assets_score_mixins"]