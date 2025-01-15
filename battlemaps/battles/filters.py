import os

from django.contrib.gis.db.models.functions import GeometryDistance
from django.db.models import Q
from rest_framework_gis.filters import DistanceToPointFilter


class NearestBattlesFilter(DistanceToPointFilter):
    """Only retrieve battles that are nearest to the point queried."""
    def filter_queryset(self, request, queryset, view):
        point = self.get_filter_point(request, srid=4326)
        queryset = queryset.order_by(GeometryDistance('point', point))

        miles = int(os.environ['MILES_LIMIT'])
        dist = miles * 1609  # Filter below uses meters so multiply miles by 1609 to get meters desired

        # We'll paginate the battles on the client, so it's unlikely users will want to see more
        # than a certain amount of battles per point queried
        nearest_slice = int(os.environ['NEAREST_SLICE'])

        return queryset.filter(
            Q(**{'%s__%s' % ('point', 'dwithin'): (point, dist)})
        )[:nearest_slice]
