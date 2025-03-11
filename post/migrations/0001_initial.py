# Generated by Django 5.1.5 on 2025-03-07 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_type', models.CharField(choices=[('News', 'News'), ('Article', 'Article')], default='Article', max_length=20)),
                ('title', models.CharField(max_length=75)),
                ('body', models.TextField(default='Empty field')),
                ('preview', models.CharField(blank=True, max_length=127)),
                ('slug', models.SlugField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post_rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('categories', models.ManyToManyField(blank=True, related_name='PostCategory', to='category.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.posts')),
            ],
        ),
    ]
