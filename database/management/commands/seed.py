from typing import Any

from django.core.management.base import BaseCommand

from database.models import RBAC, Role, Permission


class Command(BaseCommand):
    help = "Seeds the Database with Initial Data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        if not Role.objects.filter(rolename="ADMIN").exists():
            Role.objects.create(rolename="ADMIN").save()
        if not Role.objects.filter(rolename="USER").exists():
            Role.objects.create(rolename="USER").save()

        self.stdout.write(self.style.SUCCESS("Seeded Roles Table."))

        if Permission.objects.exists():
            Permission.objects.all().delete()

        # Modules
        DASHBOARD      = "Dashboard"
        ENCRYPTION     = "Enkripsi"
        DECRYPTION     = "Dekripsi"
        ACCESS_CONTROL = "Manajemen Hak Akses"
        USER_MANAGER   = "Manajemen Pengguna"

        Permission.objects.bulk_create(
            (
                Permission(permission_name="Recent Activity", module_name=DASHBOARD),
                Permission(permission_name="Stats", module_name=DASHBOARD),
                Permission(permission_name="Encrypt File", module_name=ENCRYPTION),
                Permission(permission_name="Download File", module_name=DECRYPTION),
                Permission(permission_name="Decrypt File", module_name=DECRYPTION),
                Permission(permission_name="Delete File", module_name=DECRYPTION),
                Permission(permission_name="Access Control", module_name=ACCESS_CONTROL),
                Permission(permission_name="User Manager", module_name=USER_MANAGER)
            )
        )

        self.stdout.write(self.style.SUCCESS("Seeded Permissions Table."))

        # Permissions
        all_permissions = Permission.objects.all()
        recent_activity = all_permissions.get(permission_name="Recent Activity", module_name=DASHBOARD)
        stats           = all_permissions.get(permission_name="Stats", module_name=DASHBOARD)
        encrypt_file    = all_permissions.get(permission_name="Encrypt File", module_name=ENCRYPTION)
        download_file   = all_permissions.get(permission_name="Download File", module_name=DECRYPTION)
        decrypt_file    = all_permissions.get(permission_name="Decrypt File", module_name=DECRYPTION)

        admin_rbac = []
        for permission in all_permissions:
            admin_rbac.append(
                RBAC(permission=permission, role=Role.objects.get(rolename="ADMIN"))
            )

        RBAC.objects.bulk_create(
            (
                RBAC(permission=recent_activity, role=Role.objects.get(rolename="USER")),
                RBAC(permission=stats, role=Role.objects.get(rolename="USER")),
                RBAC(permission=encrypt_file, role=Role.objects.get(rolename="USER")),
                RBAC(permission=download_file, role=Role.objects.get(rolename="USER")),
                RBAC(permission=decrypt_file, role=Role.objects.get(rolename="USER")),
                *admin_rbac
            )
        )

        self.stdout.write(self.style.SUCCESS("Seeded RBAC Table."))
