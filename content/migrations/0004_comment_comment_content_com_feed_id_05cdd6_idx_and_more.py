# Generated by Django 4.0.4 on 2022-04-26 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_bookmark_like_like_content_lik_feed_id_d49208_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('user_id', models.CharField(max_length=30)),
                ('comment', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['feed_id'], name='content_com_feed_id_05cdd6_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['email'], name='content_com_email_30465a_idx'),
        ),
    ]