# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from datetime import datetime
from django import template
from adzone.models import AdBase, AdImpression

register = template.Library()


@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_zone_ad(context, ad_zone):
    """
    Returns a random advert for ``ad_zone``.
    The advert returned is independent of the category

    In order for the impression to be saved add the following
    to the TEMPLATE_CONTEXT_PROCESSORS:

    'adzone.context_processors.get_source_ip'

    Tag usage:
    {% load adzone_tags %}
    {% random_zone_ad 'zone_slug' %}

    """
    to_return = {}

    # Retrieve a random ad for the zone
    ad = AdBase.objects.get_random_ad(ad_zone)
    to_return['ad'] = ad

    # Record a impression for the ad
    if 'from_ip' in context and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                ad=ad, impression_date=datetime.now(), source_ip=from_ip)
            impression.save()
        except:
            pass
    return to_return


@register.inclusion_tag('adzone/ad_tag.html', takes_context=True)
def random_category_ad(context, ad_zone, ad_category):
    """
    Returns a random advert from the specified category.

    Usage:
    {% load adzone_tags %}
    {% random_category_ad 'zone_slug' 'my_category_slug' %}

    """
    to_return = {}

    # Retrieve a random ad for the category and zone
    ad = AdBase.objects.get_random_ad(ad_zone, ad_category)
    to_return['ad'] = ad

    # Record a impression for the ad
    if 'from_ip' in context and ad:
        from_ip = context.get('from_ip')
        try:
            impression = AdImpression(
                ad=ad, impression_date=datetime.now(), source_ip=from_ip)
            impression.save()
        except:
            pass
    return to_return


@register.simple_tag(name='get_video_img')
def get_video_img(video_url):
    video_id = video_url.split('/')[-1]
    img_url = ''

    if 'youtube' in video_url:
        img_url = 'http://img.youtube.com/vi/%s/0.jpg' % video_id
    elif 'vimeo' in video_url:
        import json
        import urllib2
        response = urllib2.urlopen('http://vimeo.com/api/v2/video/%s.json' % video_id)
        json_resp = response.read()
        video_dict = json.loads(json_resp)
        img_url = video_dict[0]['thumbnail_large']

    return img_url