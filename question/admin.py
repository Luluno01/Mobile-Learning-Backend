from django.contrib import admin
from .models import OneChoiceQuestion, OneChoiceChoice
from .models import FillInQuestion
from .models import SubjectiveQuestion
from .models import TrueOrFalseQuestion
from .models import MultipleChoiceQuestion, MultipleChoiceChoice
from .models import QuestionList
from .models import Cron

# Register your models here.

admin.site.site_header = "Mobile Learning Administration"

class OneChoiceChoiceInline(admin.TabularInline):
    model = OneChoiceChoice
    extra = 4

class OneChoiceQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['accuracy', 'correct_count_daily', 'correct_count_weekly', 'visit_count', 'visit_count_daily', 'visit_count_weekly'], 'classes': ['collapse']}),
    ]
    inlines = [OneChoiceChoiceInline]
    list_display = ('question_id', 'question_text', 'answer_number_and_id', 'category_text', 'topic', 'source', 'entry_date', 'accuracy', 'visit_count')
    list_filter = ['entry_date', 'category']
    search_fields = ['question_text']

class FillInQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['visit_count', 'visit_count_daily', 'visit_count_weekly'], 'classes': ['collapse']}),
    ]
    list_display = ('question_id', 'question_text', 'category_text', 'topic', 'source', 'entry_date', 'visit_count')

class SubjectiveQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['visit_count', 'visit_count_daily', 'visit_count_weekly'], 'classes': ['collapse']}),
    ]
    list_display = ('question_id', 'question_text', 'category_text', 'topic', 'source', 'entry_date', 'visit_count')

class TrueOrFalseQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['correct_count', 'correct_count_daily', 'correct_count_weekly', 'visit_count', 'visit_count_daily', 'visit_count_weekly'], 'classes': ['collapse']}),
    ]
    list_display = ('question_id', 'question_text', 'category_text', 'topic', 'source', 'entry_date', 'accuracy', 'visit_count')

class MultipleChoiceChoiceInline(admin.TabularInline):
    model = MultipleChoiceChoice
    extra = 4

class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 'answer', 'resolution', 'category']}),
        ('Meta information', {'fields': ['entry_date', 'source', 'topic'], 'classes': ['collapse']}),
        ('Statistics', {'fields': ['accuracy', 'correct_count', 'correct_count_daily', 'correct_count_weekly', 'visit_count', 'visit_count_daily', 'visit_count_weekly'], 'classes': ['collapse']}),
    ]
    inlines = [MultipleChoiceChoiceInline]
    list_display = ('question_id', 'question_text', 'answer_number_and_id', 'category_text', 'topic', 'source', 'entry_date', 'accuracy', 'correct_count', 'visit_count')
    list_filter = ['entry_date', 'category']
    search_fields = ['question_text']

class CronAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['last_run']})
    ]
    list_display = ('last_run', )


class QuestionListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['one_choice_question', 'multiple_choice_question', 'true_or_false_question', 'fill_in_question', 'subjective_question']})
    ]
    list_display = (['one_choice_question', 'multiple_choice_question', 'true_or_false_question', 'fill_in_question', 'subjective_question'])

admin.site.register(OneChoiceQuestion, OneChoiceQuestionAdmin)
admin.site.register(FillInQuestion, FillInQuestionAdmin)
admin.site.register(SubjectiveQuestion, SubjectiveQuestionAdmin)
admin.site.register(TrueOrFalseQuestion, TrueOrFalseQuestionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(Cron, CronAdmin)
admin.site.register(QuestionList, QuestionListAdmin)