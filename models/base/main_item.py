from odoo import fields, models 

class AssetItem(models.Model):
    _name = "asset.item"
    _description = "main asset item"

    name = fields.Char()

    asset_ref = fields.Reference(
        selection=[
            ('assets_phone',"Phone / Tablet"),
            ('assets_other',"Other"),
            ('assets_computer',"Computer"),
            ('assets_monitor',"Monitor")
        ],
        string = "Asset"
    )

    inventory_number = fields.Char()
