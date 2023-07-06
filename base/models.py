from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name = 'имя категории' )
    slug = models.SlugField(unique = True)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    

class Product(models.Model):
#основной класс продукт, который потом будет использован для наследования для создания уже подкатегорий. например, класс ноутбук, класс смартфон
    # MIN_RESOLUTION = (400, 400)
    # MAX_RESOLUTION = (800,800)
    # MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True
    #типо как виртуальный класс для наследования на плюсах, грубо говоря шаблон для классов наследования
    Category = models.ForeignKey(Category, verbose_name= 'Категория', on_delete = models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name= 'Изображение')
    description = models.TextField(verbose_name= 'Описание', null = True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    
    def __str__(self):
        return self.title
    
    # def get_model_name(self): #функция для получения имени для view
    #     return self.__class__.__name__.lower()
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default = False)
    for_anonymous_user = models.BooleanField(default = False)
    def __str__(self):
        return str(self.id)
    

class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name= 'Диагональ')
    display_type = models.CharField(max_length=255, verbose_name = 'Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge=models.CharField(max_length=255, verbose_name='Время работы аккумулятора')
    
    def __str__(self):
        return "{} : {}".format(self.Category.name, self.title)
    def get_absolute_url(self):
        return reverse('notebook_detail', kwargs={'post_slug': self.slug})

class notebook_has_Cart(models.Model):
    products = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE)
    kolichestvo = models.IntegerField(blank= False, null = False)

    def __str__(self):
        return "№{} товар: №{} корзина: {} шт.".format(self.products, self.carts, self.kolichestvo)
    
    
class SmartPhone(Product):
    diagonal = models.CharField(max_length=255, verbose_name= 'Диагональ')
    display_type = models.CharField(max_length=255, verbose_name = 'Тип дисплея')
    resolution = models.CharField(max_length=255,verbose_name= 'Разрешение экрана')
    accum_volume = models.CharField(max_length=255, verbose_name= 'Объем аккулмулятора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True, verbose_name= 'Наличие SD карты')
    sd_volume_max = models.CharField(max_length=255, null=True, blank = True, verbose_name='Максимальный объем встраиваемой памяти')
    main_camp_mp =models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.Category.name, self.title)
    

class smartphone_has_Cart(models.Model):
    products = models.ForeignKey(SmartPhone, on_delete=models.CASCADE)
    carts = models.ForeignKey(Cart, on_delete=models.CASCADE)
    kolichestvo = models.IntegerField(blank= False, null = False)

    def __str__(self):
        return "№{} товар: №{} корзина: {} шт.".format(self.products, self.carts, self.kolichestvo)
     
class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIEVRY = 'delievery'
    STATUS_CHOISES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )
    BUYING_TYPE_CHOISES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIEVRY, 'Доставка')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_from_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000, blank = True, null= True)
    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOISES, default=BUYING_TYPE_SELF)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOISES,default=STATUS_NEW)
    comment = models.TextField(verbose_name= 'Комментарий к закаку', null = True, blank= True)
    created_at=models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now, null = True, blank= True)
# Create your models here.
