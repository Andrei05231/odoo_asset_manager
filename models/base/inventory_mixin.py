from odoo import models, fields
from odoo.exceptions import UserError

import re
import logging

_logger = logging.getLogger(__name__)

class InventoryNumberMixin(models.AbstractModel):
    _name = "assets_inventory_mixin"

    inventory_number_id = fields.Many2one(
        'asset.inventory.number',
        string="Inventory",
        readonly=True
    )
    
    inventory_code = fields.Char(
        string="Inventory Code",
        related='inventory_number_id.code',
        readonly=True,
        store=True
    )

    def action_generate_inventory_number(self):
            for asset in self:
                # Skip if already assigned
                if asset.inventory_number_id:
                    continue

                if not asset.company_id:
                    raise UserError('Please set the company before generating an inventory number.')
                
                # Pass 'self' (the current asset record) to the registry
                inventory_rec = self.env['asset.inventory.number'].generate_next(asset)
                
                # Link the new (or existing) registry record back to the asset
                asset.inventory_number_id = inventory_rec.id

    def migrate_inventory_numbers(self):
        Inventory = self.env['asset.inventory.number']

        assets = self.search([
            ('inventory', '!=', False),
            ('inventory_number_id', '=', False),
            ('company_id', '!=', False),
        ])

        _logger.info("Starting inventory migration: %s assets found", len(assets))

        for asset in assets:
            _logger.info(
                "Processing asset ID=%s inventory='%s' company_id=%s",
                asset.id,
                asset.inventory,
                asset.company_id.id if asset.company_id else None,
            )

            match = re.search(r'(\d+)', asset.inventory or '')
            if not match:
                _logger.warning(
                    "NO MATCH for asset ID=%s inventory='%s'",
                    asset.id, asset.inventory
                )
                continue

            number = int(match.group(1))
            _logger.info("Extracted number=%s for asset ID=%s", number, asset.id)

            inventory_number = Inventory.search([
                ('company_id', '=', asset.company_id.id),
                ('number', '=', number),
            ], limit=1)

            _logger.info(
                "Existing inventory_number found=%s",
                bool(inventory_number)
            )

            if not inventory_number:
                inventory_number = Inventory.create({
                    'company_id': asset.company_id.id,
                    'number': number,
                })
                _logger.info(
                    "CREATED inventory_number ID=%s number=%s",
                    inventory_number.id,
                    number,
                )

            _logger.info(
                "Writing inventory_number_id=%s to asset ID=%s",
                inventory_number.id,
                asset.id,
            )

            asset.write({'inventory_number_id': inventory_number.id})

            _logger.info(
                "AFTER WRITE asset.inventory_number_id=%s",
                asset.inventory_number_id.id,
            )

        self.env.cr.commit()
        _logger.info("Inventory migration committed")



