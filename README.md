# Asset Manager - Odoo Module

IT asset management module for Odoo with real-time integration capabilities. Designed to work with asset discovery tools like OCS Inventory.

## Overview

Manage computers, monitors, printers, phones, tablets and other IT equipment across multiple companies. Features automatic inventory numbering, performance benchmarking, and REST API for real-time asset updates.

## Key Features

### Asset Types
- **Computers**: Track specs (CPU/GPU/RAM), performance scores, user assignments
- **Monitors**: Auto-link to computers, inherit user assignments
- **Printers**: Network configuration, status tracking
- **Phones/Tablets**: Device type, phone numbers, user assignments
- **Other Devices**: Flexible model for miscellaneous equipment

### Inventory Management
- Company-specific sequential numbering with prefixes (e.g., "ABC 2001")
- Automatic generation with database locking (prevents duplicates)
- Migration tool for existing inventory data
- Related to projects for financial tracking

### Performance Scoring
- Automated benchmarking based on CPU, GPU, and RAM
- Normalized 0-100 scoring system
- Component score database for CPUs and GPUs
- Batch scoring from list view or individual records
- Smart preprocessing: handles multi-GPU systems, normalizes CPU names

### Real-time Integration
- REST API endpoint for batch updates
- OCS Inventory compatible
- Automatic computer/monitor creation and linking
- Match by serial number or hostname
- Detailed operation summaries

### Additional Features
- Asset lifecycle tracking (Ordered → Arrived → Active)
- Maintenance and upgrade history with expense linking
- Software and license management
- Color-coded tagging system
- Multi-company and multi-project support
- Integration with HR module for employee assignments

## Installation

1. Copy module to Odoo addons directory:
```bash
cp -r asset_manager /path/to/odoo/addons/
```

2. Update apps list and install "Asset Manager"

3. Configure company codes:
   - Go to Settings → Companies
   - Set unique "Company Code" for each company (e.g., "ABC", "XYZ")

4. Populate component scores (optional, for performance scoring):
   - Navigate to Config → Component Scores
   - Add CPU/GPU entries with benchmark scores

## Usage

### Generating Inventory Numbers

1. Open any asset record (Computer, Phone, Other, etc.)
2. Set the Project field (links to Company)
3. Click "Generate" button next to Inventory Code
4. System generates next sequential number: "{CompanyCode} {Number}"

### Computing Performance Scores

1. Ensure Component Scores database is populated
2. Select computers from list view
3. Use Actions → Get Score (batch operation)
4. Or click "Get Score" button in individual computer form

### Recording Asset History

1. Open asset record → History tab
2. Click "Add History"
3. Select type: Maintenance, Upgrade, or Other
4. Add notes and link to expense records if applicable

## API Integration

### Batch Update Endpoint

Update computer specifications from asset discovery tools.

**Endpoint**: `POST /web/dataset/call_kw/assets_computer/batch_update`

**Request Payload**:
```json
{
  "computers": [
    {
      "serialNumber": "ABC123XYZ",
      "name": "WORKSTATION-01",
      "cpu": "11th Gen Intel Core i7-11700 @ 2.50GHz",
      "gpu": "NVIDIA GeForce RTX 3070, Intel UHD Graphics 750",
      "memory": "2x16384",
      "monitors": [
        {
          "name": "Dell U2720Q",
          "serial": "MON123456"
        },
        {
          "name": "Dell P2419H",
          "serial": "MON789012"
        }
      ]
    }
  ]
}
```

**Response**:
```json
{
  "success": true,
  "results": [
    {
      "serialNumber": "ABC123XYZ",
      "name": "WORKSTATION-01",
      "status": "updated",
      "id": 42,
      "matched_by": "serialNumber"
    }
  ],
  "computer_summary": {
    "total": 1,
    "updated": 1,
    "not_found": 0,
    "errors": 0
  },
  "monitor_summary": {
    "status": "completed",
    "already_found": 0,
    "created": 2
  }
}
```

**Behavior**:
- Searches for existing computer by serial number, then by name
- Creates new computer if not found
- Updates only CPU, GPU, and memory fields (preserves other data)
- Automatically creates and links monitors
- Prevents duplicate monitors (checks by serial number)
- Returns detailed status for each operation

