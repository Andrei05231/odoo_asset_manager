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
            ('assets_phone', "Phone / Tablet"),
            ('assets_other', "Other"),
            ('assets_computer', "Computer"),
            ('assets_monitor', "Monitor"),
            ('assets_printer', "Printer"),
            ('assets.furniture', "Furniture"),
            ('assets.server', "Server"),
            ('assets_license', "Software License"),
            ('assets.car',"Vehicle/Car"),
        ],
        string="Asset",
    )

    number = fields.Integer(
        string="Number",
        required=True,
        readonly=True
    )

    code = fields.Char(
        string="Inventory Code",
        compute='_compute_code',
        store=True
    )

    date = fields.Date(
        string="Data Achizitie"
    )
    
    user_id = fields.Many2one(
        'hr.employee', 
        string="Asset User",
        readonly=True,
        store=True,
        help="The user assigned to the asset at the time of registry."
    )

    asset_type = fields.Selection([
        ('assets_phone', "Phone / Tablet"),
        ('assets_other', "Other"),
        ('assets_computer', "Computer"),
        ('assets_monitor', "Monitor"),
        ('assets_printer', "Printer"),
        ('assets.furniture', "Furniture"),
        ('assets.server', "Server"),
        ('assets_license', "Software License"),
         ('assets.car',"Vehicle/Car",)
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

            company_code = rec.company_id.code or ""

            # number padded to 5 digits
            number_str = str(rec.number).zfill(5)

            date_str = rec.date.strftime("%y%m%d") if rec.date else ""

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # If 'number' is 0 or missing, generate the next one
            if not vals.get('number'):
                company_id = vals.get('company_id') or self.env.company.id
                vals['number'] = self._get_next_inventory_number(company_id)
        return super(AssetInventoryNumber, self).create(vals_list)

    def _get_next_inventory_number(self, company_id):
        """ Internal helper to get the next number with a row lock """
        self.env.cr.execute("""
            SELECT number
            FROM asset_inventory_number
            WHERE company_id = %s
            ORDER BY number DESC
            LIMIT 1
            FOR UPDATE
        """, (company_id,))
        
        row = self.env.cr.fetchone()
        return (row[0] if row else 0) + 1
    

    @api.model
    def generate_next(self, asset): 
        """
        Generates/Retrieves inventory number.
        Safely handles missing projects, missing users, or models 
        that don't have those fields at all.
        """
        if not asset:
            return False

        if asset.company_id:
            asset_company = asset.company_id.id
        else:
            asset_company = asset.user_id.company_id.id

        # 1. Check for existing record
        existing = self.search([
            ('asset_ref', '=', f"{asset._name},{asset.id}"),
            ('company_id', '=', asset_company)
        ], limit=1)
        
        if existing:
            return existing

        # 2. Concurrency Lock for sequence
        self.env.cr.execute("""
            SELECT number FROM asset_inventory_number
            WHERE company_id = %s
            ORDER BY number DESC LIMIT 1
            FOR UPDATE
        """, (asset_company,))

        row = self.env.cr.fetchone()
        next_number = (row[0] if row else 0) + 1

        # 3. Safe Data Extraction
        # getattr(object, 'field_name', default) prevents crashes if field is missing
        
        # Project Date logic
        project = getattr(asset, 'project_id', False)
        
        #inv_date = project.date if project and hasattr(project, 'date') else False

        if  project and hasattr(project, 'date'):
            inv_date = project.date
        elif hasattr(asset, "asset_date") :
            inv_date = getattr(asset, "asset_date", False)
        else:
            inv_date = False
            
        # User logic: Get user_id.id if it exists, else False
        # Note: getattr(asset, 'user_id', False) returns the recordset or False
        asset_user = getattr(asset, 'user_id', False)
        inv_user_id = asset_user.id if asset_user else False

        # 4. Create the Registry Record
        return self.create({
            'company_id': asset_company,
            'number': next_number,
            'asset_ref': f"{asset._name},{asset.id}",
            'date': inv_date,
            'user_id': inv_user_id,
        })
