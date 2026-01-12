from odoo import models, fields
from odoo.exceptions import UserError

class InventoryNumberMixin(models.AbstractModel):
    _name = "assets_inventory_mixin"

    inventory_number_id = fields.Many2one(
        'asset.inventory.number',
        string="Inventory",
        readonly=True
    )

    def action_generate_inventory_number(self):
        for asset in self:
            if asset.inventory_number_id:
                continue

            if not asset.company_id:
                raise UserError('Please set the project (company) before generating an inventory number.')
            
            inventory_number = self.env['asset.inventory.number'].generate_next(asset.company_id)

            asset.inventory_number_id = inventory_number.id