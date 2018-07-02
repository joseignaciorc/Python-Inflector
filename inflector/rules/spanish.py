#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
# Copyright (c) 2006 Bermi Ferrer Martinez
# Copyright (c) 2006 Carles Sadurní Anguita
#
# bermi a-t bermilabs - com
#
# See the end of this file for the free software, open source license
# (BSD-style).

import re
from .base import Base


class Spanish (Base):
    '''
    Inflector for pluralize and singularize Spanish nouns.
    '''

    irregular_words = {
        'base': 'bases',
        'carácter': 'caracteres',
        'champú': 'champús',
        'curriculum': 'currículos',
        'espécimen': 'especímenes',
        'jersey': 'jerséis',
        'memorándum': 'memorandos',
        'menú': 'menús',
        'no': 'noes',
        'país': 'países',
        'referéndum': 'referendos',
        'régimen': 'regímenes',
        'sándwich': 'sándwiches',
        'si': 'sis', # Nota musical ALERTA: ¡provoca efectos secundarios!
        'taxi': 'taxis', 
        'ultimátum': 'ultimatos',
        }

    # These words either have the same form in singular and plural, or have no singular form at all
    non_changing_words = [
        'lunes', 'martes', 'miércoles', 'jueves', 'viernes',
        'paraguas', 'tijeras', 'gafas', 'vacaciones', 'víveres',
        'cumpleaños', 'virus', 'atlas', 'sms', 'hummus',
    ]


    def pluralize(self, word):
        '''
        Pluralizes Spanish nouns.
        Input string can be Unicode (e.g. u"palabra"), or a str encoded in UTF-8 or Latin-1.
        Output string will be encoded the same way as the input.
        '''

        #word, origType = utils.unicodify(word)  # all internal calculations are done in Unicode

        rules = [
            ['(?i)([aeiou])x$', '\\1x'],
            # This could fail if the word is oxytone.
            ['(?i)([áéíóú])([ns])$', '|1\\2es'],
            ['(?i)(^[bcdfghjklmnñpqrstvwxyz]*)an$', '\\1anes'],  # clan->clanes
            ['(?i)([áéíóú])s$', '|1ses'],
            ['(?i)(^[bcdfghjklmnñpqrstvwxyz]*)([aeiou])([ns])$', '\\1\\2\\3es'],  # tren->trenes
            ['(?i)([aeiouáéó])$', '\\1s'],  # casa->casas, padre->padres, papá->papás
            ['(?i)([aeiou])s$', '\\1s'],    # atlas->atlas, virus->virus, etc.
            ['(?i)([éí])(s)$', '|1\\2es'],  # inglés->ingleses
            ['(?i)z$', 'ces'],              # luz->luces
            ['(?i)([íú])$', '\\1es'],       # ceutí->ceutíes, tabú->tabúes
            ['(?i)(ng|[wckgtp])$', '\\1s'], # Anglicismos como puenting, frac, crack, show (En que casos podría fallar esto?)
            ['(?i)$', 'es']  # ELSE +es (v.g. árbol->árboles)
        ]

        lower_cased_word = word.lower()

        for uncountable_word in self.non_changing_words:
            if lower_cased_word[-1 * len(uncountable_word):] == uncountable_word:
                return word

        for irregular_singular, irregular_plural in self.irregular_words.items():
            match = re.search('(?i)(^' + irregular_singular + ')$', word, re.IGNORECASE)
            if match:
                result = re.sub('(?i)' + irregular_singular + '$', match.expand('\\1')[0] + irregular_plural[1:], word)
                return result

        for rule in rules:
            match = re.search(rule[0], word, re.IGNORECASE)
            if match:
                groups = match.groups()
                replacement = rule[1]
                if re.match('\|', replacement):
                    for k in range(1, len(groups)):
                        replacement = replacement.replace('|' + k, self.string_replace(groups[k - 1], 'ÁÉÍÓÚáéíóú', 'AEIOUaeio'))

                result = re.sub(rule[0], replacement, word)
                # Esto acentúa los sustantivos que al pluralizarse se
                # convierten en esdrújulos como esmóquines, jóvenes...
                match = re.search('(?i)([aeiou]).{1,3}([aeiou])nes$', result)

                if match and len(match.groups()) > 1 and not re.search('(?i)[áéíóú]', word):
                    result = result.replace(match.group(0), self.string_replace(
                        match.group(1), 'AEIOUaeio', 'ÁÉÍÓÚáéíóú') + match.group(0)[1:])

                return result

        return word


    def singularize(self, word):
        '''
        Singularizes Spanish nouns.
        Input string can be Unicode (e.g. u"palabras"), or a str encoded in UTF-8 or Latin-1.
        Output string will be encoded the same way as the input.
        '''

     # all internal calculations are done in Unicode

        rules = [
            [r'(?i)^([bcdfghjklmnñpqrstvwxyz]*)([aeiou])([ns])es$', '\\1\\2\\3'],
            [r'(?i)([aeiou])([ns])es$', '~1\\2'],
            [r'(?i)shes$', 'sh'],             # flashes->flash
            [r'(?i)oides$', 'oide'],          # androides->androide
            [r'(?i)(sis|tis|xis)$', '\\1'],   # crisis, apendicitis, praxis
            [r'(?i)(é)s$', '\\1'],            # bebés->bebé
            [r'(?i)(ces)$', 'z'],             # luces->luz
            [r'(?i)([^e])s$', '\\1'],         # casas->casa
            [r'(?i)([bcdfghjklmnñprstvwxyz]{2,}e)s$', '\\1'],  # cofres->cofre
            [r'(?i)([ghñptv]e)s$', '\\1'],    # llaves->llave, radiocasetes->radiocasete
            [r'(?i)jes$', 'je'],              # ejes->eje
            [r'(?i)ques$', 'que'],            # tanques->tanque
            [r'(?i)es$', '']                  # ELSE remove _es_  monitores->monitor
        ]

        lower_cased_word = word.lower()

        for uncountable_word in self.non_changing_words:
            if lower_cased_word[-1 * len(uncountable_word):] == uncountable_word:
                return word

        for irregular_singular, irregular_plural in self.irregular_words.items():
            match = re.search('(^' + irregular_plural + ')$', word, re.IGNORECASE)
            if match:
                result = re.sub('(?i)' + irregular_plural + '$', match.expand('\\1')[0] + irregular_singular[1:], word)
                return result

        for rule in rules:
            match = re.search(rule[0], word, re.IGNORECASE)
            if match:
                groups = match.groups()
                replacement = rule[1]
                if re.match('~', replacement):
                    for k in range(1, len(groups)):
                        replacement = replacement.replace('~' + k, self.string_replace(groups[k - 1], 'AEIOUaeio', 'ÁÉÍÓÚáéíóú'))

                result = re.sub(rule[0], replacement, word)
                # Esta es una posible solución para el problema de dobles
                # acentos. Un poco guarrillo pero funciona
                match = re.search('(?i)([áéíóú]).*([áéíóú])', result)

                if match and len(match.groups()) > 1 and not re.search('(?i)[áéíóú]', word):
                    result = self.string_replace(
                        result, 'ÁÉÍÓÚáéíóú', 'AEIOUaeio')

                return result

        return word


# Copyright (c) 2006 Bermi Ferrer Martinez
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.

