# -*- coding: utf-8 -*-
import base64

import werkzeug
import werkzeug.urls
import werkzeug.utils
import werkzeug.wrappers

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug

import openerp.addons.website_sale.controllers.main
import json

import logging
_logger = logging.getLogger(__name__)

import cStringIO
import datetime
from itertools import islice
import json
import xml.etree.ElementTree as ET

import re
import urllib2
from PIL import Image

import openerp
from openerp.addons.web.controllers.main import WebClient
from openerp.addons.web import http
from openerp.http import request, STATIC_CACHE
from openerp.tools import image_save_for_web

# inherit Website Controller
class Website(openerp.addons.web.controllers.main.Home):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        cr, uid, context = request.cr, request.uid, request.context

        product_template_obj = request.registry.get('product.template')
        product_product_obj = request.registry.get('product.product')
        _logger.info('product_id =) ' + str(product_id))
        _logger.info('add_qty =) ' + str(add_qty))
        _logger.info('set_qty =) ' + str(set_qty))
        product = product_product_obj.browse(cr, uid, int(product_id), context=context)

        qty_ok = True

        if ((product.qty_available - float(add_qty)) < 0) :
            qty_ok = False

        _logger.info('len(product.product_variant_ids) = ' + str(len(product.product_variant_ids)))
        _logger.info('product.qty_available =) ' + str(product.qty_available))


        # If you want to stay on same product page when product has more than one variant
        if (len(product.product_variant_ids) > 1):
            request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
            return request.redirect("/shop/product/%s" % slug(product.product_tmpl_id))
        else:
            return request.redirect("/shop/cart")