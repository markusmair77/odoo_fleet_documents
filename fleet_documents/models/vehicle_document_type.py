from odoo import models, fields


class VehicleDocumentType(models.Model):
    _name = 'vehicle.document.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Vehicle Document Type"

    name = fields.Char(string='Name', required=True, translate=True)
    type = fields.Selection([
        ('proof_ownership', 'Proof of ownership'),
        ('proof_insurance', 'Proof of insurance cover'),
        ('others', 'Others')], required=True, index=True, string='Type')
    description = fields.Text(string='Description')
    days_to_notify = fields.Integer(string='Days to Notify', default=7, tracking=True, required=True,
                                    help="The default number of days for documents of this type to raise a notification"
                                    " before they get expired")
    kept_by = fields.Selection([
        ('vehicle', 'Vehicle'),
        ('company', 'The Company')], required=True, default='vehicle', string='Kept by')
    return_upon_termination = fields.Boolean(string='Return Upon Termination', tracking=True,
                                             help="The default value for the documents of this type to indicate if the"
                                             " origin of the document should be return to its owner upon termination")
