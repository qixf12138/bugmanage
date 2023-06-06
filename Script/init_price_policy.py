import os
import sys

import django


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bugmanage.settings")
django.setup()
from project.models import PricePolicy



def init_price_policy_data():
    policy = PricePolicy.objects.create(level=1, price=0, create_project=3,
                                         project_user=2, project_capacity=100,
                                         file_capacity=10)
    policy.save()


if __name__ == "__main__":
    init_price_policy_data()
