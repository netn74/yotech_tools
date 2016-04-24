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

class delivery_carrier(osv.osv):
    _inherit = "delivery.carrier"

    _columns = {
        'free_delivery_allow': fields.boolean('Free price allow', help="If the enable Free delivery price is allow"),
        'show_under_cond': fields.boolean('Show under condition', help="If the enable Delivery methode will be display under condition"),
        'condition_type': fields.selection([('Partner Price List','partner_price_list')], 'Condition Type'),
        'partner_price_list_type': fields.property(
            type='many2one',
            relation='product.pricelist',
            domain=[('type','=','sale')],
            string="Sale Pricelist",
            help="This pricelist will be used, instead of the default one, for sales to the current partner"),
    }
