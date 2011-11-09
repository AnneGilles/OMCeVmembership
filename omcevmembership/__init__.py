from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from omcevmembership.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'omcevmembership:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_view('omcevmembership.views.my_view',
                    route_name='home',
                    renderer='templates/mytemplate.pt')
    # beitrittserklaerung
    config.add_route('beitrittserklaerung', '/beitrittserklaerung')
    config.add_view('omcevmembership.views.join_membership',
                    route_name='beitrittserklaerung',
                    renderer='templates/join.pt')
    return config.make_wsgi_app()

