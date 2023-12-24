from django import forms
from app.models import User, Question, Tag, Answer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpass':
            raise forms.ValidationError('Wrong password!')
        return data

    def style_form_error(self):
        for field in self.fields.keys():
            self.add_error(field, '')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean(self):
        if 'password' in self.cleaned_data and 'password_check' in self.cleaned_data:
            password = self.cleaned_data['password']
            password_check = self.cleaned_data['password_check']
            if password != password_check:
                self.add_error('password', '')
                self.add_error('password_check', '')
                raise forms.ValidationError("Passwords don't match")
        else:
            raise forms.ValidationError("The password is required!")

    
    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        return User.objects.create_user(**self.cleaned_data)


class ChangeProfileForm(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.EmailField()
    picture = forms.FileField(widget=forms.FileInput, required=False)


class AskQuestionForm(forms.ModelForm):
    tags = forms.CharField()
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
    
    def clean_tags(self):
        tags = self.cleaned_data['tags'].split(sep=' ')
        if len(tags) < 1 or len(tags) > 3:
            raise forms.ValidationError('Too many tags!')
        return tags
    
    def save(self, **kwargs):
        tags = self.cleaned_data['tags']

        # Collect existing tags
        existing_tags = {}
        for tag in tags:
            existing_tag = Tag.objects.filter(tag_name=tag)
            if existing_tag.count() > 0:
                existing_tags[tag] = existing_tag[0]
        
        # Create new tags
        new_tags = []
        for tag in tags:
            if tag not in existing_tags.keys():
                new_tag = Tag(tag_name=tag).save()
                new_tags.append(new_tag)

        # Create new question item
        question = Question(title=self.cleaned_data['title'], content=self.cleaned_data['content'], author=kwargs['profile'], rating=0)
        question.save()
        tag_items = new_tags + list(existing_tags.values())
        for tag in tag_items:
            question.tags.add(tag)

        return question
    

class AnswerForm(forms.ModelForm):
    class Meta():
        model = Answer
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 0 or len(content) > 700:
            raise forms.ValidationError('Too many symbols (max is 700)!')
        return content
    
    def save(self, **kwargs):
        answer = Answer(content=self.cleaned_data['content'], author=kwargs['profile'], rating=0, question=kwargs['question'])
        answer.save()
        return answer