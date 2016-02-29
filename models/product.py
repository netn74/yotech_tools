# -*- coding: utf-8 -*-
##############################################################################
#
#    Yotech module
#    Copyright (C) 2014-2015 Yotech (<http://yotech.pro>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields, expression
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round, float_compare

import logging
_logger = logging.getLogger(__name__)

class product_attribute(osv.osv):
    _inherit = "product.attribute"
    _order = 'sequence'

    _columns = {
        'sequence': fields.integer('Sequence', help="Determine the display order"),
    }

class product_product(osv.osv):
    _inherit = "product.product"



    def _product_cart_qty(self, cr, uid, ids, field_name, arg, context=None):
        _logger.info("product_cart_qty ids ")
        res = dict()
        i = 0
        website_obj = self.pool.get('website')
        order = website_obj.sale_get_order(cr, uid, ids[0], context=context)
        if order:
            _logger.info("order  " + str(order))

            for product in self.browse(cr, uid, ids, context=context):
                qty = 0
                _logger.info("product  " + str(product))
                for line in order.website_order_line:
                    _logger.info("line  " + str(line))
                    if product.id == line.product_id.id:
                        qty = int(line.product_uom_qty or 0)
                res[product.id] = qty
        return res

    def button_switch_template(self, cr, uid, ids, context=None):
        """ Utility method used to switch of Product_template """

        product_attribute_line_obj = self.pool.get('product.attribute.line')
        product_attribute_value_obj = self.pool.get('product.attribute.value')
        product_attribute_obj = self.pool.get('product.attribute')
        product_template_obj = self.pool.get('product.template')

        product_info = self.browse(cr, uid, ids[0], context=context)
        _logger.info('button_change_template  { ...')
        _logger.info('product_info =) '+ str(product_info))

        product_old_template_info = product_info.product_tmpl_id
        _logger.info('product_old_template_info =) '+ str(product_old_template_info))
        product_new_template_info = product_info.product_new_tmpl_id
        _logger.info('product_new_template_info =) '+ str(product_new_template_info))

        if len(product_old_template_info.attribute_line_ids) <> len(product_new_template_info.attribute_line_ids):
            error_Msg = 'Old Template and New Template must have the same attribute_line number  Old => %s <> New => %s' % (len(product_old_template_info.attribute_line_ids),len(product_new_template_info.attribute_line_ids))
            raise osv.except_osv(_("Error!"), _(error_Msg))
            _logger.error(error_Msg)
            return {}

        if product_old_template_info == product_new_template_info:
            error_Msg = 'Old and New template are already the same'
            raise osv.except_osv(_("Error!"), _(error_Msg))
            _logger.error(error_Msg)
            return {}

        _logger.info('product_info.ean13 =) '+ str(product_info.ean13))
        _logger.info('product_info.product_new_tmpl_id.id =) '+ str(product_info.product_new_tmpl_id.id))

        _logger.info('product_old_template_info.attribute_line_ids[0] =) '+ str(product_old_template_info.attribute_line_ids[0]))
        _logger.info('product_new_template_info.attribute_line_ids[0] =) '+ str(product_new_template_info.attribute_line_ids[0]))

        for tmplnew_attribute_line_id in product_new_template_info.attribute_line_ids:
            _logger.info('tmplnew_attribute_line_id =) '+ str(tmplnew_attribute_line_id))
            for tmplold_attribute_line_id in product_old_template_info.attribute_line_ids:
                _logger.info('tmplold_attribute_line_id =) '+ str(tmplold_attribute_line_id))
                if (tmplold_attribute_line_id.attribute_id.name == tmplnew_attribute_line_id.attribute_id.name) :
                    _logger.info('tmplold_attribute_line_id.attribute_id.name =) '+ str(tmplold_attribute_line_id.attribute_id.name))
                    new_attribute_line_id = tmplnew_attribute_line_id
                    _logger.info('new_attribute_line_id =) '+ str(new_attribute_line_id))
                    # If attribute line found in a new template
                    old_product_tmpl_id = product_info.product_tmpl_id
                    new_product_tmpl_id = product_info.product_new_tmpl_id

                    product_attribute_line_new_info = new_attribute_line_id
                    product_attribute_line_old_info = tmplold_attribute_line_id

                    product_attribute_value_old_info = product_info.attribute_value_ids
                    _logger.info('product_attribute_value_old_info =) '+ str(product_attribute_value_old_info))

                    _logger.info('----------------- STEP1 -----------------')
                    _logger.info('Merge attribut value id to the new template')
                    #if value attribut is not yet in new tpl
                    value_id_found = False
                    value_id_search = tmplold_attribute_line_id.value_ids[0]
                    _logger.info('value_id_search =) '+ str(value_id_search))
                    for value_id in tmplnew_attribute_line_id.value_ids:
                        _logger.info('current value_id =) '+ str(value_id))
                        if value_id == value_id_search:
                            value_id_found = True
                    if not value_id_found:
                        attribute_line_info = {
                            'product_tmpl_id' : new_product_tmpl_id.id
                        }

                        _logger.info('attribute_line_info =) '+ str(attribute_line_info))

                        product_attribute_line_obj.write(cr, uid, product_attribute_line_old_info.id, attribute_line_info, context=context)
                        SQL_UPDATE="UPDATE product_attribute_line_product_attribute_value_rel SET line_id='%s' WHERE line_id='%s'" % (product_attribute_line_new_info.id,product_attribute_line_old_info.id)
                        _logger.info(SQL_UPDATE)
                        cr.execute(SQL_UPDATE)
                    SQL_DELETE="DELETE FROM product_attribute_line WHERE id='%s' AND product_tmpl_id='%s'" % (product_attribute_line_old_info.id,new_product_tmpl_id.id)
                    _logger.info(SQL_DELETE)
                    cr.execute(SQL_DELETE)

                    _logger.info('--------------- END STEP1 ---------------')

        _logger.info('----------------- STEP2 -----------------')
        _logger.info('Change template id of current product')
        product_update_info = {
            'product_tmpl_id': product_info.product_new_tmpl_id.id,
            'product_new_tmpl_id' : False
        }

        _logger.info('product_update_info =) '+ str(product_update_info))
        self.write(cr, uid, product_info.id, product_update_info, context=context)
        _logger.info('--------------- END STEP2 ---------------')

        # Disable Old Template with unique variant
        product_template_old_update_info = {
            'active': False
        }

        _logger.info('product_template_old_update_info =) '+ str(product_template_old_update_info))
        product_template_obj.write(cr, uid, old_product_tmpl_id.id, product_template_old_update_info, context=context)

        _logger.info('button_change_template  }')
        return {}

    _columns = {
        'product_new_tmpl_id': fields.many2one('product.template', 'New Product Template Proposal'),
        'product_cart_quantity': fields.function(_product_cart_qty, type='integer', string='Product Cart Quantity'),
    }

