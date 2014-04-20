#!/usr/bin/env python
#coding:utf-8
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from grappelli.dashboard import modules, Dashboard
# from grappelli.dashboard.utils import get_admin_site_name


class AllRecentActions(modules.DashboardModule):
    """
    Module that lists the recent actions for the current user.
    """

    title = _('All Recent Actions')
    template = 'grappelli/dashboard/modules/recent_actions_all.html'
    limit = 10
    include_list = None
    exclude_list = None

    def __init__(self, title=None, limit=10, include_list=None,
                 exclude_list=None, **kwargs):
        self.include_list = include_list or []
        self.exclude_list = exclude_list or []
        kwargs.update({'limit': limit})
        super(AllRecentActions, self).__init__(title, **kwargs)

    def init_with_context(self, context):
        if self._initialized:
            return
        from django.db.models import Q
        from django.contrib.admin.models import LogEntry

        def get_qset(list):
            qset = None
            for contenttype in list:
                if isinstance(contenttype, ContentType):
                    current_qset = Q(content_type__id=contenttype.id)
                else:
                    try:
                        app_label, model = contenttype.split('.')
                    except:
                        raise ValueError(
                            'Invalid contenttype: "%s"' % contenttype)
                    current_qset = Q(
                        content_type__app_label=app_label,
                        content_type__model=model
                    )
                if qset is None:
                    qset = current_qset
                else:
                    qset = qset | current_qset
            return qset

        qs = LogEntry.objects.all()

        if self.include_list:
            qs = qs.filter(get_qset(self.include_list))
        if self.exclude_list:
            qs = qs.exclude(get_qset(self.exclude_list))

        self.children = qs.select_related('content_type', 'user')[:self.limit]
        self._initialized = True


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        # site_name = get_admin_site_name(context)

        # append a group for "Administration" & "Applications"
        self.children.append(modules.AppList(
            'Yönetim',
            column=1,
            collapsible=True,
            css_classes=('grp-closed',),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.ModelList(
            title='Çerçi',
            column=1,
            models=('cerci_issue.*', 'cerci_content.*', 'cerci_newsletters.*')
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            'Benim İşlem Geçmişim',
            limit=10,
            collapsible=True,
            column=2,
        ))

        # append a recent actions module
        self.children.append(AllRecentActions(
            'Tüm İşlem Geçmişi',
            limit=10,
            collapsible=True,
            column=3,
        ))

        self.children.append(modules.LinkList(
            title='Linkler',
            layout='inline',
            column=2,
            children=(
                {
                    'title': 'Anasayfa',
                    'url': 'http://cercisanat.com',
                    'external': False,
                    'description': 'Çerçi Sanat',
                },
                {
                    'title': 'Çerçi e-posta',
                    'url': 'http://mail.cercisanat.com',
                    'external': True,
                    'description': 'Çerçi Sanat E-posta',
                }
            )
        ))
