from django.contrib import admin
from .models import MessageLog

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = (
        'team_user',
        'client_mobile',
        'client_name',
        'document_type',
        'loan_amount',
        'created_at'
    )
    list_filter = ('document', 'branch')  # optional filters
    search_fields = ('name', 'mobile')    # optional search

    # Methods to map admin display names to model fields
    @admin.display(description='Team User')
    def team_user(self, obj):
        return obj.user  # This links to your ForeignKey 'user'

    @admin.display(description='Client Mobile')
    def client_mobile(self, obj):
        return obj.mobile

    @admin.display(description='Client Name')
    def client_name(self, obj):
        return obj.name

    @admin.display(description='Document Type')
    def document_type(self, obj):
        return obj.document

    @admin.display(description='Loan Amount')
    def loan_amount(self, obj):
        return obj.loan