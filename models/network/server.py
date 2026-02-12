from odoo import fields, models 

class Server(models.Model):
    _name = "assets.server"
    _description = "Server related asset"

    name = fields.Char()
    details = fields.Text()

    usage = fields.Char()

