from django.contrib import admin
from .models import OneChoiceQuestion, OneChoiceChoice, FillInQuestion

# Register your models here.

admin.site.site_header = "Mobile Learning Administration"

class OneChoiceChoiceInline(admin.TabularInline):
    model = OneChoiceChoice
    extra = 4

class OneChoiceQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['accuracy', 'visit_count'], 'classes': ['collapse']}),
    ]
    inlines = [OneChoiceChoiceInline]
    list_display = ('question_id', 'question_text', 'answer_number_and_id', 'category_text', 'topic', 'source', 'entry_date', 'accuracy', 'visit_count')
    list_filter = ['entry_date', 'category']
    search_fields = ['question_text']

class FillInQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['visit_count'], 'classes': ['collapse']}),
    ]
    list_display = ('question_id', 'question_text', 'category_text', 'topic', 'source', 'entry_date', 'visit_count')

admin.site.register(OneChoiceQuestion, OneChoiceQuestionAdmin)
admin.site.register(FillInQuestion, FillInQuestionAdmin)