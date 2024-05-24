from django.contrib import admin

import database.models as db

# Register your models here.

admin.site.register((db.Role, db.User, db.File, db.Transaction, db.RecentActivity))
