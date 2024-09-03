from django.db import models
from django.utils import timezone


class Player(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_log_in = models.DateTimeField(null=True, blank=True)
    log_in_count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def log_in(self):
        now = timezone.now()
        if not self.first_log_in:
            self.first_login = now
        self.log_in_count += 1
        self.points += 1  # В качестве примера: за каждый вход начисляется 1 балл
        self.save()

    def add_boost(self, boost_type, quantity=1):
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
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlayerBoost(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    boost_type = models.ForeignKey(Boost, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.user.username} - {self.boost_type.name}: {self.quantity}"
