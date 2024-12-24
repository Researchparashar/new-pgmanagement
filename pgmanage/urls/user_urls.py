from django.urls import path
from ..views.user_views import register_owner , register_tenant,login_owner,login_tenant
from..views.getcsrf import get_csrf_token
from ..views.tenant_view import tenant_details,tenant_profile
from ..views.showpgrel_owner import show_pgs_owner
from ..views.showtenantrel_pgowner import owner_view_tenants

from ..views.pg_views import addpg


urlpatterns = [
    path("register/owner/", register_owner, name="register_owner"),
    path("register/tenant/",register_tenant,name="register_tenant"),
    path("login/owner/",login_owner,name="login_owner"),
    path("login/tenant/",login_tenant,name="login_tenant"),
    path("add/pg/",addpg,name="addpg"),
    path("get/csrf/",get_csrf_token,name="get_csrf_token"),
    path("show/pg/",show_pgs_owner,name="show_pgs_owner"),
    path("show/tenant/",tenant_details,name="tenant_details"),
    path("save/tenant/",tenant_profile,name="tenant_profile"),
    path('show/tenant/owner/<str:pg_secret>/',owner_view_tenants,name="owner_view_tenants")


  
]
