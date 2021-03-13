from pony.orm import Database, Json, Required

from settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """user state inside scenario"""
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """registration application"""
    dep_city = Required(str)
    dest_city = Required(str)
    date = Required(str)
    tickets = Required(str)
    commentary = Required(str)
    telephone = Required(str)


db.generate_mapping(create_tables=True)
