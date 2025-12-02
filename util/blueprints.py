import routes

def register_blueprints(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.crystal)
    app.register_blueprint(routes.courses)
    app.register_blueprint(routes.lightsaber)
    app.register_blueprint(routes.masters)
    app.register_blueprint(routes.padawan_course)
    app.register_blueprint(routes.padawans)
    app.register_blueprint(routes.species)
    app.register_blueprint(routes.temples)
