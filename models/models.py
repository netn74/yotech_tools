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


class yotech_setting(osv.osv):
    _order = "name"
    _name = "yotech.setting"
    _description = "Yotech setting"

    _columns = {
        'name': fields.char('Yotech Setting Name', required=True, copy=False,
            readonly=False, select=True),
        'product_out_of_stock_mgn': fields.boolean('Product Out of Stock Management?')
    }

class message_type(osv.osv):
    _order = "name"
    _name = "message.type"
    _description = "Web html Message type after description sale"

    _columns = {
        'name': fields.char('Message Name', required=True, copy=False,
            readonly=False, select=True),
        'message': fields.html('Html Message',translate=True,
            help="An addtionnal description of the Product that you want to add on Frontend. "
                 "This description will not be added to the Sale Order and others documents"),
    }