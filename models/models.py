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

class yotech_settings(osv.osv):
    _name = "yotech.settings"
    _description = "Yotech settings"

    def copy(self, cr, uid, id, values, context=None):
        raise UserError(_("Cannot duplicate configuration!"), "")

    def execute(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        context = dict(context, active_test=False)
        if not self.pool['res.users']._is_admin(cr, uid, [uid]):
            raise openerp.exceptions.AccessError(_("Only administrators can change the settings"))

        # force client-side reload (update user menu and current view)
        return {}

    def cancel(self, cr, uid, ids, context=None):
        # ignore the current record, and send the action to reopen the view
        act_window = self.pool['ir.actions.act_window']
        action_ids = act_window.search(cr, uid, [('res_model', '=', self._name)])
        if action_ids:
            return act_window.read(cr, uid, action_ids[0], [], context=context)
        return {}

    _columns = {
        'name': fields.char('Yotech Setting Name', copy=False, required=True, readonly=False, select=True),
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