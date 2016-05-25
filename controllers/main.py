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


class QueryURL(object):
    def __init__(self, path='', **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        for k,v in self.args.items():
            kw.setdefault(k,v)
        l = []
        for k,v in kw.items():
            if v:
                if isinstance(v, list) or isinstance(v, set):
                    l.append(werkzeug.url_encode([(k,i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k,v)]))
        if l:
            path += '?' + '&'.join(l)
        return path

# inherit website_sale Controller
class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    def check_partner(self, data=None):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        """"Check if partner exists and for new partner put Fiscal position according to shipping cournty id"""
        orm_partner = registry.get('res.partner')
        orm_user = registry.get('res.users')
        orm_country = registry.get('res.country')
        state_orm = registry.get('res.country.state')
        orm_ir_property = registry.get('ir.property')

        country_ids = orm_country.search(cr, SUPERUSER_ID, [], context=context)
        countries = orm_country.browse(cr, SUPERUSER_ID, country_ids, context)
        states_ids = state_orm.search(cr, SUPERUSER_ID, [], context=context)
        states = state_orm.browse(cr, SUPERUSER_ID, states_ids, context)
        partner = orm_user.browse(cr, SUPERUSER_ID, request.uid, context).partner_id

        order = None

        shipping_id = None
        shipping_ids = []
        checkout = {}
        user_already_exists = False

        if not data:
            if request.uid != request.website.user_id.id:
                shipping_ids = orm_partner.search(cr, SUPERUSER_ID, [("parent_id", "=", partner.id), ('type', "=", 'delivery')], context=context)
            else:
                order = request.website.sale_get_order(force_create=1, context=context)
                if order.partner_id:
                    domain = [("partner_id", "=", order.partner_id.id)]
                    user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID, domain, context=dict(context or {}, active_test=False))
                    if user_ids :
                        user_already_exists = True
        else:
            checkout = self.checkout_parse('billing', data)
            try:
                shipping_id = int(data["shipping_id"])
            except ValueError:
                pass

        if shipping_id is None:
            if not order:
                order = request.website.sale_get_order(context=context)
            if order and order.partner_shipping_id:
                shipping_id = order.partner_shipping_id.id

        shipping_ids = list(set(shipping_ids) - set([partner.id]))

        if shipping_id == partner.id:
            shipping_id = 0
        elif shipping_id > 0 and shipping_id not in shipping_ids:
            shipping_ids.append(shipping_id)
        elif shipping_id is None and shipping_ids:
            shipping_id = shipping_ids[0]

        ctx = dict(context, show_address=1)
        shippings = []
        if shipping_ids:
            shippings = shipping_ids and orm_partner.browse(cr, SUPERUSER_ID, list(shipping_ids), ctx) or []
        if shipping_id > 0:
            shipping = orm_partner.browse(cr, SUPERUSER_ID, shipping_id, ctx)

        checkout['shipping_id'] = shipping_id

        # Default search by user country

        if not checkout.get('country_id'):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                country_ids = request.registry.get('res.country').search(cr, uid, [('code', '=', country_code)], context=context)
                if country_ids:
                    checkout['country_id'] = country_ids[0]

        _logger.info("Partner =) " + str(partner.name))
        _logger.info("partner.property_payment_term.id =) " + str(partner.property_payment_term.id))
        #partner_info = orm_partner.read(cr, uid, partner.id, [], context=context, load='_classic_read')
        #_logger.info("partner_info =) " + str(partner_info ))
        #_logger.info("account_config_setting =) " + str(account_config_setting))



        if order:
            _logger.info("Order =) " + str(order.name))
        country_id = checkout.get('country_id')
        _logger.info("Country Code from checkout =) " + str(country_id))
        _logger.info("user_already_exists =) " + str(user_already_exists))
        _logger.info("request.uid  =) " + str(request.uid))
        _logger.info("request.website.user_id.id  =) " + str(request.website.user_id.id))
        _logger.info("partner.id  =) " + str(partner.id))

        if partner.property_payment_term.id == False:
            if country_id == 6:
                _logger.info("Switzerland")
                payment_term_info = {
                    'property_payment_term' : orm_ir_property.search(cr, uid, [('value_reference','=','default_local_property_payment_term')], context=context),
                    'property_account_position' : orm_ir_property.search(cr, uid, [('value_reference','=','default_local_property_property_payment_term')], context=context),
                    'proprety_account_receivable' : orm_ir_property.search(cr, uid, [('value_reference','=','default_local_property_property_payment_term')], context=context),
                    'proprety_account_payable' : orm_ir_property.search(cr, uid, [('value_reference','=','default_local_property_account_payable')], context=context),
                }
            else:
                _logger.info("World Wild")
                payment_term_info = {
                    'property_payment_term' : orm_ir_property.search(cr, uid, [('value_reference','=','default_property_property_payment_term')], context=context),
                    'property_account_position' : orm_ir_property.search(cr, uid, [('value_reference','=','default_property_property_payment_term')], context=context),
                    'proprety_account_receivable' : orm_ir_property.search(cr, uid, [('value_reference','=','default_property_property_payment_term')], context=context),
                    'proprety_account_payable' : orm_ir_property.search(cr, uid, [('value_reference','=','default_property_account_payable')], context=context),
                }
            _logger.info("payment_term_info" + str(payment_term_info))
            # save partner informations
            if partner.id and request.website.partner_id.id != partner.id:
                #orm_partner.write(cr, SUPERUSER_ID, [partner_id], payment_term_info, context=context)
                _logger.info("Partner already set")
            else:
                # create partner
                partner_id = orm_partner.create(cr, SUPERUSER_ID, payment_term_info, context=context)


        return

    @http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
    def confirm_order(self, **post):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        email_act = None

        order = request.website.sale_get_order(context=context)
        if not order:
            return request.redirect("/shop")
        sale_order_obj = request.registry['sale.order']

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        values = self.checkout_values(post)

        values["error"] = self.checkout_form_validate(values["checkout"])
        if values["error"]:
            return request.website.render("website_sale.checkout", values)

        #self.check_partner(post)

        self.checkout_form_save(values["checkout"])

        request.session['sale_last_order_id'] = order.id

        request.website.sale_get_order(update_pricelist=True, context=context)

        return request.redirect("/shop/payment")

    #------------------------------------------------------
    # Payment Validate manage new Order mail
    #------------------------------------------------------

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        """ End of checkout process controller. Confirmation is basically seing
        the status of a sale.order. State at this point :

         - should not have any context / session info: clean them
         - take a sale.order id, because we request a sale.order and are not
           session dependant anymore
        """
        cr, uid, context = request.cr, request.uid, request.context

        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.registry['sale.order'].browse(cr, SUPERUSER_ID, sale_order_id, context=context)

            sale_order_obj = request.registry['sale.order']
            email_act2 = None
            email_act2 = sale_order_obj.action_quotation_send_for_approb(cr, SUPERUSER_ID, [order.id], context=request.context)

            if email_act2 and email_act2.get('context'):
                composer_values2 = {}
                email_ctx2 = email_act2['context']
                email_ctx2['mail_approb'] = True
                email_ctx2['order_id'] = order.id
                #_logger.info('email_ctx2 =)' + str(email_ctx2))
                public_id = request.website.user_id.id
                if uid == public_id:
                    composer_values2['email_from'] = request.website.user_id.company_id.email
                #_logger.info('composer_values2 =)' + str(composer_values2))

                composer_id = request.registry['mail.compose.message'].create(cr, SUPERUSER_ID, composer_values2, context=email_ctx2)
                #_logger.info('composer_id =)' + str(composer_id))

                request.registry['email.template'].send_mail(cr, SUPERUSER_ID, email_ctx2['default_template_id'], order.id, force_send=True, raise_exception=True, context=email_ctx2)


        else:
            return request.redirect('/shop')

        return request.website.render("website_sale.confirmation", {'order': order})
    @http.route(['/shop/get_unit_price'], type='json', auth="public", methods=['POST'], website=True)
    def get_unit_price(self, product_ids, add_qty, use_order_pricelist=False, **kw):
        _logger.info(" get_unit_price  { ... ")
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        products = pool['product.product'].browse(cr, uid, product_ids, context=context)
        partner = pool['res.users'].browse(cr, uid, uid, context=context).partner_id
        if use_order_pricelist:
            pricelist_id = request.session.get('sale_order_code_pricelist_id') or partner.property_product_pricelist.id
        else:
            pricelist_id = partner.property_product_pricelist.id
        prices = pool['product.pricelist'].price_rule_get_multi(cr, uid, [], [(product, add_qty, partner) for product in products], context=context)
        _logger.info(" get_unit_price   ... }")
        return {product_id: prices[product_id][pricelist_id][0] for product_id in product_ids}

    def get_attribute_value_ids(self, product):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        currency_obj = pool['res.currency']
        #_logger.info(" get_attribute_value_ids  { ... ")
        attribute_value_ids = []
        visible_attrs = set(l.attribute_id.id
                                for l in product.attribute_line_ids
                                    if len(l.value_ids) > 1)
        _logger.info("visible_attrs =) " + str(visible_attrs))
        if request.website.pricelist_id.id != context['pricelist']:
            #_logger.info("context['pricelist']")
            website_currency_id = request.website.currency_id.id
            currency_id = self.get_pricelist().currency_id.id
            for p in product.product_variant_ids:
                #_logger.info(" p =) " + str(p))
                price = currency_obj.compute(cr, uid, website_currency_id, currency_id, p.lst_price)
                attribute_value_ids.append([p.id, [v.id for v in p.attribute_value_ids if v.attribute_id.id in visible_attrs], p.price, price])
        else:
            attribute_value_ids = [[p.id, [v.id for v in p.attribute_value_ids if v.attribute_id.id in visible_attrs], p.price, p.lst_price]
                for p in product.product_variant_ids]
            #_logger.info(" len(attribute_value_ids) " + str(len(attribute_value_ids)))
            #_logger.info("attribute_value_ids" + str(attribute_value_ids))
        #_logger.info(" get_attribute_value_ids  ... } ")
        return attribute_value_ids

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', lang_selected='', **kwargs):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        category_obj = pool['product.public.category']
        template_obj = pool['product.template']

        context.update(active_id=product.id)

        if category:
            category = category_obj.browse(cr, uid, int(category), context=context)
            category = category if category.exists() else False

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int,v.split("-")) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

        category_ids = category_obj.search(cr, uid, [], context=context)
        category_list = category_obj.name_get(cr, uid, category_ids, context=context)
        category_list = sorted(category_list, key=lambda category: category[1])

        pricelist = self.get_pricelist()

        from_currency = pool.get('product.price.type')._get_field_currency(cr, uid, 'list_price', context)
        to_currency = pricelist.currency_id
        compute_currency = lambda price: pool['res.currency']._compute(cr, uid, from_currency, to_currency, price, context=context)

        if not context.get('pricelist'):
            context['pricelist'] = int(self.get_pricelist())
            product = template_obj.browse(cr, uid, int(product), context=context)


        values = {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'lang_selected': lang_selected,
            'attrib_values': attrib_values,
            'compute_currency': compute_currency,
            'attrib_set': attrib_set,
            'keep': keep,
            'category_list': category_list,
            'main_object': product,
            'product': product,
            'get_attribute_value_ids': self.get_attribute_value_ids
        }
        return request.website.render("website_sale.product", values)

