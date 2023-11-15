from django.contrib import admin

from .models import *


class HouseImageInline(admin.StackedInline):
    model = HouseImage
    fields = ('get_html_photo', 'image', 'default', )
    readonly_fields = ('get_html_photo', )

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class HouseAdmin(admin.ModelAdmin):
    inlines = (HouseImageInline,)
    list_display = ('id', 'title', 'price', 'm2', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'price', 'm2')
    list_editable = ('is_published', )
    list_filter = ('price', 'm2', 'is_published')
    fields = ('title', 'price', 'm2', 'desc', 'is_published', 'get_html_photo')
    readonly_fields = ('get_html_photo', )

    def get_html_photo(self, obj):
        img = obj.houseimage_set.filter(default=True)[0]
        return mark_safe(f"<a href='{img.image.url}'><img src='{img.image.url}' width=150")

    get_html_photo.short_description = 'Превью фото'


admin.site.register(House, HouseAdmin)


class HouseImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_house_name', 'get_html_photo')
    list_display_links = ('id', 'get_house_name', 'get_html_photo')
    search_fields = ('id', )
    list_filter = ('id', )
    fields = ('get_house_name', 'get_html_photo')
    readonly_fields = ('get_house_name', 'get_html_photo')

    def get_house_name(self, object):
        link = reverse("admin:Novi_Sad_houses_house_change", args=[object.house_id])
        return mark_safe(f"<a href='{link}'> {object.house.slug}")

    get_house_name.short_description = 'Дом'

    def get_html_photo(self, object):
        return mark_safe(f"<a href='{object.image.url}'><img src='{object.image.url}' width=500")

    get_html_photo.short_description = 'Фото'


admin.site.register(HouseImage, HouseImageAdmin)
