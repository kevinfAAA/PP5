from django import forms


# Comment Form


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a Comment!"
        }))
