from apps.golos.backend import GolosBackend

def golos_publish_current_post_action(modeladmin, request, queryset):
    for post in queryset:
        golos_backend = GolosBackend()
        golos_backend.init()
        golos_backend.publish_post(post)

def get_post_reward_action(modeladmin, request, queryset):
    for post in queryset:
        golos_backend = GolosBackend()
        golos_backend.init()
        golos_backend.get_post(post)
