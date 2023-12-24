from django import forms
from app.models import User, Question, Tag, Answer, Profile

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
        user = User.objects.create_user(**self.cleaned_data)
        profile = Profile.objects.create(user=user, rating=0)
        profile.save()
        return user


class SettingsForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def save(self, **kwargs):
        new_username = self.cleaned_data['username']
        new_email = self.cleaned_data['email']

        user = kwargs['user']

        existing_username_user = User.objects.filter(username=new_username).exclude(id=user.id)
        existing_email_user = User.objects.filter(username=new_email).exclude(id=user.id)
        if existing_username_user.count() != 0:
            self.add_error('username', 'User with this username already exists!')

        if existing_email_user.count() != 0:
            self.add_error('email', 'User with this email already exists!')

        if existing_username_user.count() == 0 and existing_email_user.count() == 0:
            user.username = new_username
            user.email = new_email
            user.save()


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
        if len(content) < 1 or len(content) > 700:
            raise forms.ValidationError('Too many symbols (max is 700)!')
        return content
    
    def save(self, **kwargs):
        answer = Answer(content=self.cleaned_data['content'], author=kwargs['profile'], rating=0, question=kwargs['question'])
        answer.save()
        return answer