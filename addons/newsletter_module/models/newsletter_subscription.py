from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class NewsletterSubscription(models.Model):
   _name = 'newsletter.subscription'
   _description = 'Newsletter Subscription'
   _inherit = ['mail.thread',
               'mail.activity.mixin']  # For chatter and activities
   name = fields.Char(string='Subscriber Name', required=True, tracking=True)
   email = fields.Char(string='Email', required=True, tracking=True)
   is_active = fields.Boolean(string='Active', default=True, tracking=True)
   subscription_date = fields.Datetime(string='Subscription Date',
                                       default=fields.Datetime.now)
   category_id = fields.Many2one('newsletter.category', string='Category')
   source = fields.Selection([
       ('website', 'Website'),
       ('manual', 'Manual Entry'),
       ('event', 'Event'),
       ('other', 'Other')
   ], string='Source', default='website')
   # SQL constraints for data integrity
   _sql_constraints = [
       ('email_unique', 'UNIQUE(email)', 'Email address must be unique!'),
   ]
   # Python constraints
   @api.constrains('email')
   def _check_email(self):
       for record in self:
           if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', record.email):
               raise ValidationError(_('Please enter a valid email address'))
   # Custom methods
   def action_activate(self):
       self.write({'is_active': True})
   def action_deactivate(self):
       self.write({'is_active': False})
