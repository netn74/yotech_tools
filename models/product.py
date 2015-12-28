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

from openerp.osv import fields, osv

import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round, float_compare

import logging
_logger = logging.getLogger(__name__)

class product_product(osv.osv):
    _inherit = "product.product"

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

        if len(product_old_template_info.attribute_line_ids) <> 1:
            _logger.error('Old template has no attibute or more than 1 attribute')
            return {}

        if len(product_new_template_info.attribute_line_ids) == 0:
            _logger.error('New template has no attibute')
            return {}

        if product_old_template_info == product_new_template_info:
            _logger.error('Old and New template are already egal')
            return {}

        _logger.info('product_info.ean13 =) '+ str(product_info.ean13))
        _logger.info('product_info.product_new_tmpl_id.id =) '+ str(product_info.product_new_tmpl_id.id))

        attribute_line_found = False
        _logger.info('product_old_template_info.attribute_line_ids[0] =) '+ str(product_old_template_info.attribute_line_ids[0]))
        _logger.info('product_new_template_info.attribute_line_ids[0] =) '+ str(product_new_template_info.attribute_line_ids[0]))
        for attribute_line_id in product_new_template_info.attribute_line_ids:
            _logger.info('attribute_line_id =) '+ str(attribute_line_id))
            if (product_old_template_info.attribute_line_ids[0].attribute_id.name == attribute_line_id.attribute_id.name) :
                new_attribute_line_id = attribute_line_id
                _logger.info('new_attribute_line_id =) '+ str(new_attribute_line_id))
                attribute_line_found = True
        # If attribute line found in a new template
        if attribute_line_found:
            old_product_tmpl_id = product_info.product_tmpl_id
            new_product_tmpl_id = product_info.product_new_tmpl_id

            product_attribute_line_new_info = new_attribute_line_id
            product_attribute_line_old_info = product_old_template_info.attribute_line_ids[0]

            product_attribute_value_old_info = product_info.attribute_value_ids
            _logger.info('product_attribute_value_old_info =) '+ str(product_attribute_value_old_info))

            _logger.info('----------------- STEP1 -----------------')
            _logger.info('Merge attribut value id to the new template')

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
        else:
            _logger.info('Product_attribute not found in new template check there is same attribute name in new and old template')
        _logger.info('button_change_template  }')

        return {}

    _columns = {
        'product_new_tmpl_id': fields.many2one('product.template', 'New Product Template Proposal'),
        #UPDATE product_attribute_line_product_attribute_value_rel SET line_id=7 WHERE line_id=1;
        #'attributes_proposal_ids' : fields.one2many('product.attribute.line', 'product_tmpl_id', 'Product Attributes')
        #'attributes_ids' : fields.one2many('product.attribute.line', 'product_tmpl_id', 'Product Attributes')
    }

class product_template(osv.osv):
    _inherit = "product.template"

    _columns = {
        'message_type_ids': fields.many2many('message.type', 'message_type_rel', 'child_id', 'parent_id', 'Message list'),
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