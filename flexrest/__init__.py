from .api.rest_api import RestApiHandler, RestApiResource


class FlexRestManager(object):
    def __init__(self, db_base, db_session_callback, strict_slash=False,
                 app=None):
        self.db_session_callback = db_session_callback
        self.db_base = db_base
        self.strict_slash = strict_slash
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''
        Configures an application. This registers an `after_request` call, and
        attaches this `LoginManager` to it as `app.login_manager`.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        :param add_context_processor: Whether to add a context processor to
            the app that adds a `current_user` variable to the template.
            Defaults to ``True``.
        :type add_context_processor: bool
        '''
        app.flexrest_manager = self
        app.url_map.strict_slashes = self.strict_slash

__all__ = [RestApiHandler, RestApiResource, FlexRestManager]
