from odoo import models, fields


class hmsDepartment(models.Model):
    _name = "hms.department"

    name = fields.Char()
    Capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many("hms.patient", "department_id", string="Patients")
    doctors_id = fields.Many2one("hms.doctors")
