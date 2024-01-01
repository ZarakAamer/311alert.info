from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'price', 'contact', 
                'ticket',
                'privacy',
                'terms',
                'register',
                'login',
                ]

    def location(self, item):
        return reverse(item)
