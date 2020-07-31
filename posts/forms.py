from django import forms
from posts.models import Post

# for adding medium style adding
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('message','group')
        widgets={
            'message': forms.Textarea(attrs={'rows':15, 'cols':15,
                                            'class':'editable medium-editor-textarea postcontent',}),
            
        }