from django import template

register = template.Library()

@register.filter(name='is_image')
def is_image(file_url):
    return file_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif','.webp'))

@register.filter(name='is_video')
def is_video(file_url):
    return file_url.lower().endswith('.mp4')

@register.filter(name='is_audio')
def is_audio(file_url):
    return file_url.lower().endswith('.mp3')