**Status Values**:
- `updated`: Computer found and updated
- `created`: New computer created
- `no_updates`: Computer found but no changes needed
- `not_found`: Computer not found and creation failed
- `error`: Operation failed with error details

## Performance Scoring Algorithm

### Calculation
```
score = (0.63 × gpu_normalized) + (0.35 × cpu_normalized) + (0.02 × ram_score)
```

### Normalization
- **GPU**: Score divided by 7000 (max reference), multiplied by 100
- **CPU**: Score divided by 600 (max reference), multiplied by 100
- **RAM**: Logarithmic scaling with diminishing returns above 64GB

### Preprocessing
- **CPU Names**: Removes generation markers ("11th Gen"), trademarks, frequencies
- **Multi-GPU**: Detects discrete GPUs (NVIDIA, Radeon, Arc) from integrated graphics
- **RAM Format**: Parses strings like "2x16384" (2 sticks × 16GB)

### Component Score Database
Maintain benchmark scores in Config → Component Scores:
- Component Type: CPU or GPU
- Name: Normalized component name (as processed by scoring logic)
- Score: Benchmark value (e.g., PassMark score)

## Module Structure

```
asset_manager/
├── models/
│   ├── base/
│   │   ├── asset_mixin.py          # Common fields (name, details, project, status)
│   │   ├── inventory_mixin.py      # Inventory number management
│   │   ├── asset_tag.py            # Tagging system
│   │   └── history.py              # Maintenance/upgrade tracking
│   ├── computer/
│   │   ├── computer.py             # Computer model + batch_update method
│   │   ├── monitor.py              # Monitor model
│   │   └── compute_score.py        # Scoring logic
│   ├── devices/
│   │   ├── printer.py              # Printer management
│   │   ├── phone_tablet.py         # Mobile devices
│   │   └── other.py                # Miscellaneous assets
│   ├── financial/
│   │   └── finance_project.py      # Financing projects (PNRR/ADR/POR/Self)
│   ├── inventory/
│   │   ├── inventory.py            # Inventory number registry
│   │   └── res_company.py          # Company code extension
│   ├── software/
│   │   ├── software.py             # Software catalog
│   │   └── license.py              # License management
│   ├── scoring/
│   │   └── component_score.py      # CPU/GPU benchmark database
│   └── utils/
│       └── computer_helpers.py     # Batch update helper functions
├── views/                           # XML UI definitions
├── security/
│   └── ir.model.access.csv         # Access rights configuration
└── __manifest__.py
```

## Extending the Module

### Creating New Asset Types

Inherit from `assets_mixin` to get common functionality:

```python
from odoo import models, fields

class CustomAsset(models.Model):
    _name = 'custom_asset'
    _inherit = ['assets_mixin']
    
    custom_field = fields.Char(string="Custom Field")
```

This provides: name, details, inventory_code, project_id, company_id, asset_status

### Adding to Batch Update

Modify `models/utils/computer_helpers.py` to extend update logic.

### Custom Scoring Logic

Override or extend `action_compute_score()` in `models/computer/compute_score.py`.

## Data Migration

Migrate existing inventory numbers to the new system:

```python
# Run from Odoo shell or through code
self.env['assets_computer'].migrate_inventory_numbers()
```

Extracts numbers from old inventory strings and creates structured records.

## Technical Details

### Dependencies
- **base**: Odoo core
- **hr**: Human Resources (for employee assignments)

### Database
- PostgreSQL required (uses `FOR UPDATE` locking for inventory generation)
- SQL constraint: unique inventory numbers per company

### Access Rights
Default: all users have full CRUD access
Customize in `security/ir.model.access.csv` as needed

### Inventory Number Generation
Uses database-level locking to prevent race conditions:
```python
self.env.cr.execute("""
    SELECT number FROM asset_inventory_number
    WHERE company_id = %s
    ORDER BY number DESC LIMIT 1
    FOR UPDATE
""", (company.id,))
```

## Version

**0.6** - Current version

## License

Internal use module.