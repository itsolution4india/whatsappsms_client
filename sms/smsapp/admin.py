from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import CustomUser,Whitelist_Blacklist,ReportInfo,Templates, RegisterApp, ScheduledMessage, TemplateLinkage, MessageResponse, UserAccess, CoinsHistory, Flows, CountryPermission, BotSentMessages, Train_wit_Bot
from .models import Register_TwoAuth, Validate_TwoAuth, Notifications, Group, Contact, Last_Replay_Data, LoginAttempt, LoginHistory
from .emailsend import main_send
from django.utils.html import format_html
from django import forms

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'user_id', 'username', 'phone_number_id', 'whatsapp_business_account_id', 'coins','marketing_coins','authentication_coins', 'is_staff', 'register_app')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'user_id', 'phone_number_id', 'whatsapp_business_account_id','marketing_coins','authentication_coins',"remarks", 'password', 'register_app', 'api_token')}),
        (_('Personal info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_id', 'username', 'phone_number_id', 'whatsapp_business_account_id','marketing_coins','authentication_coins', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'register_app'),  # Removed 'coins' here
        }),
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(email='admin@gmail.com')
    
    def save_model(self, request, obj, form, change):
        # Get the original object from the database (if it exists)
        if change:
            orig_obj = self.model.objects.get(pk=obj.pk)
            # Check if certain fields have changed (e.g., email)
            if obj.email != orig_obj.email:
                new_mail=obj.email
                old_mail=orig_obj.email
                main_send(new_mail,old_mail)      
        # Save the object
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RegisterApp)
class WhitelistBlacklistAdminForm(forms.ModelForm):
    class Meta:
        model = Whitelist_Blacklist
        fields = '__all__'
        widgets = {
            'whitelist_phone': forms.Textarea(attrs={'placeholder': '+9197857XXXXX'}),
            'blacklist_phone': forms.Textarea(attrs={'placeholder': '+9197857XXXXX'}),
        }

# class Whitelist_BlacklistAdmin(admin.ModelAdmin):
#     list_display = ('whitelist_phone', 'blacklist_phone')
#     search_fields = ('whitelist_phone', 'blacklist_phone')
    
#     fieldsets = (
#         (None, {
#             'fields': ('whitelist_phone', 'blacklist_phone'),
#             'description': "Enter new phone numbers to be whitelist and blacklist, each on a new line."
#         }),
#     )
#     form = WhitelistBlacklistAdminForm

# admin.site.register(Whitelist_Blacklist, Whitelist_BlacklistAdmin)


class ReportInfoAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'email',
        "campaign_title",
        'template_name',
        'message_date',
        'message_delivery',
        "contact_list",
        "waba_id_list",
        "start_request_id",
        "end_request_id"
        
        

    )
    list_filter = (
        'email',
        'message_date',
    )
    search_fields = (
        'email__email',
    )
    date_hierarchy = 'message_date'
    ordering = ('-message_date',)

    fields = (
        'created_at',
        'email',
        "campaign_title",
        "contact_list",
        "waba_id_list",
        'message_date',
        'message_delivery',
        'template_name',
        "start_request_id",
        "end_request_id"
      
 
    )
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(email__email='admin@gmail.com')



admin.site.register(ReportInfo, ReportInfoAdmin)


# class TemplatesAdmin(admin.ModelAdmin):
#     list_display = (
#         'email',
#         'templates',
#     )
#     list_filter = (
#         'email',
#     )
#     search_fields = (
#         'email__email',
#     )
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'email',
#                 'templates',
#             ),
#         }),
#     )
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.exclude(email__email='admin@gmail.com')

class UserAccessAdminForm(forms.ModelForm):
    class Meta:
        model = UserAccess
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter out admin@gmail.com from the user dropdown
        if 'user' in self.fields:
            self.fields['user'].queryset = self.fields['user'].queryset.exclude(email='admin@gmail.com')

