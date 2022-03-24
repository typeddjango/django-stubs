from django.contrib.gis.db.backends.base.features import BaseSpatialFeatures as BaseSpatialFeatures
from django.db.backends.sqlite3.features import DatabaseFeatures as SQLiteDatabaseFeatures

class DatabaseFeatures(BaseSpatialFeatures, SQLiteDatabaseFeatures):
    supports_3d_storage: bool = ...
    @property
    def supports_area_geodetic(self): ...
