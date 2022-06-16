from odoo import models, fields, api


class logRecord(models.Model):
    _name = "log.record"

    description = fields.Text()
    patient_id = fields.Many2one("hms.patient")
