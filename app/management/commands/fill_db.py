from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from app.models import Question, Profile, Answer, Tag, User
from faker import Faker


class Command(BaseCommand):
    help = 'Fills database'

    def add_arguments(self, parser):
        return parser.add_argument('num', type=int)

    def handle(self, *args, **options):
        fake = Faker()

        num = options['num']

        users = []
        usernames = set()
        for _ in range(num):
            user = User(username=fake.user_name(), password=fake.password(length=12))
            while user.username in usernames:
                user = User(username=fake.user_name(), password=fake.password(length=12))
            usernames.add(user.username)
            users.append(user)
        
        User.objects.bulk_create(users)

        profiles = [
            Profile(
                user=user,
                rating=fake.random_int(min=-40, max=40)
            ) for user in users
        ]
        Profile.objects.bulk_create(profiles)

        tags = []
        if num > 971:
            tags_pks = fake.words(nb=971, unique=True)
            for _ in range(num - 971):
                word = ''.join(fake.random_letters(length=15))
                while word in tags_pks:
                    word = ''.join(fake.random_letters(length=15))
                tags_pks.append(word)
        else:
            tags_pks = fake.words(nb=num, unique=True)

        for tag_pk in tags_pks:
            tag = Tag(tag_name=tag_pk, tag_color=fake.random_element(elements=['bg-danger', 'bg-primary', 'bg-warning'])) 
            tags.append(tag)

        Tag.objects.bulk_create(tags)
        print("Tags created")
        profiles = Profile.objects.all()
        tags = Tag.objects.all()
    
        questions = [
            Question(
                title=fake.sentence().replace('.', '?'),
                content=fake.paragraph(nb_sentences=20),
                author=fake.random_element(elements=profiles),
                creation_date=str(fake.date_between(start_date='-10y')),
                rating=fake.random_int(min=-40, max=40)
            ) for _ in range(num * 10)
        ]
        Question.objects.bulk_create(questions)
        for i in range(num * 10):
            temp_tags=fake.random_elements(elements=list(tags), length=3, unique=True)
            for j in range(3):
                questions[i].tags.add(temp_tags[j])
        print("Questions created")
            
        questions = Question.objects.all()

        seen_questions = set()
        answers = []
        for _ in range(num * 100):
            question = fake.random_element(elements=questions)
            is_correct = question.pk not in seen_questions
            if is_correct:
                seen_questions.add(question.pk)

            answers.append(
                Answer(
                    content=fake.paragraph(nb_sentences=15),
                    author=fake.random_element(elements=profiles),
                    is_correct=is_correct,
                    creation_date=str(fake.date_between(start_date='-5y')),
                    rating=fake.random_int(min=-40, max=40),
                    question=question
                )
            )

        Answer.objects.bulk_create(answers)
        print("Answers created")
