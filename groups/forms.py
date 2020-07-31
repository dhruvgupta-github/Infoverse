from django import forms
from groups.models import Group

class GroupForm(forms.ModelForm):
    class Meta():
        model = Group
        fields= ('name', 'description')
        widgets={
            
            'description': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent',
                                                'rows':100, 'cols':15 ,}),

            'name': forms.Textarea(attrs={'rows':1, 'cols':15}),
        }