# inherit Website Controller
class Website(openerp.addons.web.controllers.main.Home):

# Original
    # @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    # def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
    #     cr, uid, context = request.cr, request.uid, request.context
    #     request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))
    #     return request.redirect("/shop/cart")

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, lang_selected=1, item_type='alone', **kw):
        cr, uid, context = request.cr, request.uid, request.context

        product_product_obj = request.registry.get('product.product')
        product_template_obj = request.registry.get('product.template')

        _logger.info('product_id =) ' + str(product_id))
        _logger.info('add_qty =) ' + str(add_qty))
        # _logger.info('set_qty =) ' + str(set_qty))
        _logger.info('lang_selected =) ' + str(lang_selected))
        #_logger.info('context =) ' + str(context))
        _logger.info('item_type =) ' + str(item_type))

        product = product_product_obj.browse(cr, uid, int(product_id), context=context)

        # If product_id comes from variant
        if item_type == 'variant':
            variant_number = len(product.product_variant_ids)
        else :
            # If product_id comes from product alone
            variant_number = 1
            product_template_ids = product_template_obj.search(cr, uid, [('id', '=', product_id)], context=context)
            product_from_template_read = product_template_obj.read(cr, uid, product_template_ids, ['name','product_variant_ids'], context=context)[0]
            _logger.info('product_from_template_read =) ' + str(product_from_template_read))
            product_id = product_from_template_read['product_variant_ids'][0]

        _logger.info('product_id =) ' + str(product_id))

        _logger.info('len(variant_number) =) ' + str(variant_number))
        #qty_ok = True

        #if ((product.qty_available - float(add_qty)) < 0) :
        #    qty_ok = False

        # _logger.info('len(product.product_variant_ids) =) ' + str(len(product.product_variant_ids)))
        # _logger.info('product.qty_available =) ' + str(product.qty_available))
        _logger.info('product_id =) ' + str(product_id))

        request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=float(add_qty), set_qty=float(set_qty))

        # If you want to stay on same product page when product has more than one variant
        if item_type == 'variant':
            #values = self.checkout_values()
            #return request.website.render("website_sale.checkout", values)
            if lang_selected == 1 :
                return request.redirect("/shop/product/%s" % (slug(product.product_tmpl_id)))
            else:
                return request.redirect("/shop/product/%s?lang_selected=%s" % (slug(product.product_tmpl_id),lang_selected))
        else:
           return request.redirect("/shop/cart")

