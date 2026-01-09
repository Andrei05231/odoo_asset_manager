from odoo import models, fields, api

class AssetInventoryNumber(models.Model):
    _name = 'asset.inventory.number'
    _description = 'Asset Inventory Number Registry'
    _order = 'id desc'

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        index=True
    )

    number = fields.Integer(
        string="Number",
        required=True
    )

    code = fields.Char(
        string="Inventory Code",
        compute='_compute_code',
        store=True
    )

    _sql_constraints = [
        (
            'unique_company_number',
            'unique(company_id, number)',
            'Inventory number must be unique per company.'
        )
    ]

    @api.depends('company_id', 'number')
    def _compute_code(self):
        for rec in self:
            rec.code = f"{rec.company_id.code} {rec.number}"

    @api.model
    def generate_next(self, company):
        """
        Generate the next inventory number for a company
        Uses database locking to prevent duplicates
        """

        self.env.cr.execute("""
            SELECT number
            FROM asset_inventory_number
            WHERE company_id = %s
            ORDER BY number DESC
            LIMIT 1
            FOR UPDATE
        """, (company.id,))

        row = self.env.cr.fetchone()
        next_number = (row[0] if row else 2000) + 1

        return self.create({
            'company_id': company.id,
            'number': next_number,
        })
