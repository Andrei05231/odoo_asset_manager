from odoo import fields, models 
from datetime import timedelta

class CarAsset(models.Model):
    _name = "assets.car"
    _description = "Track Company Cars"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Masina", required=True)
    license_plate = fields.Char(string="Nr. Inmatriculare")
    driver = fields.Many2one('hr.employee', string="Responsabil", tracking=True)
    
    rca_expire = fields.Date(string="Data expirare RCA", tracking=True)
    itp_expire = fields.Date(string="Data expirare ITP", tracking=True)
    rovinieta_expire = fields.Date(string="Data expirare Rovinieta ", tracking=True)
    leasing_expire = fields.Date(string="Data expirare Leasing", tracking=True)
    casco_expire = fields.Date(string="Data expirare Casco", tracking=True)
    revizie_expire = fields.Date(string="Data expirare Revizie Tehnica", tracking=True)

    has_casco = fields.Boolean(string="Casco")
    has_leasing = fields.Boolean(string="Leasing")

    REMINDER_RULES = {
        'rca_expire': [30, 7],
        'itp_expire': [30, 5],
        'rovinieta_expire': [20, 3],
        'leasing_expire': [60, 15],
        'casco_expire': [30, 10],
        'revizie_expire': [15, 3],
    }

    STATIC_EMAILS = [
        'andrei.carare@artehnis.ro',
    ]

    def create(self, vals):
        record = super().create(vals)
        record.message_post(body="Car asset created.")
        return record
    
    def _cron_send_expiry_reminders(self):
        today = fields.Date.today()
        template = self.env.ref('odoo_asset_manager.email_car_expiry_reminder')

        cars = self.search([])

        for car in cars:
            for field_name, days_list in self.REMINDER_RULES.items():
                expire_date = getattr(car, field_name)
                if not expire_date:
                    continue

                for days in days_list:
                    if expire_date == today + timedelta(days=days):
                        recipients = []

                        if car.driver and car.driver.work_email:
                            recipients.append(car.driver.work_email)

                        recipients += self.STATIC_EMAILS

                        template.with_context(
                            days=days,
                            label=car._fields[field_name].string,
                            expire_date=expire_date,
                        ).send_mail(
                            car.id,
                            email_values={
                                'email_to': ','.join(set(recipients)),
                            },
                            force_send=True,
                        )