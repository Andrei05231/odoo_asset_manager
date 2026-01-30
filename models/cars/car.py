from odoo import fields, models 

class CarAsset(models.Model):
    _name = "assets.car"
    _description = "Track Company Cars"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Masina", required=True)
    license_plate = fields.Char(string="Nr. Inmatriculare")
    driver = fields.Many2one('hr.employee', string="Responsabil", tracking=True)
    
    rca_expire = fields.Date(string="Data expirare RCA", tracking=True)
    itp_expire = fields.Date(string="Data expirare ", tracking=True)
    rovinieta_expire = fields.Date(string="Data expirare Rovinieta ", tracking=True)
    leasing_expire = fields.Date(string="Data expirare Leasing", tracking=True)
    casco_expire = fields.Date(string="Data expirare Casco", tracking=True)
    revizie_expire = fields.Date(string="Data expirare Revizie Tehnica", tracking=True)

    casco = fields.boolean(string="Casco")
    leasing = fields.boolean(string="Leasing")

    def create(self, vals):
        record = super().create(vals)
        record.message_post(body="Car asset created.")
        return record