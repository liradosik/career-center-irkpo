from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import PortfolioAttachment, PortfolioEntry


def _delete_file(file_field):
    if not file_field:
        return
    try:
        storage = file_field.storage
        name = file_field.name
    except AttributeError:
        return
    if name and storage.exists(name):
        storage.delete(name)


@receiver(post_delete, sender=PortfolioAttachment)
def delete_attachment_file(sender, instance, **kwargs):
    _delete_file(instance.file)


@receiver(post_delete, sender=PortfolioEntry)
def delete_entry_legacy_file(sender, instance, **kwargs):
    _delete_file(instance.file)


@receiver(pre_save, sender=PortfolioEntry)
def remember_replaced_entry_legacy_file(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_file = sender.objects.only('file').get(pk=instance.pk).file
    except sender.DoesNotExist:
        return
    new_name = instance.file.name if instance.file else ''
    old_name = old_file.name if old_file else ''
    if old_name and old_name != new_name:
        instance._old_file_to_delete = old_file


@receiver(post_save, sender=PortfolioEntry)
def delete_replaced_entry_legacy_file(sender, instance, **kwargs):
    old_file = getattr(instance, '_old_file_to_delete', None)
    if old_file:
        _delete_file(old_file)
        instance._old_file_to_delete = None
