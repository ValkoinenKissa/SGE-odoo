{
    'name': 'Custom Newsletter',
    'version': '18.0.1.0.0',
    'summary': 'Newsletter Subscription Management System',
    'description': """
        Comprehensive newsletter management module for Odoo 18
        =====================================================
        Features:
        - Subscriber management with email validation
        - Category organization
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'category': 'Marketing/Email Marketing',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/newsletter_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
