from catalog.models import Version


def set_product_version(product):
    """
    Функция для получения версии последней версии продукта
    :param product:
    :return:
    """
    active_version = Version.objects.filter(product=product, current_version=True).last()
    if active_version:
        product.active_version_number = active_version.version
        product.active_version_name = active_version.name_version
    else:
        product.active_version_number = None
        product.active_version_name = None
    return product