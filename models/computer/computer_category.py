from odoo import fields, models

class ComputerCategory(models.Model):
    _name = "assets_score_category"
    _description = "category that will be used to alter the computer score"

    name = fields.Char()
    
    cpu_weight = fields.Float()
    gpu_weight = fields.Float()
    ram_weight = fields.Float()

    max_cpu_score = fields.Float()
    max_gpu_score = fields.Float()