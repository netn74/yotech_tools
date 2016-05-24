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

import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round, float_compare

import time
import datetime
from dateutil.relativedelta import relativedelta

import openerp
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools.translate import _
from openerp.osv import fields, osv

import logging
_logger = logging.getLogger(__name__)

class account_config_settings(osv.osv_memory):
    _inherit = 'account.config.settings'

    _columns = {
        'default_local_property_account_payable': fields.property(
            type='many2one',
            relation='account.account',
            string="Default local Account Payable",
            domain="[('type', '=', 'payable')]",
            help="Default local property_account_payable"),
        'default_local_property_account_receivable': fields.property(
            type='many2one',
            relation='account.account',
            string="Default local Account Receivable",
            domain="[('type', '=', 'receivable')]",
            help="Default local property_account_receivable"),
        'default_local_property_account_position': fields.property(
            type='many2one',
            relation='account.fiscal.position',
            string="Default local Fiscal Position",
            help="Default local property_account_position",),
        'default_local_property_payment_term': fields.property(
            type='many2one',
            relation='account.payment.term',
            string ='Default local Customer Payment Term',
            help="Default local property_payment_term"),

        'default_property_account_payable': fields.property(
            type='many2one',
            relation='account.account',
            string="Default Account Payable",
            domain="[('type', '=', 'payable')]",
            help="Default property_account_payable"),
        'default_property_account_receivable': fields.property(
            type='many2one',
            relation='account.account',
            string="Default Account Receivable",
            domain="[('type', '=', 'receivable')]",
            help="Default property_account_receivable"),
        'default_property_account_position': fields.property(
            type='many2one',
            relation='account.fiscal.position',
            string="Default Fiscal Position",
            help="Default property_account_position",),
        'default_property_payment_term': fields.property(
            type='many2one',
            relation='account.payment.term',
            string ='Default Customer Payment Term',
            help="Default property_payment_term")
    }

