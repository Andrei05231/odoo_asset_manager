from odoo import fields, models

class GpuScore(models.Model):
    _name = "assets_gpu_score"
    _inherit = ["assets_score_mixin"]
