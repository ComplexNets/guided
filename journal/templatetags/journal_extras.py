from django import template
import re
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='format_feedback')
def format_feedback(text):
    if not text:
        return ''
        
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra'])
    html = md.convert(text)
    
    # Add our custom classes for styling
    html = html.replace('<h1>', '<div class="feedback-section"><h1 class="feedback-section-title">')
    html = html.replace('</h1>', '</h1><div class="feedback-section-content">')
    html = html.replace('<h2>', '<div class="feedback-section"><h2 class="feedback-section-title">')
    html = html.replace('</h2>', '</h2><div class="feedback-section-content">')
    html = html.replace('<h3>', '<div class="feedback-section"><h3 class="feedback-section-title">')
    html = html.replace('</h3>', '</h3><div class="feedback-section-content">')
    
    # Close feedback sections
    html = html.replace('</div>\n<div class="feedback-section">', '</div></div>\n<div class="feedback-section">')
    html = html + '</div></div>' if '<div class="feedback-section">' in html else html
    
    return mark_safe(html)
