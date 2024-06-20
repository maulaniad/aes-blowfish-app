from enum import Enum
from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import (Model,
                              UUIDField,
                              IntegerField,
                              CharField,
                              DateTimeField,
                              FileField,
                              BinaryField,
                              ForeignKey,
                              CASCADE)

from helpers.dates import dt_end_date, dt_now
from helpers.enums import TransactionStatus
from helpers.types import ICONS, COLORS

# Create your models here.

class BaseModel(Model):
    date_created = DateTimeField(db_column="date_created", auto_now_add=True)
    date_updated = DateTimeField(db_column="date_updated", auto_now=True)
    date_deleted = DateTimeField(db_column="date_deleted", default=dt_end_date)

    def soft_delete(self) -> None:
        self.date_deleted = dt_now()
        self.save()

    class Meta:
        abstract = True


class Role(BaseModel):
    oid      = UUIDField(db_column="oid", unique=True, default=uuid4)
    rolename = CharField(db_column="rolename", max_length=20, db_index=True)

    def __str__(self) -> str:
        return self.rolename

    class Meta(BaseModel.Meta):
        db_table = "tb_roles"


class UserManager(BaseUserManager):
    def create_user(self, username, email, fullname, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        if not fullname:
            raise ValueError("The given fullname must be set")
        if not password:
            raise ValueError("The given password must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, fullname=fullname, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, fullname, password, **extra_fields):
        role = Role.objects.get(rolename__icontains="admin")
        extra_fields.setdefault('role', role)
        return self.create_user(username, email, fullname, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    oid              = UUIDField(db_column="oid", unique=True, default=uuid4)
    fullname         = CharField(db_column="fullname", max_length=150, db_index=True)
    username         = CharField(db_column="username", unique=True, max_length=50, db_index=True)
    email            = CharField(db_column="email", max_length=50, db_index=True)
    password         = CharField(db_column="password", max_length=255)
    password_changed = DateTimeField(db_column="password_changed", null=True, default=None)
    role             = ForeignKey(to=Role, db_column="role_id", on_delete=CASCADE)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'fullname']

    def __str__(self) -> str:
        return self.fullname

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.password = make_password(self.password)

        if "ADMIN" not in args:
            self.role = Role.objects.get(rolename="USER")

        super().save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        db_table = "tb_users"


class File(BaseModel):
    oid        = UUIDField(db_column="oid", unique=True, default=uuid4)
    file       = FileField(db_column="file")
    filename   = CharField(db_column="filename", max_length=255, db_index=True)
    extension  = CharField(db_column="extension", max_length=10)
    size       = IntegerField(db_column="size")
    aes_key    = BinaryField(db_column="aes_key")
    secret_key = CharField(db_column="secret_key", max_length=255, blank=True)

    def __str__(self) -> str:
        return self.filename

    def save(self, *args, **kwargs) -> None:
        if not self.filename:
            self.filename = self.file.name
        if not self.extension:
            self.extension = self.filename.split(".")[-1]
        if not self.size:
            self.size = self.file.size
        super().save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        db_table = "tb_files"


class Transaction(BaseModel):
    oid    = UUIDField(db_column="oid", unique=True, default=uuid4)
    key    = CharField(db_column="key", max_length=255, db_index=True)
    vector = BinaryField(db_column="vector")
    name   = CharField(db_column="name", max_length=255)
    status = CharField(db_column="status", max_length=10, choices=[(s.name, s.value) for s in TransactionStatus])
    user   = ForeignKey(to=User, db_column="user_id", on_delete=CASCADE)
    file   = ForeignKey(to=File, db_column="file_id", on_delete=CASCADE)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if isinstance(self.status, Enum):
            self.status = self.status.value
        super().save(*args, **kwargs)

    class Meta(BaseModel.Meta):
        db_table = "tb_transactions"


class RecentActivity(BaseModel):
    oid      = UUIDField(db_column="oid", unique=True, default=uuid4)
    action   = CharField(db_column="action", max_length=50, db_index=True)
    box_icon = CharField(db_column="box_icon", max_length=50, choices=[(k.name, v) for k, v in ICONS.items()])
    tw_color = CharField(db_column="tw_color", max_length=50, choices=[(k.name, v) for k, v in COLORS.items()])
    issued   = DateTimeField(db_column="issued", auto_now_add=True)
    user     = ForeignKey(to=User, db_column="user_id", on_delete=CASCADE)

    def __str__(self) -> str:
        return self.action

    class Meta(BaseModel.Meta):
        db_table = "tb_recent_activities"


class Permission(BaseModel):
    oid             = UUIDField(db_column="oid", unique=True, default=uuid4)
    permission_name = CharField(db_column="permission_name", max_length=50, db_index=True)
    module_name     = CharField(db_column="module_name", max_length=50, db_index=True)

    def __str__(self) -> str:
        return self.permission_name

    class Meta(BaseModel.Meta):
        db_table = "tb_permissions"


class RBAC(BaseModel):
    oid        = UUIDField(db_column="oid", unique=True, default=uuid4)
    permission = ForeignKey(to=Permission, db_column="permission_id", on_delete=CASCADE)
    role       = ForeignKey(to=Role, db_column="role_id", on_delete=CASCADE)

    class Meta(BaseModel.Meta):
        db_table = "tb_rbac"
