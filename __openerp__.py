{
    "name":"Open Academy",
    "depends":["base"],
    "author":"Gabriel Schwanen",
    "data":[
        "openacademy_view.xml",
        "partner_view.xml",
        "security/groups.xml",
        "security/ir.model.access.csv",
        "wizard/create_attendee_view.xml",
    ],
    'test': [
        'test/test_runbot.yml',
    ],
    "installable":True,
    "application":True,
    "active":False,
}