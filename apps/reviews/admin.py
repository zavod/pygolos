from django.contrib import admin
from apps.reviews.models import Review, Asset
from django.db.models.fields import TextField
from tinymce.widgets import AdminTinyMCE
from apps.reviews.actions import *

admin.site.register(Asset)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',),}
    list_display = ['title', 'provider', 'source_id', 'slug', 'publish', 'complete', 'votes', 'reward', 'asset', 'btc', 'rub', 'get_out_link', ]
    formfield_overrides = {
        TextField: {'widget': AdminTinyMCE(attrs={'cols': 80, 'rows': 40}, )},
    }
    actions = [blockchain_publish_current_post_action, get_post_reward_action]

    def get_out_link(self, obj):
        return u"<a href='%s'>link</a>" % (obj.get_out_link())
    get_out_link.allow_tags = True
    get_out_link.short_description = 'profile'



