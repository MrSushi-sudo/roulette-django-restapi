from django.db import models

    
class Spin(models.Model):
    result = models.IntegerField()

    def __str__(self):
        return "Спин #{}, выпал: {}".format(self.pk, self.result)

class RoundManager(models.Manager):
    """
    RoundManager: кастомный менеджер для
    возврата проаннотированного queryset'а
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            spins_count=models.Count('spins')
        )

        return queryset

class Round(models.Model):
    user = models.CharField(
        verbose_name="Пользователь",
        max_length=50
    )

    is_finished = models.BooleanField(
        default=False,
        verbose_name="Игра закончена"
    )

    is_jackpot = models.BooleanField(
        default=False,
        verbose_name="Джекпот выигран"
    )

    spins = models.ManyToManyField(
        Spin,
        verbose_name="Спины раунда",
        blank=True
    )

    # переопределяем дефолтный менеджер
    objects = RoundManager()

    def __str__(self):
        def get_deferred_fields(field):
            if field:
                return "Да"
            
            return "Нет"

        return "Раунд #{}, джекпот: {}, завершён: {}".format(
            self.pk,
            get_deferred_fields(self.is_jackpot),
            get_deferred_fields(self.is_finished)
        )
