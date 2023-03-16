from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget

FIELDS = [
            'title',
            'main_text',
            'category',
        ]

LABELS = {
    'Category': 'Категория',
}


class PostForm(forms.ModelForm):
    main_text = forms.CharField(min_length=20, widget=CKEditorUploadingWidget, label='Описание')
    title = forms.CharField(min_length=5, label='Название')

    class Meta:
        model = Post
        fields = FIELDS
        labels = LABELS

    def clean(self):
        cleaned_data = super().clean()
        main_text = cleaned_data.get("main_text")
        title = cleaned_data.get("title")

        if title == main_text:
            raise ValidationError({
                "title": "Описание не должно быть идентично названию."
            })

        return cleaned_data


FIELDS_COMMENT = [
            'main_text',
        ]


class CommentForm(forms.ModelForm):
    main_text = forms.CharField(min_length=10, widget=forms.Textarea, label='Описание')

    class Meta:
        model = Comment
        fields = FIELDS_COMMENT
