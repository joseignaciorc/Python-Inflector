#!/usr/bin/env python

# Copyright (c) 2006 Bermi Ferrer Martinez
# bermi a-t bermilabs - com
#
# See the end of this file for the free software, open source license
# (BSD-style).

import re
from .base import Base


class French (Base):
    """
    Inflector for pluralize and singularize English nouns.

    This is the default Inflector for the Inflector obj
    """

    def pluralize(self,word):
        for GRAMMAR_RULE in (self._ail_word, self._al_word, self._au_word, self._eil_word, self._eu_word, self._ou_word, self._s_word, self._x_word, self._z_word,
                             self._default):
            plural = GRAMMAR_RULE(word)
            if plural:
                return plural

    def _ail_word(self,word):
        if word.endswith("ail"):
            if word == "ail":
                return "aulx"
            elif word in (
            "bail", "corail", u"émail", "fermail", "soupirail", "travail", "vantail", "ventail", "vitrail"):
                return word[:-3] + "aux"
            return word + "s"

    def _al_word(self,word):
        if word.endswith("al"):
            if word in (
                    "bal", "carnaval", "chacal", "festival", u"récital", u"régal",
                    "bancal", "fatal", "fractal", "final", "morfal", "natal", "naval",
                    u"aéronaval",
                    u"anténatal", u"néonatal", u"périnatal", u"postnatal", u"prénatal",
                    "tonal", "atonal", "bitonal", "polytonal",
                    "corral", "deal", "goal", "autogoal", "revival", "serial", "spiritual", "trial",
                    "caracal", "chacal", "gavial", "gayal", "narval", "quetzal", "rorqual", "serval",
                    "metical", "rial", "riyal", "ryal",
                    "cantal", "emmental", "emmenthal",
                    u"floréal", "germinal", "prairial",
            ):
                return word + "s"
            return word[:-2] + "aux"

    def _au_word(self,word):
        if word.endswith("au"):
            if word in ("berimbau", "donau", "karbau", "landau", "pilau", "sarrau", "unau"):
                return word + "s"
            return word + "x"

    def _eil_word(self,word):
        if word.endswith("eil"):
            return "vieux" if word == "vieil" else word + "s"

    def _eu_word(self,word):
        if word.endswith("eu"):
            if word in ("bleu", u"émeu", "enfeu", "pneu", "rebeu"):
                return word + "s"
            return word + "x"

    def _ou_word(self,word):
        if word.endswith("ou"):
            if word in ("bijou", "caillou", "chou", "genou", "hibou", "joujou", "pou"):
                return word + "x"
            return word + "s"

    def _s_word(self,word):
        if word[-1] == "s":
            return word

    def _x_word(self,word):
        if word[-1] == "x":
            return word

    def _z_word(self,word):
        if word[-1] == "z":
            return word

    def _default(self,word):
        return word + "s"

    def singularize(self, word):
        '''Singularizes English nouns.'''

        word=word.lower()

        if word in set(["baux", "coraux", "émaux", "fermaux", "soupiraux", "travaux", "vantaux", "ventaux", "vitraux"]):
            return word[:-3] + "ail"
        if word.endswith("als") or word.endswith("aux"):
            return  word[:-3]+"al"
        if word.endswith == "vieux":
            return "vieil"
        if word.endswith("x") or word.endswith("s"):
            return word[:-1]



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
