# -*- encoding:utf-8 -*-
'''
Created on Jul 7, 2014

@author: gsc
'''

from osv import osv, fields

class attendee_memory(osv.osv_memory):
    _name = 'openacademy.attendee.memory'
    
    _columns = {
                'name' : fields.char('Name', 64),
                'partner_id' : fields.many2one('res.partner', 'Partner', required=True),
                'wiz_id' : fields.many2one('openacademy.create.attendee.wizard',),
                } 
attendee_memory()

class create_attendee_wizard(osv.osv_memory):
    _name = 'openacademy.create.attendee.wizard'
    
    _columns = {
                'session_id' : fields.many2one('openacademy.session', 'Session', required=True, ondelete='cascade'),
                'attendee_ids': fields.one2many('openacademy.attendee', 'session_id', 'Attendees')
                }

    def action_add_attendee(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        attendee_pool = self.pool.get('openacademy.attendee')
        for attendee in wizard.attendee_ids:
            attendee_pool.create(cr, uid, {'name':attendee.name,
                                    'partner_id':attendee.partner_id.id,
                                    'session_id':wizard.session_id.id})
        return {}   

  

