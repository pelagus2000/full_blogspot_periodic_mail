from django.apps import AppConfig
import redis

red = redis.Redis(
    host = 'redis-15129.c91.us-east-1-3.ec2.redns.redis-cloud.com',
    port = 15129
    # password=
    # commandline = redis-cli -u redis://default:ytGJpqcoSNtEkgN4IDsCQ5PlAzA6GJUP@redis-15129.c91.us-east-1-3.ec2.redns.redis-cloud.com:15129
)

class SubscriberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriber'

    def ready(self):
        from . import tasks
        tasks.start()