{
    'name': 'Open Academy',
    'depends': ['base', ],
    'author': 'Gabriel Schwanen',
    'description': """
    Open Academy module for managing trainings:
    - training courses
    - training sessions
    - attendees registration
    """,
    'data': ['openacademy_view.xml', 'security/ir.model.access.csv', ],
    'test': ['test/test_course_name.yml', ],
    'installable': True,
    'application': True,
    'active': False,
}
