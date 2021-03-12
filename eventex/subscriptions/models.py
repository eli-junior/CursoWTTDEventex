from django.db import models


class Subscription(models.Model):
    id = models.CharField('ID', primary_key=True, serialize=False, max_length=33)
    name = models.CharField('nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11)
    phone = models.CharField('telefone', max_length=20)
    email = models.EmailField('e-mail')
    created_at = models.DateTimeField('inscrito em', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering = ('-created_at', )

    def __str__(self):
        return self.name
