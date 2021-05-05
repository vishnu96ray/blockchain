from django.core.management.base import BaseCommand
from accounts.models import *
from .utils import *


class Command(BaseCommand):
    help = 'amount_transfer is a amount_transfer'

    def handle(self, *args, **options):
       