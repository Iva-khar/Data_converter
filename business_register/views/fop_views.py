from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl import Workbook
from rest_framework import viewsets

from business_register.filters import FopFilterSet
from business_register.models.fop_models import Fop
from business_register.serializers.fop_serializers import FopSerializer
from data_ocean.views import CachedViewMixin, RegisterViewMixin
from rest_framework.filters import SearchFilter


class FopViewSet(RegisterViewMixin,
                 CachedViewMixin,
                 viewsets.ReadOnlyModelViewSet):
    queryset = Fop.objects.select_related(
        'status', 'authority'
    ).prefetch_related(
        'kveds', 'exchange_data'
    ).all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    serializer_class = FopSerializer
    filterset_class = FopFilterSet
    search_fields = ('fullname', 'address', 'status__name')

    def list(self, request, *args, **kwargs):
        try:
            if request.GET['export'] == 'xlsx':
                queryset = self.filter_queryset(self.get_queryset())
                export_dict = {
                    'Full Name': 'name',
                    'Status': 'status',
                    'Address': 'address',
                    'Registration Date': 'registration_date',
                    'Termination Date': 'termination_date',
                }
                export_file_path = settings.EXPORT_FOLDER + 'fop_{0}.xlsx'.format(
                    datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                )
                worksheet_title = 'FOP'
                export_xlsx(queryset, export_file_path, export_dict, worksheet_title)
                return HttpResponse(export_file_path, content_type="text/plain")
        except:
            return super().list(request, *args, **kwargs)


def export_xlsx(queryset, export_file_path, export_dict, worksheet_title):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = worksheet_title
    for col_num, (column_title, query_field) in enumerate(export_dict.items(), 1):
        row_num = 1
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        for record in queryset:
            row_num += 1
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = locals().get('record.'+query_field)
    return workbook.save(export_file_path)
