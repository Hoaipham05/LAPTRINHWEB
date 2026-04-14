from django.contrib import admin

from .models import (
    Appointment,
    ConsultationConversation,
    ConsultationMessage,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Thong tin co ban', {
            'fields': ('user', 'role')
        }),
        ('Thong tin lien he', {
            'fields': ('phone', 'address')
        }),
        ('Thoi gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'service_name',
        'package_name',
        'appointment_date',
        'appointment_time',
        'status',
    )
    list_filter = ('status', 'appointment_date', 'created_at')
    search_fields = (
        'user__username',
        'user__email',
        'service_name',
        'package_name',
    )
    readonly_fields = ('created_at', 'updated_at')


class ConsultationMessageInline(admin.TabularInline):
    model = ConsultationMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'created_at')


@admin.register(ConsultationConversation)
class ConsultationConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'status', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'subject')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ConsultationMessageInline]


@admin.register(ConsultationMessage)
class ConsultationMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'created_at')
    list_filter = ('sender', 'created_at')
    search_fields = ('conversation__user__username', 'conversation__user__email', 'content')
    readonly_fields = ('created_at',)