class product_template(osv.osv):
    _inherit = "product.template"

    _columns = {
        'message_type_ids': fields.many2many('message.type', 'message_type_rel', 'child_id', 'parent_id', 'Message list'),
    }

class product_attribute_value(osv.Model):
    _inherit = "product.attribute.value"

    def _get_product_info(self, cr, uid, ids, attribute_value, field_name, arg, context=None):
        for product_info in attribute_value.product_ids:
            for value_id in product_info.attribute_value_ids:
                if value_id.attribute_id == attribute_value.attribute_id:
                    val_return = product_info
        return val_return

    def _get_ean13(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for attribute_value in self.browse(cr, uid, ids):
            product_info = self._get_product_info(cr, uid, ids, attribute_value, field_name, arg, context)
            res[attribute_value.id] = product_info.ean13
        return res

    def _get_defaultcode(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for attribute_value in self.browse(cr, uid, ids):
            product_info = self._get_product_info(cr, uid, ids, attribute_value, field_name, arg, context)
            res[attribute_value.id] = product_info.default_code
        return res

    def _get_prod_id(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for attribute_value in self.browse(cr, uid, ids):
            product_info = self._get_product_info(cr, uid, ids, attribute_value, field_name, arg, context)
            res[attribute_value.id] = product_info.id
        return res



    _columns = {
        'jsdata': fields.char("JS data", help="Here you can set a specific data to display icon on the website if the attibute type is 'Color' according to methode already implemented. exmple : ['rect2','red','blue'] \
                                               ref : http://www.w3schools.com/html/html_colornames.asp"),
        'get_ean13': fields.function(_get_ean13, string="EAN13", type="char"),
        'get_defaultcode': fields.function(_get_defaultcode, string="Ref", type="char"),
        'get_prod_id': fields.function(_get_prod_id, string="Product_id", type="integer"),
    }

# Structure reference :
# class product_attribute(osv.osv):
#     _name = "product.attribute"
#     _description = "Product Attribute"
#     _columns = {
#         'name': fields.char('Name', translate=True, required=True),
#         'value_ids': fields.one2many('product.attribute.value', 'attribute_id', 'Values', copy=True),
#     }
# class product_attribute_line(osv.osv):
#     _name = "product.attribute.line"
#     _rec_name = 'attribute_id'
#     _columns = {
#         'product_tmpl_id': fields.many2one('product.template', 'Product Template', required=True, ondelete='cascade'),
#         'attribute_id': fields.many2one('product.attribute', 'Attribute', required=True, ondelete='restrict'),
#         'value_ids': fields.many2many('product.attribute.value', id1='line_id', id2='val_id', string='Product Attribute Value'),
#     }

# class product_attribute_value(osv.osv):
#     _columns = {
#         'sequence': fields.integer('Sequence', help="Determine the display order"),
#         'name': fields.char('Value', translate=True, required=True),
#         'attribute_id': fields.many2one('product.attribute', 'Attribute', required=True, ondelete='cascade'),
#         'product_ids': fields.many2many('product.product', id1='att_id', id2='prod_id', string='Variants', readonly=True),
# ...
#     }

# class product_product
#        'attribute_value_ids': fields.many2many('product.attribute.value', id1='prod_id', id2='att_id', string='Attributes', readonly=True, ondelete='restrict'),
#        'is_product_variant': fields.function( _is_product_variant_impl, type='boolean', string='Is product variant'),
#        'product_tmpl_id': fields.many2one('product.template', 'Product Template', required=True, ondelete="cascade", select=True, auto_join=True),

# class product_template
        # 'attribute_line_ids': fields.one2many('product.attribute.line', 'product_tmpl_id', 'Product Attributes'),
        # 'product_variant_ids': fields.one2many('product.product', 'product_tmpl_id', 'Products', required=True),
        # 'product_variant_count': fields.function( _get_product_variant_count, type='integer', string='# of Product Variants'),

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
