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
        product_info = self.browse(cr, uid, ids[0], context=context)
        _logger.info('button_change_template  { ...')
        _logger.info('product_info =) '+ str(product_info))

        if product_info.product_new_tmpl_id:
            product_attribute_line_obj = self.pool.get('product.attribute.line')
            product_attribute_value_obj = self.pool.get('product.attribute.value')

            _logger.info('product_info.product_new_tmpl_id.id =) '+ str(product_info.product_new_tmpl_id.id))
            if len(product_info.product_new_tmpl_id.attribute_line_ids)==1:

                attributes_line_id = product_info.product_new_tmpl_id.attribute_line_ids[0]
                _logger.info('attributes_line_id =) '+ str(attributes_line_id))
                _logger.info('product_info.product_new_tmpl_id.attribute_line_ids[0].attribute_id =) '+ str(product_info.product_new_tmpl_id.attribute_line_ids[0].attribute_id))
                _logger.info('product_info.product_tmpl_id.attribute_line_ids[0].attribute_id =) '+ str(product_info.product_tmpl_id.attribute_line_ids[0].attribute_id))
                _logger.info('product_info.product_tmpl_id.attribute_line_ids[0].value_ids =) '+ str(product_info.product_tmpl_id.attribute_line_ids[0].value_ids))
                product_attribute_line_info = product_attribute_line_obj.browse(cr, uid, [attributes_line_id], context=context)

                attribute_line_info = {
                    'product_tmpl_id' : product_info.product_new_tmpl_id.id,
                    'attribute_id' : product_info.product_new_tmpl_id.attribute_line_ids[0].attribute_id.id,
                    'value_ids' : product_info.product_tmpl_id.attribute_line_ids[0].value_ids
                }

                _logger.info('attribute_line_info =) '+ str(attribute_line_info))
                product_attribute_line_obj.write(cr, uid, product_info.product_tmpl_id.attribute_line_ids[0].id, attribute_line_info, context=context)
                product_update_info = {
                    'product_tmpl_id': product_info.product_new_tmpl_id.id
                }

                _logger.info('product_update_info =) '+ str(product_update_info))
                self.write(cr, uid, product_info.id, product_update_info, context=context)
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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: