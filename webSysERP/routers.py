class InternalExternalRouter:
    internal_apps = {'users', 'almacen', 'logistica', 'rrhh'}
    external_apps = {'clientes', 'visitas', 'proveedores'}
    system_apps = {'auth', 'contenttypes', 'admin', 'sessions'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.system_apps:
            return 'default'
        elif model._meta.app_label in self.internal_apps:
            return 'default'
        elif model._meta.app_label in self.external_apps:
            return 'extranet'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.system_apps:
            return 'default'
        elif model._meta.app_label in self.internal_apps:
            return 'default'
        elif model._meta.app_label in self.external_apps:
            return 'extranet'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_for_read(obj1)
        db2 = self.db_for_read(obj2)
        if db1 and db2:
            return db1 == db2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.system_apps:
            return db == 'default'
        elif app_label in self.internal_apps:
            return db == 'default'
        elif app_label in self.external_apps:
            return db == 'extranet'
        return None