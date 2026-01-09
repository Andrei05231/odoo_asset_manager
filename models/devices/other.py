from odoo import models, fields
from odoo.exceptions import UserError  # type: ignore

class Other(models.Model):
    _name = "assets_other"

    name = fields.Char(string="Name")
    inventory = fields.Char(string="Inventory Number")

    inventory_number_id = fields.Many2one(
        'asset.inventory.number',
        string="Inventory",
        readonly=True,
        copy=False
    )

    inventory_code = fields.Char(
        string="Inventory Code",
        related='inventory_number_id.code',
        readonly=True,
        store=True
    )


    serial = fields.Char(string="Serial Number")
    project_id = fields.Many2one('assets_project', string="Project")
    company_id = fields.Many2one('res.company',
                                 related='project_id.company_id',
                                 store=True,
                                 readonly=True,
                                 string="Company")
    details = fields.Text(string="Description")

    asset_status = fields.Selection([
        ('odered',"Ordered"),
        ('arrived',"Arrived"),
        ('active', "Active")
    ],
        string="Asset Status")
    
    def action_generate_inventory_number(self):
        """
        Button action:
        - Requires company
        - Generates inventory number ONCE
        """

        for asset in self:
            if asset.inventory_number_id:
                continue

            if not asset.company_id:
                raise UserError(
                    "Please set the project (company) before generating an inventory number."
                )

            inventory_number = self.env['asset.inventory.number'].generate_next(
                asset.company_id
            )

            asset.inventory_number_id = inventory_number.id