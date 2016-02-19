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

        _logger.info('len(product.product_variant_ids) =) ' + str(len(product.product_variant_ids)))
        _logger.info('product.qty_available =) ' + str(product.qty_available))


        # If you want to stay on same product page when product has more than one variant
        request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
        if (len(product.product_variant_ids) > 1):
            return request.redirect("/shop/product/%s" % slug(product.product_tmpl_id))
        else:
            return request.redirect("/shop/cart")

def get_pricelist():
    cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
    sale_order = context.get('sale_order')
    if sale_order:
        pricelist = sale_order.pricelist_id
    else:
        partner = pool['res.users'].browse(cr, SUPERUSER_ID, uid, context=context).partner_id
        pricelist = partner.property_product_pricelist
    return pricelist

# inherit Website_sale Controller
class Yo_WebsiteSale(openerp.addons.website_sale.controllers.main.website_sale):

    def get_pricelist(self):
        return get_pricelist()

    def get_attribute_value_ids(self, product):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        currency_obj = pool['res.currency']
        _logger.info(" get_attribute_value_ids  { ... ")
        attribute_value_ids = []
        visible_attrs = set(l.attribute_id.id
                                for l in product.attribute_line_ids
                                    if len(l.value_ids) > 1)
        _logger.info("visible_attrs =) " + str(visible_attrs))
        if request.website.pricelist_id.id != context['pricelist']:
            _logger.info("context['pricelist']")
            website_currency_id = request.website.currency_id.id
            currency_id = self.get_pricelist().currency_id.id
            for p in product.product_variant_ids:
                _logger.info(" p =) " + str(p))
                price = currency_obj.compute(cr, uid, website_currency_id, currency_id, p.lst_price)
                attribute_value_ids.append([p.id, [v.id for v in p.attribute_value_ids if v.attribute_id.id in visible_attrs], p.price, price])
        else:
            attribute_value_ids = [[p.id, [v.id for v in p.attribute_value_ids if v.attribute_id.id in visible_attrs], p.price, p.lst_price]
                for p in product.product_variant_ids]
            _logger.info(" len(attribute_value_ids) " + str(len(attribute_value_ids)))
            _logger.info("attribute_value_ids" + str(attribute_value_ids))
        _logger.info(" get_attribute_value_ids  ... } ")
        return attribute_value_ids