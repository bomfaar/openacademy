# -*- coding:utf-8 -*-

from osv import orm
from osv import fields

class Course(orm.BaseModel):
    _name = 'openacademy.course'
    _description = 'Open Academy Course'


    # Exo 4
    def _check_description(self, cr, uid, ids, context=None):
        courses = self.browse(cr, uid, ids, context=context)
        check = True
        for course in courses:
            if course.name == course.description:
                return False
        return check

    _constraints = [(_check_description,
                     'Please use a different description',
                     ['name', 'description'])]
    # Exo 5
    _sql_constraints = [('unique_name', 'unique(name)', 'Course Title must be unique')]
    
    # Exo 6
    def copy(self, cr, uid, ids, defaults, context=None):
        previous_name = self.browse(cr, uid, ids, context=context).name
        new_name = 'Copy of %s' % previous_name
        lst = self.search(cr, uid, [('name', 'like', new_name)], context=context)
        if len(lst) > 0:
            new_name = '%s (%s)' % (new_name, len(lst))
        defaults['name'] = new_name
        return super(Course, self).copy(cr, uid, ids, defaults, context=context)


    # Exo 5 - Graph View
    
    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for course in self.browse(cr, uid, ids, context=context):
            num = 0
            for session in course.session_ids:
                num += len(session.attendee_ids)
                res[course.id] = num
        return res

    _columns = {
        'name' : fields.char('Course Title', 128, required=True),
        'responsible_id' : fields.many2one('res.users', string='Responsible', ondelete='set null'),
        'description' : fields.text('Description'),
        'session_ids' : fields.one2many('openacademy.session', 'course_id', 'Session'),
        'attendee_count': fields.function(_get_attendee_count, type='integer', 
                                          string='attendee Count', method=True),
        }
    
Course()


class Session(orm.BaseModel):
    _name = 'openacademy.session'
    _description = 'Open Academy Session'
    
    def _get_remaining_seats_percent(self, seats, attendee_lst):
        return seats and (100.0 * (seats - len(attendee_lst))) / seats or 0
        # return (100.0*(seats - len(attendee_lst)))/seats if seat else 0
        
    def _remaining_seats_percent(self, cr, uid, ids, field, arg, context=None):
        sessions = self.browse(cr, uid, ids, context=None)
        result = {}
        for session in sessions :
            result[session.id] = self._get_remaining_seats_percent(session.seats, session.attendee_ids)
        return result
        
        
    def onchange_remaining_seats(self, cr, uid, ids, seats, attendee_ids):
        res = {
               'value': {
                         'remaining_seats_percent' : self._get_remaining_seats_percent(seats, attendee_ids)
                         }
               }
        
        if seats < 0:
            res['warning'] = {
                              'title' : 'Warning',
                              'message' : 'You cannot have negative seats',
                              } 
        return res  


    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = len(session.attendee_ids)
        return res

    _columns = {
        'name' : fields.char('Session Title', 128, required=True),
        'start_date' : fields.date('Start Date'),
        'duration' : fields.float('Duration', digits=(6, 2), help='Duration in days'),
        'seats' : fields.integer('Number of seat'),
        'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', 'Attendees'),
        'remaining_seats_percent':fields.function(_remaining_seats_percent,
                                                  method=True, type='float',
                                                  string="Remaining seats"),
        'instructor_id': fields.many2one('res.partner', 'Instructor'),
        'course_id': fields.many2one('openacademy.course', 'Course', required=True, ondelete='cascade'),
        'active': fields.boolean('Active'),
        'attendee_count': fields.function(_get_attendee_count,
                                          type='integer', string='Attendee Count',
                                          method=True),
    }
    
    _defaults = {
                 'start_date': fields.date.context_today,
                 'active':True,
                 }


Session()

class Attendee(orm.BaseModel):
    _name = 'openacademy.attendee'
    _rec_name = 'partner_id'

    _columns = {
        'partner_id' : fields.many2one('res.partner', 'Partner', required=True, ondelete='cascade'),
        'session_id' : fields.many2one('openacademy.session', 'Session', required=True, ondelete='cascade'),
    }

Attendee()
