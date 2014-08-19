# -*- coding: utf-8 -*-
from osv import orm, fields


class Course(orm.BaseModel):
    _name = "openacademy.course"
    _description = "Open Academy Course"

    _columns = {
        'name': fields.char('Course Title', 128, required=True),
        'description': fields.text('Description'),
    }

Course()
