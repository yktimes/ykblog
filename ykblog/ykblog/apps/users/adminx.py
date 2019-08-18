import xadmin

from .models import User
from xadmin.plugins import auth


class UserAdmin(auth.UserAdmin):
    list_display = ['id', 'username','name', 'avatar' ,'last_login','date_joined','is_staff']
    readonly_fields = ['last_login', 'date_joined']
    list_filter=['username','name']
    list_editable=['avatar','is_staff']
    search_fields = ('username', )
    show_detail_fields = ['id']
    style_fields = {'user_permissions': 'm2m_transfer', 'groups': 'm2m_transfer'}

    data_charts = {
        "user_amount": {'title': '活跃度', "x-field": "last_login", "y-field": ('id')},
    }

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.fields = ['username',  'is_staff']

        return super().get_model_form(**kwargs)


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)