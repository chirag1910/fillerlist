from django.db import models
from django.db.models.functions import TruncDate
from django.db.models import Count

class AnalyticManager(models.Manager):
    def get_daily_trend(self):
        """
        Will return total no. of visits, and unique visits on each day
        """

        qs = self.annotate(day=TruncDate('time')).values('day')
        qs = qs.annotate(
            total=Count('ip_address'),
            unique=Count("ip_address", distinct=True)
        ).order_by('day')

        return qs
    
    def get_visits(self, time=None, unique=False):
        qs = self.all()

        if time:
            qs = qs.filter(time__gte=time)
        
        if unique:
            qs = qs.values("ip_address").distinct()

        return qs.count()
