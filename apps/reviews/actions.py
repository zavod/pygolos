from apps.providers.provider import BaseProvider

def blockchain_publish_current_post_action(modeladmin, request, queryset):
    for review in queryset:
        provider = BaseProvider().get_review_provider(review)
        if provider:
            provider.init()
            provider.publish_post(review)

def get_post_reward_action(modeladmin, request, queryset):
    for review in queryset:
        provider = BaseProvider().get_review_provider(review)
        if provider:
            provider.init()
            provider.get_post(review)
