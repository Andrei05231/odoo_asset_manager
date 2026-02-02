from . import models

def post_load():
    """Create cron job after module loads"""
    import odoo
    from odoo import api, SUPERUSER_ID
    
    for db_name in odoo.service.db.list_dbs():
        try:
            registry = odoo.registry(db_name)
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                
                # Check if our module is installed
                module = env['ir.module.module'].search([
                    ('name', '=', 'odoo_asset_manager'),
                    ('state', '=', 'installed')
                ], limit=1)
                
                if not module:
                    continue
                
                # Check if cron already exists
                cron = env['ir.cron'].search([
                    ('name', '=', 'Car Expiry Reminders'),
                ], limit=1)
                
                if not cron:
                    env['ir.cron'].create({
                        'name': 'Car Expiry Reminders',
                        'model_id': env.ref('odoo_asset_manager.model_assets_car').id,
                        'state': 'code',
                        'code': 'model._cron_send_expiry_reminders()',
                        'interval_number': 1,
                        'interval_type': 'days',
                        'numbercall': -1,
                        'active': True,
                    })
                    cr.commit()
                    print("✓ Car Expiry Reminders cron job created")
        except:
            pass