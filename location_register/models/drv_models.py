from django.db import models

from data_ocean.models import DataOceanModel


class DrvRegion(DataOceanModel):
    code = models.CharField('код', max_length=3, unique=True)
    number = models.CharField('номер', max_length=3, unique=True)
    name = models.CharField('назва', max_length=30, unique=True)
    short_name = models.CharField('коротка назва', max_length=5, unique=True)
    capital = models.CharField('центр', max_length=20, unique=True, null=True)

    class Meta:
        verbose_name = 'регіон'


class DrvDistrict(DataOceanModel):
    region = models.ForeignKey(DrvRegion, on_delete=models.CASCADE, verbose_name='регіон')
    name = models.CharField('назва', max_length=100)

    class Meta:
        verbose_name = 'район'


class DrvCouncil(DataOceanModel):
    region = models.ForeignKey(DrvRegion, on_delete=models.CASCADE, verbose_name='регіон')
    name = models.CharField('назва', max_length=100)

    class Meta:
        verbose_name = 'рада'


class DrvAto(DataOceanModel):
    """
    ATO means "адміністративно-територіальна одиниця". Central Election Comission call that name a city, 
    a district in city, a town and a village
    """
    region = models.ForeignKey(DrvRegion, on_delete=models.CASCADE, verbose_name='регіон')
    district = models.ForeignKey(DrvDistrict, on_delete=models.CASCADE, verbose_name='район')
    council = models.ForeignKey(DrvCouncil, on_delete=models.CASCADE, verbose_name='рада')
    name = models.CharField('назва', max_length=100)
    code = models.CharField('код', max_length=7, unique=True)

    class Meta:
        verbose_name = 'адміністративно-територіальна одиниця'


class DrvStreet(DataOceanModel):
    region = models.ForeignKey(DrvRegion, on_delete=models.CASCADE, verbose_name='регіон')
    district = models.ForeignKey(DrvDistrict, on_delete=models.CASCADE, verbose_name='район')
    council = models.ForeignKey(DrvCouncil, on_delete=models.CASCADE)
    ato = models.ForeignKey(DrvAto, on_delete=models.CASCADE)
    code = models.CharField('код', max_length=15, unique=True)
    name = models.CharField('назва', max_length=155)
    previous_name = models.TextField('попередня назва', null=True)
    number_of_buildings = models.PositiveIntegerField('кількість будинків', null=True)

    class Meta:
        verbose_name = 'вулиця'


class ZipCode(DataOceanModel):
    region = models.ForeignKey(DrvRegion, on_delete=models.CASCADE, verbose_name='регіон')
    district = models.ForeignKey(DrvDistrict, on_delete=models.CASCADE, verbose_name='район')
    council = models.ForeignKey(DrvCouncil, on_delete=models.CASCADE, verbose_name='рада')
    ato = models.ForeignKey(DrvAto, on_delete=models.CASCADE,
                            verbose_name='адміністративно-територіальна одиниця')
    code = models.CharField('індекс', max_length=6, unique=True)

    class Meta:
        verbose_name = 'поштовий індекс'

    def __str__(self):
        return self.code


class DrvBuilding(DataOceanModel):
    INVALID = 'INVALID'
    region = models.ForeignKey(DrvRegion, on_delete=models.CASCADE, verbose_name='регіон')
    district = models.ForeignKey(DrvDistrict, on_delete=models.CASCADE, verbose_name='район')
    council = models.ForeignKey(DrvCouncil, on_delete=models.CASCADE, verbose_name='рада')
    ato = models.ForeignKey(DrvAto, on_delete=models.CASCADE,
                            verbose_name='адміністративно-територіальна одиниця')
    street = models.ForeignKey(DrvStreet, on_delete=models.CASCADE, verbose_name='вулиця')
    zip_code = models.ForeignKey(ZipCode, on_delete=models.CASCADE,
                                 verbose_name='поштовий індекс')
    code = models.CharField('код', max_length=20, unique=True)
    number = models.CharField(max_length=58)

    class Meta:
        verbose_name = 'будинок'

    def __str__(self):
        return self.number