class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_send_sms', 'can_view_reports', 'can_manage_campaign', 'can_schedule_tasks', 'can_create_flow_message', 'can_send_flow_message', 'can_link_templates', 'can_manage_bot_flow', "can_access_API_doc", 'can_manage_number_validation', "can_enable_2fauth")
    form = UserAccessAdminForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(user__email='admin@gmail.com')

class CountryPermissionAdminForm(forms.ModelForm):
    class Meta:
        model = CountryPermission
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter out admin@gmail.com from the user dropdown
        if 'user' in self.fields:
            self.fields['user'].queryset = self.fields['user'].queryset.exclude(email='admin@gmail.com')

class CountryPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_send_msg_to_india')
    form = CountryPermissionAdminForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(user__email='admin@gmail.com')


# Form for Flows admin
class FlowsAdminForm(forms.ModelForm):
    class Meta:
        model = Flows
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].queryset = self.fields['email'].queryset.exclude(email='admin@gmail.com')

# Admin class for Flows
class FlowsAdmin(admin.ModelAdmin):
    list_display = ('email', 'flows')
    form = FlowsAdminForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(email__email='admin@gmail.com')

# Form for LoginHistory admin
class LoginHistoryAdminForm(forms.ModelForm):
    class Meta:
        model = LoginHistory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'user' in self.fields:
            self.fields['user'].queryset = self.fields['user'].queryset.exclude(email='admin@gmail.com')

# Admin class for LoginHistory
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address', 'location')
    form = LoginHistoryAdminForm
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(user__email='admin@gmail.com')

# Update the existing WhitelistBlacklistAdminForm
class WhitelistBlacklistAdminForm(forms.ModelForm):
    class Meta:
        model = Whitelist_Blacklist
        fields = '__all__'
        widgets = {
            'whitelist_phone': forms.Textarea(attrs={'placeholder': '+9197857XXXXX'}),
            'blacklist_phone': forms.Textarea(attrs={'placeholder': '+9197857XXXXX'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].queryset = self.fields['email'].queryset.exclude(email='admin@gmail.com')

# Update the existing Whitelist_BlacklistAdmin
class Whitelist_BlacklistAdmin(admin.ModelAdmin):
    list_display = ('whitelist_phone', 'blacklist_phone')
    search_fields = ('whitelist_phone', 'blacklist_phone')
    form = WhitelistBlacklistAdminForm
    
    fieldsets = (
        (None, {
            'fields': ('email', 'whitelist_phone', 'blacklist_phone'),
            'description': "Enter new phone numbers to be whitelist and blacklist, each on a new line."
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(email__email='admin@gmail.com')

# Form for Templates admin
class TemplatesAdminForm(forms.ModelForm):
    class Meta:
        model = Templates
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].queryset = self.fields['email'].queryset.exclude(email='admin@gmail.com')

# Update the existing TemplatesAdmin
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ('email', 'templates')
    list_filter = ('email',)
    search_fields = ('email__email',)
    form = TemplatesAdminForm
    
    fieldsets = (
        (None, {
            'fields': ('email', 'templates',),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(email__email='admin@gmail.com')
    
    
# Register your admin class with the model
admin.site.register(Templates, TemplatesAdmin)
admin.site.register(Whitelist_Blacklist, Whitelist_BlacklistAdmin)
admin.site.register(LoginHistory, LoginHistoryAdmin)
admin.site.register(Flows, FlowsAdmin)
admin.site.register(ScheduledMessage)
admin.site.register(TemplateLinkage)
admin.site.register(MessageResponse)
admin.site.register(BotSentMessages)
admin.site.register(UserAccess, UserAccessAdmin)
admin.site.register(CountryPermission, CountryPermissionAdmin)
admin.site.register(CoinsHistory)
admin.site.register(Train_wit_Bot)
admin.site.register(Register_TwoAuth)
admin.site.register(Validate_TwoAuth)
admin.site.register(Notifications)
admin.site.register(Group)
admin.site.register(Contact)
admin.site.register(Last_Replay_Data)
admin.site.register(LoginAttempt)