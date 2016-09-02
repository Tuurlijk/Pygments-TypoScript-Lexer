# -*- coding: utf-8 -*-
"""
    pygments.lexers.typoscript
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for TypoScript

    `TypoScriptLexer`
        A TypoScript lexer.

    `TypoScriptCssDataLexer`
        Lexer that highlights markers, constants and registers within css.

    `TypoScriptHtmlDataLexer`
        Lexer that highlights markers, constants and registers within html tags.

    version: 1.1.6

    :copyright: Copyright 2013-now by Donation Based Hosting.
    :license: BSD, see LICENSE for details.
"""
import re

from pygments.lexer import RegexLexer, include, bygroups, using
from pygments.token import Keyword, Text, Comment, Name, String, Number, \
                           Operator, Punctuation
from pygments.lexer import DelegatingLexer
from pygments.lexers.web import HtmlLexer, CssLexer


__all__ = ['TypoScriptLexer', 'TypoScriptCssDataLexer', 'TypoScriptHtmlDataLexer']

class TypoScriptCssDataLexer(RegexLexer):
    """
    Lexer that highlights markers, constants and registers within css blocks.

    """
    name = 'TypoScriptCssData'
    aliases = ['typoscriptcssdata']

    tokens = {
        'root': [
              # marker: ###MARK###
            (r'(.*)(###\w+###)(.*)', bygroups(String, Name.Constant, String)),
              # constant: {$some.constant}
            (r'(\{)(\$)((?:[\w\-_]+\.)*)([\w\-_]+)(\})',
                bygroups(String.Symbol, Operator, Name.Constant, Name.Constant, String.Symbol)), # constant
              # constant: {register:somevalue}
            (r'(.*)(\{)([\w\-_]+)(\s*:\s*)([\w\-_]+)(\})(.*)',
                bygroups(String, String.Symbol, Name.Constant, Operator, Name.Constant, String.Symbol, String)), # constant
              # whitespace
            (r'\s+', Text),
              # comments
            (r'/\*(?:(?!\*/).)*\*/', Comment),
            (r'(?<!(#|\'|"))(?:#(?!(?:[a-fA-F0-9]{6}|[a-fA-F0-9]{3}))[^\n#]+|//[^\n]*)', Comment),
              # other
            (r'[<>,:=\.\*%+\|]', String),
            (r'[\w"_\-!\/&;\(\)\{\}]+', String),
        ]
    }


class TypoScriptHtmlDataLexer(RegexLexer):
    """
    Lexer that highlights markers, constants and registers within html tags.

    """
    name = 'TypoScriptHtmlData'
    aliases = ['typoscripthtmldata']

    tokens = {
        'root': [
              # INCLUDE_TYPOSCRIPT
            (r'(INCLUDE_TYPOSCRIPT)', Name.Class),
              # Language label or extension resource FILE:... or LLL:... or EXT:...
            (r'(EXT|FILE|LLL):[^\}\n"]*', String),
              # marker: ###MARK###
            (r'(.*)(###\w+###)(.*)', bygroups(String, Name.Constant, String)),
              # constant: {$some.constant}
            (r'(\{)(\$)((?:[\w\-_]+\.)*)([\w\-_]+)(\})',
                bygroups(String.Symbol, Operator, Name.Constant, Name.Constant, String.Symbol)), # constant
              # constant: {register:somevalue}
            (r'(.*)(\{)([\w\-_]+)(\s*:\s*)([\w\-_]+)(\})(.*)',
                bygroups(String, String.Symbol, Name.Constant, Operator, Name.Constant, String.Symbol, String)), # constant
              # whitespace
            (r'\s+', Text),
              # other
            (r'[<>,:=\.\*%+\|]', String),
            (r'[\w"_\-!\/&;\(\)\{\}#]+', String),
        ]
    }

