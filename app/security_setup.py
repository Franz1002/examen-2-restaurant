def setup_roles_and_permissions(appbuilder):

    from flask_appbuilder.security.sqla.models import Role
    
    db_session = appbuilder.session
    
    roles_to_create = ['Admin', 'Cajera', 'Supervisor']
    
    for role_name in roles_to_create:
        role = db_session.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db_session.add(role)
    
    db_session.commit()
    print(f"Roles creados: {', '.join(roles_to_create)}")