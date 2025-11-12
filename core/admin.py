from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CourseFeature, CourseOverview, CourseSkill, CourseTool, CourseBrochure,
    CoursePayment, CourseAccess
)
from .models_brochure import BrochureDownload
from .admin_brochure import BrochureDownloadAdmin  # Import the brochure admin
# Register CourseFeature for admin control
@admin.register(CourseFeature)
class CourseFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    ordering = ('course', 'order')

@admin.register(CourseOverview)
class CourseOverviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('course', 'order')

@admin.register(CourseSkill)
class CourseSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('name',)
    list_editable = ('order', 'is_active')
    ordering = ('course', 'order')

@admin.register(CourseTool)
class CourseToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'order', 'is_active')
    list_filter = ('course', 'is_active')
    search_fields = ('name',)
    list_editable = ('order', 'is_active')
    ordering = ('course', 'order')

@admin.register(CourseBrochure)
class CourseBrochureAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'is_active', 'updated_at')
    list_filter = ('course', 'is_active')
    search_fields = ('course__name', 'title')
    list_editable = ('is_active',)
    ordering = ('course',)
from django.contrib import admin
from .models import (
    Section, Content, HeroBanner, AboutPage, AboutSection, 
    FeatureCard, HomeAboutSection, CourseCategory, CourseBrowser,
    LearningBanner, WhyChoose, WhyChooseItem, CertificateSection,
    FAQQuestion, TestimonialStrip, Course, CourseInstructor
    , CourseLocalInstructor
)
from .models import CourseScheduleDay, CourseScheduleItem

class ContentInline(admin.TabularInline):
    model = Content
    extra = 1
    fields = ('title', 'content', 'image', 'order', 'is_active')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ContentInline]
    list_editable = ('order', 'is_active')
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'description', 'image', 'order', 'is_active')}),
        ('Styling', {'fields': ('background_color', 'text_color', 'custom_css'), 'classes': ('collapse',)}),
    )
    # show font size in styling section
    def get_fieldsets(self, request, obj=None):
        fs = list(self.fieldsets)
        # insert text_font_size into Styling if present
        fs[1][1]['fields'] = tuple(list(fs[1][1]['fields']) + ['text_font_size'])
        return tuple(fs)
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)
        
from django.contrib import admin
from .models import *

@admin.register(CoursePurchaseCard)
class CoursePurchaseCardAdmin(admin.ModelAdmin):
    """Admin interface for CoursePurchaseCard model."""
    list_display = ['course', 'title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['course__name', 'title']
    raw_id_fields = ['course']
    fieldsets = (
        ('Course', {
            'fields': ('course',)
        }),
        ('Card Content', {
            'fields': (
                'card_image',
                'title',
                'description',
                'button_text',
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title', 'highlight_text']
    list_editable = ('is_active',)
    fieldsets = (
        (None, {'fields': ('title', 'highlight_text', 'image', 'button_text', 'button_url', 'is_active')}),
        ('Styling', {'fields': ('overlay_color', 'text_color', 'button_background', 'button_text_color'), 'classes': ('collapse',)}),
    )
    def get_fieldsets(self, request, obj=None):
        fs = list(self.fieldsets)
        fs[1][1]['fields'] = tuple(list(fs[1][1]['fields']) + ['text_font_size', 'button_font_size'])
        return tuple(fs)
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)
        
@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {'fields': ('title', 'subtitle', 'main_image', 'is_active')}),
        ('Styling', {'fields': ('background_color', 'text_color'), 'classes': ('collapse',)}),
    )
    def get_fieldsets(self, request, obj=None):
        fs = list(self.fieldsets)
        fs[1][1]['fields'] = tuple(list(fs[1][1]['fields']) + ['text_font_size'])
        return tuple(fs)
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)
        
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type', 'order', 'is_active', 'updated_at')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('order', 'is_active')
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)
        
    def save_formset(self, request, form, formset, change):
        """Override save_formset to ensure related content changes are saved immediately."""
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        for obj in formset.deleted_objects:
            obj.delete()


@admin.register(LearningBanner)
class LearningBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'highlight', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'highlight', 'subtitle')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {'fields': ('title', 'highlight', 'subtitle', 'image', 'button_text', 'button_url', 'is_active')}),
    )

    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)



