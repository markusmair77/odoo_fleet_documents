from odoo import fields, models


class Vehicle(models.Model):
    _inherit = 'fleet.vehicle'

    document_ids = fields.One2many('vehicle.document', 'vehicle_id', string='Fahrzeufdokumente')
    document_count = fields.Integer(string="Vehicle Document counts", compute='_compute_document_count')

    def _compute_document_count(self):
        docs_data = self.env['vehicle.document'].read_group([('vehicle_id', 'in', self.ids)], ['vehicle_id'], ['vehicle_id'])
        mapped_data = dict([(dict_data['vehicle_id'][0], dict_data['vehicle_id_count']) for dict_data in docs_data])
        for r in self:
            r.document_count = mapped_data.get(r.id, 0)
