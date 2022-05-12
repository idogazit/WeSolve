# Generated by Django 3.0.8 on 2022-05-12 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0010_auto_20220507_1723'),
        ('questions', '0015_auto_20220508_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionTopic',
            fields=[
                ('questionTopicId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('labeledByUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('questionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Question')),
                ('topicName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Topic', to_field='topicName')),
            ],
            options={
                'db_table': 'QuestionTopics',
            },
        ),
    ]
