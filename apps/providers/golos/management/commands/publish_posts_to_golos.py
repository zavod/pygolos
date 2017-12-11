# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from apps.providers.golos import GolosBackend


class Command(BaseCommand):
    help = "Test post to Golos.io"

    def handle(self, *args, **options):
        golos_backend = GolosBackend()
        golos_backend.publish_post()



