from odoo import models, fields, api
from odoo.exceptions import UserError


class hmsCustomer(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one("hms.patient")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError("you can't delete this Customer")
        super().unlink()

    _sql_constraints = [
        ("unique", "unique(email)", "email is already exist ")
    ]

    @api.constrains('email')
    def chk_email(self):
        for rec in self:
            email_search = rec.env['hms.patient'].search_count([("email", "=", rec.email)])
            if email_search:
                raise UserError("this is email already exist in patient models")


