from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Khách hàng'),
        ('staff', 'Nhân viên'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    class Meta:
        db_table = 'accounts_userprofile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Da xac nhan'),
        ('pending', 'Cho xac nhan'),
        ('cancelled', 'Da huy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service_id = models.CharField(max_length=50)
    service_name = models.CharField(max_length=255)
    package_id = models.CharField(max_length=50)
    package_name = models.CharField(max_length=255)
    package_sessions = models.CharField(max_length=100)
    package_price = models.CharField(max_length=100)
    package_result = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.service_name} - {self.appointment_date} {self.appointment_time}"

    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['appointment_date', 'appointment_time']
        constraints = [
            models.UniqueConstraint(
                fields=['appointment_date', 'appointment_time'],
                name='unique_appointment_slot'
            )
        ]


class ConsultationConversation(models.Model):
    STATUS_CHOICES = [
        ('open', 'Dang mo'),
        ('closed', 'Da dong'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_conversations')
    subject = models.CharField(max_length=255, default='Tư vấn dịch vụ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"

    class Meta:
        db_table = 'consultation_conversations'
        verbose_name = 'Consultation Conversation'
        verbose_name_plural = 'Consultation Conversations'
        ordering = ['-updated_at']


class ConsultationMessage(models.Model):
    SENDER_CHOICES = [
        ('customer', 'Khach hang'),
        ('spa', 'Spa'),
    ]

    conversation = models.ForeignKey(
        ConsultationConversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation_id} - {self.sender}"

    class Meta:
        db_table = 'consultation_messages'
        verbose_name = 'Consultation Message'
        verbose_name_plural = 'Consultation Messages'
        ordering = ['created_at']

