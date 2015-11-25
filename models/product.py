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


class product_template(osv.osv):
    _inherit = "product.template"

    def _website_price_displayed(self, cr, uid, ids, field_name, arg, context=None):
        """ Return true if price must be display or not on a website
            Ex: product out of stock and Product avaible on demand
        """
        res = {}
        yotech_setting = self.pool['yotech.setting'].browse(cr, uid, ids, context=context)[0]

        for product_tmpl in self.browse(cr, uid, ids):
            res[product_tmpl.id] = True
            if yotech_setting.product_out_of_stock_mgn:
                if product_tmpl['qty_available'] <= 0:
                    res[product_tmpl.id] = False
            if product_tmpl['product_on_demand_only']:
                res[product_tmpl.id] = False
        return res

    _columns = {
        'website_price_displayed': fields.function(_website_price_displayed, string="Is price displayed", type="boolean"),
        'product_on_demand_only': fields.boolean('Product on demand only?'),
        'message_type_ids': fields.many2many('message.type', 'message_type_rel', 'child_id', 'parent_id', 'Message list'),
    }    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: