from django.contrib.auth.models import User
from django.db import models

class DadosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Adicione quaisquer outros campos necessários para o UserProfile

    def __str__(self):
        return self.user.username


class MinhasCompras(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='compras')
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
