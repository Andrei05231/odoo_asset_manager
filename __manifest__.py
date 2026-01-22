{
    'name':'Asset Manager',
    'version':'0.6',
    'category':'Administration',
    'description':' App used for mananging computers, printers, phones and other assets',
    'depends': ['base','hr'],
    'data':[
        'views/menu_view.xml',
        'security/ir.model.access.csv',
        'views/computer_views.xml',
        'views/project_views.xml',
        'views/monitor_views.xml',
        'views/software_views.xml',
        'views/license_views.xml',
        'views/history_views.xml',
        'views/printer_views.xml',
        'views/other_views.xml',
        'views/inventory_views.xml',
        'views/phone_tablet_views.xml',
        'views/tag_views.xml',
        'views/score_views.xml',
        'views/computer_category_views.xml'
        ],
    'installable':True,
    'application':True,
    'auto_install':False,
        
}