class TypoScriptLexer(RegexLexer):
    """
    Lexer for TypoScript code.

    http://docs.typo3.org/typo3cms/TyposcriptReference/
    """
    name = 'TypoScript'
    aliases = ['typoscript']
    filenames = ['*.ts','*.txt']
    mimetypes = ['text/x-typoscript']

    flags = re.DOTALL | re.MULTILINE

    tokens = {
        'root': [
            include('comment'),
            include('constant'),
            include('html'),
            include('label'),
            include('whitespace'),
            include('keywords'),
            include('punctuation'),
            include('operator'),
            include('structure'),
            include('literal'),
            include('other'),
        ],
        'keywords': [
              # Conditions
            (r'(\[)(?i)(browser|compatVersion|dayofmonth|dayofweek|dayofyear|device|ELSE|END|GLOBAL|globalString|globalVar|hostname|hour|IP|language|loginUser|loginuser|minute|month|page|PIDinRootline|PIDupinRootline|system|treeLevel|useragent|userFunc|usergroup|version)([^\]]*)(\])', bygroups(String.Symbol, Name.Constant, Text, String.Symbol)),
              # Functions
            (r'(?=[\w\-_])(HTMLparser|HTMLparser_tags|addParams|cache|encapsLines|filelink|if|imageLinkWrap|imgResource|makelinks|numRows|numberFormat|parseFunc|replacement|round|select|split|stdWrap|strPad|tableStyle|tags|textStyle|typolink)(?![\w\-_])', Name.Function),
              # Toplevel objects and _*
            (r'(?:(=?\s*<?\s+|^\s*))(cObj|field|config|content|constants|FEData|file|frameset|includeLibs|lib|page|plugin|register|resources|sitemap|sitetitle|styles|temp|tt_[^:\.\n\s]*|types|xmlnews|INCLUDE_TYPOSCRIPT|_CSS_DEFAULT_STYLE|_DEFAULT_PI_VARS|_LOCAL_LANG)(?![\w\-_])',
              bygroups(Operator, Name.Builtin)),
              # Content objects
            (r'(?=[\w\-_])(CASE|CLEARGIF|COA|COA_INT|COBJ_ARRAY|COLUMNS|CONTENT|CTABLE|EDITPANEL|FILE|FILES|FLUIDTEMPLATE|FORM|HMENU|HRULER|HTML|IMAGE|IMGTEXT|IMG_RESOURCE|LOAD_REGISTER|MEDIA|MULTIMEDIA|OTABLE|PAGE|QTOBJECT|RECORDS|RESTORE_REGISTER|SEARCHRESULT|SVG|SWFOBJECT|TEMPLATE|TEXT|USER|USER_INT)(?![\w\-_])', Name.Class),
              # Menu states
            (r'(?=[\w\-_])(ACT|ACTIFSUB|ACTIFSUBRO|ACTRO|CUR|CURIFSUB|CURIFSUBRO|CURRO|IFSUB|IFSUBRO|NO|SPC|USERDEF1|USERDEF1RO|USERDEF2|USERDEF2RO|USR|USRRO)', Name.Class),
              # Menu objects
            (r'(?=[\w\-_])(GMENU|GMENU_FOLDOUT|GMENU_LAYERS|IMGMENU|IMGMENUITEM|JSMENU|JSMENUITEM|TMENU|TMENUITEM|TMENU_LAYERS)', Name.Class),
              # PHP objects
            (r'(?=[\w\-_])(PHP_SCRIPT(_EXT|_INT)?)', Name.Class),
            (r'(?=[\w\-_])(userFunc)(?![\w\-_])', Name.Function),
        ],
        'whitespace': [
            (r'\s+', Text),
        ],
        'html':[
            (r'<[^\s][^\n>]*>', using(TypoScriptHtmlDataLexer)),
            (r'&[^;\n]*;', String),
            (r'(_CSS_DEFAULT_STYLE)(\s*)(\()(?s)(.*(?=\n\)))',
              bygroups(Name.Class, Text, String.Symbol, using(TypoScriptCssDataLexer))),
        ],
        'literal': [
            (r'0x[0-9A-Fa-f]+t?',Number.Hex),
            #(r'[0-9]*\.[0-9]+([eE][0-9]+)?[fd]?\s*(?:[^=])', Number.Float),
            (r'[0-9]+', Number.Integer),
            (r'(###\w+###)', Name.Constant),
        ],
        'label': [
              # Language label or extension resource FILE:... or LLL:... or EXT:...
            (r'(EXT|FILE|LLL):[^\}\n"]*', String),
              # Path to a resource
            (r'(?![^\w\-_])([\w\-_]+(?:/[\w\-_]+)+/?)([^\s]*\n)', bygroups(String, String)),
        ],
        'punctuation': [
            (r'[,\.]', Punctuation),
        ],
        'operator': [
            (r'[<>,:=\.\*%+\|]', Operator),
        ],
        'structure': [
              # Brackets and braces
            (r'[\{\}\(\)\[\]\\\\]', String.Symbol),
        ],
        'constant': [
              # Constant: {$some.constant}
            (r'(\{)(\$)((?:[\w\-_]+\.)*)([\w\-_]+)(\})',
                bygroups(String.Symbol, Operator, Name.Constant, Name.Constant, String.Symbol)), # constant
              # Constant: {register:somevalue}
            (r'(\{)([\w\-_]+)(\s*:\s*)([\w\-_]+)(\})',
                bygroups(String.Symbol, Name.Constant, Operator, Name.Constant, String.Symbol)), # constant
              # Hex color: #ff0077
            (r'(#[a-fA-F0-9]{6}\b|#[a-fA-F0-9]{3}\b)', String.Char)
        ],
        'comment': [
            (r'(?<!(#|\'|"))(?:#(?!(?:[a-fA-F0-9]{6}|[a-fA-F0-9]{3}))[^\n#]+|//[^\n]*)', Comment),
            (r'/\*(?:(?!\*/).)*\*/', Comment),
            (r'(\s*#\s*\n)', Comment),
        ],
        'other': [
            (r'[\w"\-_!\/&;@]+', Text),
        ],
    }

