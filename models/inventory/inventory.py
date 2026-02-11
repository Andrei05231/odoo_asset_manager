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

    asset_ref = fields.Reference(
        selection=[
            ('assets_phone',"Phone / Tablet"),
            ('assets_other',"Other"),
            ('assets_computer',"Computer"),
            ('assets_monitor',"Monitor")
        ],
        string="Asset",
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

    date = fields.Date(
        string="Data Achizitie"
    )

    asset_type = fields.Selection([
        ('assets_phone', "Phone / Tablet"),
        ('assets_other', "Other"),
        ('assets_computer', "Computer"),
        ('assets_monitor', "Monitor")
    ], string="Asset Type", compute="_compute_asset_type", store=True)

    @api.depends('asset_ref')
    def _compute_asset_type(self):
        for rec in self:
            if rec.asset_ref:
                # Extracts 'assets_phone' from 'assets_phone,14'
                rec.asset_type = rec.asset_ref._name if hasattr(rec.asset_ref, '_name') else rec.asset_ref.split(',')[0]
            else:
                rec.asset_type = False
        _sql_constraints = [
            (
                'unique_company_number',
                'unique(company_id, number)',
                'Inventory number must be unique per company.'
            )
        ]

    # -------------------------
    # COMPUTE INVENTORY CODE
    # -------------------------
    @api.depends('company_id', 'number', 'date', 'asset_ref')
    def _compute_code(self):
        for rec in self:
            if not rec.company_id or not rec.number:
                rec.code = False
                continue

            # company code
            company_code = rec.company_id.code or ""

            # number padded to 5 digits
            number_str = str(rec.number).zfill(5)

            # date
            date_str = rec.date.strftime("%Y%m%d") if rec.date else ""

            # finance project from reference
            finance_code = ""
            if rec.asset_ref:
                asset = rec.asset_ref  # this is a recordset
                if hasattr(asset, "project_id") and asset.project_id:
                    # use code if exists, otherwise name
                    finance_code = getattr(asset.project_id, "code", False) \
                                   or asset.project_id.name \
                                   or ""

            # build final code
            parts = [company_code, number_str]

            if date_str:
                parts.append(date_str)

            if finance_code:
                parts.append(finance_code)

            rec.code = "_".join(parts)

    # -------------------------
    # GENERATE NEXT NUMBER
    # -------------------------
    @api.model
    def generate_next(self, company, asset_ref=None, date=None):
        """
        Generate next sequential number per company
        Safe for concurrency
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
        next_number = (row[0] if row else 0) + 1

        return self.create({
            'company_id': company.id,
            'number': next_number,
            'asset_ref': asset_ref,
            'date': date,
        })

