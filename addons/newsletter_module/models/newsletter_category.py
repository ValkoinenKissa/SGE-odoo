from odoo import models, fields, api, _
class NewsletterCategory(models.Model):
   _name = 'newsletter.category'
   _description = 'Newsletter Category'
   name = fields.Char(string='Name', required=True)
   code = fields.Char(string='Code')
   subscription_ids = fields.One2many('newsletter.subscription',
                                      'category_id', string='Subscriptions')
   subscriber_count = fields.Integer(string='Subscriber Count',
                                     compute='_compute_subscriber_count')
   @api.depends('subscription_ids')
   def _compute_subscriber_count(self):
       for category in self:
           category.subscriber_count = len(category.subscription_ids)
