from django.db import models
from django.utils import timezone

# В данном задании реализовано только ручное начисление бустов,
# так как для начисления бустов за прохождение уровней нужно
# по аналогии со вторым заданием создать модель Level для уровней,
# модель PlayerLevel для учета прохождения игроками уровней,
# и модель LevelBoost, отражающую соотношение уровней и причитающихся
# за них бустов; логика будет та же, что с начислением призов.
# Если будет нужно, тоже могу реализовать.


class Player(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)  # Связываем с моделью User
    first_log_in = models.DateTimeField(null=True, blank=True)  # Запоминаем первую дату входа
    log_in_count = models.IntegerField(default=0)  # Количество входов
    points = models.IntegerField(default=0)  # Количество полученных баллов за вход

    # Метод, добавляющий баллы за вход
    def log_in(self):
        now = timezone.now()
        if not self.first_log_in:
            self.first_login = now  # Фиксируем, если это первый вход
        self.log_in_count += 1
        self.points += 1  # В качестве примера: за каждый вход начисляется 1 балл
        self.save()

    # Метод для ручного добавления буста пользователю в количестве quantity
    def add_boost(self, boost_type: str, quantity: int = 1):
        boost, created = PlayerBoost.objects.get_or_create(
            player=self, boost_type=boost_type,
            defaults={'quantity': quantity}
        )
        if not created:
            boost.quantity += quantity
            boost.save()

    def __str__(self):
        return f"Player {self.user.username}"


class Boost(models.Model):
    BOOST_CHOICES = [
        ('first_boost', 'Boost 1'),
        ('second_boost', 'Boost 2'),
        ('third_boost', 'Boost 3'),
    ]  # Схематичные примеры возможных типов бустов

    name = models.CharField(max_length=100, choices=BOOST_CHOICES)

    def __str__(self):
        return self.name


# Модель, которая отражает назначение бустов игрокам и их количество
class PlayerBoost(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    boost_type = models.ForeignKey(Boost, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.user.username} - {self.boost_type.name}: {self.quantity}"
