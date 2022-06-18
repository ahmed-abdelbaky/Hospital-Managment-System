import base64
import re
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource


class hmsPatient(models.Model):
    _name = "hms.patient"

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    CR_Ratio = fields.Float()
    Blood_type = fields.Selection(
        [("O", "O"), ("A+", "A+"), ("O+", "O+")]
    )
    PCR = fields.Boolean()
    Image = fields.Image(default=_default_image)
    Address = fields.Text()
    Age = fields.Integer(compute="compute_age")
    doctor_ids = fields.Many2many("hms.doctors")
    department_id = fields.Many2one("hms.department")
    department_capacity = fields.Integer(related="department_id.Capacity")
    new_registration_history = fields.One2many("log.record", "patient_id")
    state = fields.Selection(
        [
            ("Undetermined", "Undetermined"),
            ("Good", "Good"),
            ("Fair", "Fair"),
            ("Serious", "Serious")
        ]
    )

    def create_log_registration(self):
        self.env["log.record"].create(
            {
                "description": f"new registration states {self.state}",
                "patient_id": self.id
            }
        )

    @api.depends("birth_date")
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                # print("date", rec.birth_date, date.today())
                rec.Age = int((date.today() - rec.birth_date).days) // 365
                # print("age ", rec.Age)
            else:
                rec.Age = 0

    def check_email(self, vals):
        regex = r'\b([a-zA-Z0-9/./_/-]+)@([a-zA-Z0-9/./_/-]+)'
        if vals.get('email', False):
            if re.fullmatch(regex, vals['email']):
                pass
            else:
                raise UserError("invalid email")

    _sql_constraints = [
        ("unique", "unique(email)", "this is email already existed")
    ]

    @api.model
    def create(self, vals):
        self.check_email(vals)

        return super().create(vals)

    def write(self, vals):
        for record in self:
            record.check_email(vals)

        return super().write(vals)

    def state_undetermined(self):
        self.state = "Undetermined"
        self.create_log_registration()

    def state_good(self):
        self.state = "Good"
        self.create_log_registration()

    def state_fair(self):
        self.state = "Fair"
        self.create_log_registration()

    def state_serious(self):
        self.state = "Serious"
        self.create_log_registration()

    @api.onchange("Age")
    def pcr_check(self):
        if self.Age < 30:
            self.PCR = True
        return {
            'warning': {
                'title': 'Warning',
                'message': "PCR has been check"
            }

        }

