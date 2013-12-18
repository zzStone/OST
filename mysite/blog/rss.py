from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.files import File
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
import uuid, os, datetime
from models import *

class CorrectMimeTypeFeed(Rss201rev2Feed):
    mime_type = 'application/xml'


class RssFeed(Feed):
    title = "OST blOgShoT"
    link = ""
    description = "zzStone's fianl project."
    feed_type = CorrectMimeTypeFeed

    def get_object(self, request, blog_id=None):
        return Blog.objects.get(pk=blog_id)

    def title(self, obj):
        return obj.name

    def link(self, obj):
        return reverse('blog:blogs', args=(obj.id, 0))
        #return ''

    def description(self, obj):
        return obj.name

    def author_name(self, obj):
        return  (obj.user.username)

    # def author_email(self, obj):
    #     return obj.creator.email

    def items(self, obj):
        return Post.objects.filter(blog__id=obj.id)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = item.body[:500]
        return content

    def item_link(self, item):
        return reverse('blog:posts', args=(item.id,))

    def item_guid(self, item):
        return reverse('blog:posts', args=(item.id,))
    
    def item_author_name(self, item):
        return  (item.blog.user.username)

    # def item_pubdate(self, item):
    #     return item.create_time