class WhyChooseItemInline(admin.TabularInline):
    model = WhyChooseItem
    extra = 1
    fields = ('text', 'image', 'order', 'is_active', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return f'<img src="{obj.image.url}" style="max-height:60px;" />'
        return ''
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'


@admin.register(WhyChoose)
class WhyChooseAdmin(admin.ModelAdmin):
    list_display = ('section_title', 'section_subtitle', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('section_title', 'section_subtitle')
    inlines = [WhyChooseItemInline]
    fieldsets = (
        (None, {'fields': ('section_title', 'section_subtitle', 'is_active')}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# WhyChooseItem is intentionally not registered as a top-level ModelAdmin so it is
# managed inline under WhyChooseAdmin (WhyChooseItemInline above). This keeps
# the admin index simpler and avoids duplicated entry points for editing items.

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'is_active', 'updated_at')
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'content')
    list_editable = ('order', 'is_active')
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)
        
@admin.register(FeatureCard)
class FeatureCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'card_title', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('card_title', 'card_description')
    list_editable = ('order', 'is_active')
    fieldsets = (
        (None, {'fields': ('card_number', 'card_title', 'card_description', 'card_image', 'order', 'is_active')}),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)

@admin.register(HomeAboutSection)
class HomeAboutSectionAdmin(admin.ModelAdmin):
    list_display = ('section_label', 'main_heading', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('section_label', 'main_heading', 'description')
    fieldsets = (
        (None, {'fields': ('section_label', 'main_heading', 'description', 'image', 'is_active')}),
        ('Button Options', {'fields': ('button_text', 'button_url')}),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)


@admin.register(CertificateSection)
class CertificateSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {'fields': ('title', 'subtitle', 'image', 'is_active')}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(FAQQuestion)
class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active', 'updated_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active', 'order')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('name', 'is_active', 'order')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)

@admin.register(CourseBrowser)
class CourseBrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name',)
    list_editable = ('is_active', 'order')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('name', 'image', 'category', 'is_active', 'order')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save_model to ensure changes are saved immediately."""
        super().save_model(request, obj, form, change)

@admin.register(TestimonialStrip)
class TestimonialStripAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description')
    list_editable = ('order', 'is_active')
    fieldsets = (
        (None, {'fields': ('title', 'subtitle', 'description', 'image', 'order', 'is_active')}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class CourseInstructorInline(admin.TabularInline):
    model = CourseInstructor
    extra = 1
    fields = ('instructor', 'order', 'is_primary')

class CourseLocalInstructorInline(admin.TabularInline):
    model = CourseLocalInstructor
    extra = 1
    fields = ('name', 'image', 'order', 'is_primary', 'is_active')
    readonly_fields = ()


class CourseScheduleDayInline(admin.TabularInline):
    """Allow quick adding of schedule days directly on the Course admin."""
    model = CourseScheduleDay
    extra = 1
    fields = ('title', 'order', 'is_active')
    show_change_link = True

@admin.register(CoursePayment)
class CoursePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'course__name', 'order_id', 'payment_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(CourseAccess)
class CourseAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__email', 'course__name')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'original_price', 'discounted_price', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active')
    # detailed_description removed from model; keep searchable fields minimal
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    # Keep both the global CourseInstructor inline (select existing instructors)
    # and the CourseLocalInstructor inline (manual per-course instructor entries).
    # Also allow quick creation of schedule days inline. Detailed schedule items
    # should be edited from their own admin so they can be ordered per-day.
    inlines = [CourseInstructorInline, CourseLocalInstructorInline, CourseScheduleDayInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('Course Details', {
            'fields': ('category', 'original_price', 'discounted_price', 'buy_url')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# Schedule admin
class CourseScheduleItemInline(admin.TabularInline):
    model = CourseScheduleItem
    extra = 1
    # Keep the inline minimal for admins: title, thumbnail image, uploaded file, ordering and active flag
    fields = ('title', 'thumbnail', 'video_file', 'order', 'is_active')


@admin.register(CourseScheduleDay)
class CourseScheduleDayAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_active', 'updated_at')
    list_filter = ('course', 'is_active')
    search_fields = ('title', 'course__name')
    inlines = [CourseScheduleItemInline]
    list_editable = ('order', 'is_active')
    ordering = ('course', 'order')


@admin.register(CourseScheduleItem)
class CourseScheduleItemAdmin(admin.ModelAdmin):
    # Minimal list display without thumbnail/duration to match admin preference
    list_display = ('title', 'day', 'order', 'is_active')
    list_filter = ('day__course', 'is_active')
    # Remove description from searchable fields since it's no longer editable in admin
    search_fields = ('title', 'day__title')
    list_editable = ('order', 'is_active')
    ordering = ('day', 'order')
    fieldsets = (
        (None, {'fields': ('day', 'title', 'thumbnail')}),
        ('Video', {'fields': ('video_file',)}),
        ('Options', {'fields': ('order', 'is_active')}),
    )