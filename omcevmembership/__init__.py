from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from omcevmembership.models import initialize_sql
from pyramid_beaker import session_factory_from_settings


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          session_factory=session_factory)
    config.add_translation_dirs('omcevmembership:locale/')
    config.add_static_view('static',
                           'omcevmembership:static', cache_max_age=3600)

    config.add_subscriber('omcevmembership.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    # home /
    config.add_route('home', '/')
    config.add_view('omcevmembership.views.home_view',
                    route_name='home',
                    renderer='templates/home.pt')
    # /why
    config.add_route('why', '/why')
    config.add_view('omcevmembership.views.why_view',
                    route_name='why',
                    renderer='templates/why.pt')
    # /types
    config.add_route('types', '/types')
    config.add_view('omcevmembership.views.types_view',
                    route_name='types',
                    renderer='templates/membership_types.pt')

    # beitrittserklaerung
    config.add_route('beitrittserklaerung', '/beitrittserklaerung')
    config.add_view('omcevmembership.views.join_membership',
                    route_name='beitrittserklaerung',
                    renderer='templates/join.pt')
    return config.make_wsgi_app()
