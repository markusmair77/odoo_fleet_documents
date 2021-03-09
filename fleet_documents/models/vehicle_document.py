from odoo import models, fields, api
from datetime import timedelta


class VehicleDocument(models.Model):
    _name = 'vehicle.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vehicle Document"
    active = fields.Boolean(default=True)
    name = fields.Char(string='Doc. Number', required=True, tracking=True)

    kept_by = fields.Selection([
        ('vehicle', 'Vehicle'),
        ('company', 'The Company')], required=True, default='vehicle', string='Kept by', tracking=True)
    user_id = fields.Many2one('res.users', string='Document Manager', required=True, default=lambda self: self.env.user,
                              tracking=True, help="The one in your"
                              " HR Department that takes responsibility for managing this document")
    type_id = fields.Many2one('vehicle.document.type', string="Document Type", required=True, ondelete='restrict')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True, ondelete='cascade', tracking=True)
    company_id = fields.Many2one(related='vehicle_id.company_id', store=True)
    issue_date = fields.Date(string="Issue Date", tracking=True, help="The date on which this document was issued")
    expire_date = fields.Date(string='Expire Date', tracking=True, help="The date on which this document get expired")
    days_to_notify = fields.Integer(string='Days to Notify', default=0, tracking=True, required=True,
                                    help="The number of days prior to the expire date to notify the employee and the document manager"
                                    " about the expiration. Leave it as zero (0) to disable notification.")
    date_to_notify = fields.Date(string='Date to notify', compute='_compute_date_to_notify', store=True, tracking=True,
                                 help="Technical field that indicated the date on which the notification should be sent.")
    issued_by = fields.Many2one('res.partner', string='Issued By', tracking=True)
    place_of_issue = fields.Char(string="Place of Issue", tracking=True)
    notes = fields.Text(string='Notes')
    pdf = fields.Binary(string='PDF', help="Store the PDF version of the Document")
    image1 = fields.Binary(string='Image 1')
    image2 = fields.Binary(string='Image 2')
    return_upon_termination = fields.Boolean(string='Return Upon Termination', tracking=True,
                                             help="If checked, the original document must be return to its owner."
                                             " I.e. if the origin is kept by the company, it should be returned to the employee;"
                                             " if the origin is kept by the employee, it should be returned to the company")

    has_scanned_doc = fields.Boolean('Has Scanned Document attached', compute='_compute_has_scanned_doc', store=True)

    _sql_constraints = [
        ('vehicle_doc_type_doc_name_uniq',
         'unique(name, type_id, vehicle_id, id)',
         "The document number must be unique per document type per vehicle!"),
    ]

    def name_get(self):
        name = []
        for r in self:
            name.append((r.id, '%s / %s' % (r.type_id.name, r.vehicle_id.name)))
        return name

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('type_id.name', '=ilike', '%' + name + '%'), ('name', operator, name)]
        docs = self.search(domain + args, limit=limit)
        return docs.name_get()

    @api.onchange('issued_by')
    def _onchange_issued_by(self):
        issue_loc = []
        if self.issued_by:
            if self.issued_by.city:
                issue_loc.append(self.issued_by.city)

            if self.issued_by.state_id:
                issue_loc.append(self.issued_by.state_id.name)
            if self.issued_by.country_id:
                issue_loc.append(self.issued_by.country_id.name)
        if issue_loc:
            self.place_of_issue = ', '.join(issue_loc)

    @api.onchange('type_id')
    def _onchage_type_id(self):
        if self.type_id:
            if self.type_id.days_to_notify > 0:
                self.days_to_notify = self.type_id.days_to_notify
            self.kept_by = self.type_id.kept_by
            self.return_upon_termination = self.type_id.return_upon_termination

    @api.depends('pdf')
    def _compute_has_scanned_doc(self):
        for r in self:
            r.has_scanned_doc = True if r.pdf or r.image1 or r.image2 else False

    @api.depends('expire_date', 'days_to_notify')
    def _compute_date_to_notify(self):
        for r in self:
            if r.expire_date and r.days_to_notify > 0:
                r.date_to_notify = r.expire_date - timedelta(days=r.days_to_notify)
            else:
                r.date_to_notify = False

    def cron_notify_expire_vehicle_docs(self):
        today = fields.Date.today()
        to_notify_docs = self.search([('date_to_notify', '<=', today)])
        to_notify_docs.action_send_expiry_notification()

    def action_send_expiry_notification(self):
        for r in self:
            email_template_id = self.env.ref('to_vehicle_documents.email_template_doc_expire_notif')
            r.message_post_with_template(email_template_id.id)

#    @api.model
#    def message_new(self, msg_dict, custom_values=None):
#        """ Overrides mail_thread message_new that is called by the mailgateway
#            through message_process.
#            This override updates the document according to the email.
#        """
#        # remove default author when going through the mail gateway. Indeed we
#        # do not want to explicitly set user_id to False; however we do not
#        # want the gateway user to be responsible if no other responsible is
#        # found.
##        create_context = dict(self.env.context or {})
##        create_context['default_user_id'] = False
#        if custom_values is None:
#            custom_values = {}
#        defaults = {
#            'name': msg_dict.get('message_id') or _("No Subject"),
#            'employee_id': 480,
#            'user_id': 9,
#            'type_id': 50,
#            'active': True,
#            'pdf': msg_dict.get('attachments', [1])
#        }
#        defaults.update(custom_values)
#        e_doc = super(EmployeeDocument, self).message_new(msg_dict, custom_values=defaults)
#        e_doc = super(EmployeeDocument, self).message_new(msg, custom_values=default)
#        followers_obj = p_order.env['mail.followers']
#        follower_id = False
#        reg = {
#                'res_id': e_doc.id,
#                'res_model': 'employee.document',
#                'partner_id': msg.get('author_id'), }
#        try:
#                follower_id = followers_obj.create(reg)
#        except:
#                 _logger.info(u'AddFollower: follower already exists')
#
#        return False

