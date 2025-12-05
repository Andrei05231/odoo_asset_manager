{

    'name':'Asset Manager',
    'version':'0.1',
    'category':'Administration',
    'description':' App used for mananging computers, printers, phones and other assets',
    'depends': ['base','hr'],
    'data':[
        'views/menu_view.xml',
        'security/ir.model.access.csv',
        'views/computer_views.xml',
        'views/project_views.xml',
        'views/monitor_views.xml',
        ],
    'installable':True,
    'application':True,
    'auto_install':False,
        
}
