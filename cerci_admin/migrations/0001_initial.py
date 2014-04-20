# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("easy_thumbnails", "0015_auto__del_unique_thumbnail_name_storage_hash__add_unique_thumbnail_sou"),
        ("reversion", "0005_auto__add_field_revision_manager_slug"),
    )
    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass

    models = {
        
    }

    complete_apps = ['cerci_admin']