# __openerp__.py
# Nicolas Trubert
{
'name': "Yotech Tools",
'description': "Yotech Generic tools",
'author':'Nicolas Trubert',
'category': 'Hidden',
'depends': ['web','website_sale','stock'],
'css': ['static/src/css/yotech.css'],
'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/templates.xml'
],
'active':True,
'auto_install':False,
}
