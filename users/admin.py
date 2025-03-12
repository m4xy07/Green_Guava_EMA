from django.contrib import admin
from .models import *
from django.utils.html import format_html


admin.site.register(Profile)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'video_preview')  # ✅ Use video_preview instead

    def video_preview(self, obj):
        """Shows a playable video preview in the admin panel."""
        if obj.video:  # Check if video exists
            return format_html(
                '<video width="150" controls><source src="{}" type="video/mp4"></video>',
                obj.video.url
            )
        return "No Video"

    video_preview.allow_tags = True
    video_preview.short_description = "Preview"

