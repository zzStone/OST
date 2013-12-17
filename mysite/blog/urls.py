from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index', name='index'),
    url(r'^about/$', 'blog.views.about', name='about'),
    url(r'^contact/$', 'blog.views.contact', name='contact'),
    url(r'^register/$', 'blog.views.register', name='register'),
    url(r'^reg_result/$', 'blog.views.reg_result', name='reg_result'),
    url(r'^login/$', 'blog.views.login', name='login'),
    url(r'^login_result/$', 'blog.views.login_result', name='login_result'),
    url(r'^logout/$', 'blog.views.logout', name='logout'),
    url(r'^logout_result/$', 'blog.views.logout_result', name='logout_result'),
    url(r'^(?P<blog_id>\d+)/blogs/(?P<page_id>\d+)$', 'blog.views.blogs', name='blogs'),
    url(r'^(?P<post_id>\d+)/posts/$', 'blog.views.posts', name='posts'),
    url(r'^(?P<tag_id>\d+)/tags/$', 'blog.views.tags', name='tags'),
    url(r'^myblogs/$', 'blog.views.myblogs', name='myblogs'),
    url(r'^addnewblog/$', 'blog.views.addnewblog', name='addnewblog'),
    url(r'^addblog_result/$', 'blog.views.addblog_result', name='addblog_result'),
    url(r'^(?P<blog_id>\d+)/addnewpost/$', 'blog.views.addnewpost', name='addnewpost'),
    url(r'^addpost_result/$', 'blog.views.addpost_result', name='addpost_result'),
    url(r'^(?P<blog_id>\d+)/rmblog/$', 'blog.views.rmblog', name='rmblog'),
    url(r'^(?P<post_id>\d+)/rmpost/$', 'blog.views.rmpost', name='rmpost'),
    url(r'^(?P<post_id>\d+)/addnewtag/$', 'blog.views.addnewtag', name='addnewtag'),
    url(r'^(?P<post_id>\d+)/addtag_result/$', 'blog.views.addtag_result', name='addtag_result'),
    url(r'^(?P<tag_id>\d+)/rmtag/$', 'blog.views.rmtag', name='rmtag'),


#    url(r'^(?P<poll_id>\d+)/$', 'blog.views.detail', name='detail'),
#    url(r'^(?P<poll_id>\d+)/results/$', 'blog.views.results', name='results'),
#    url(r'^(?P<poll_id>\d+)/vote/$', 'blog.views.vote', name='vote'),
)