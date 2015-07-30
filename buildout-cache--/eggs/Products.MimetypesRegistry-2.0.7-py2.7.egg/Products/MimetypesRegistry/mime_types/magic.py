"""
magic.py

 Initial Author: Jason Petrone <jp@demonseed.net>

 Updated by Gabriel Wicke <groups@gabrielwicke.de>
    Thu Oct 16 23:00:03 CEST 2003
    with magic data from gnome-vfs-mime-magic

"""
__version__ = '$Revision: 1.2 $'[11:-2]

import struct
import string


magic = [

    [0, 'string', '=', '%PDF-', 'application/pdf'],
    [0, 'string', '=', '\177ELF', 'application/x-executable'],
    [0, 'string', '=', '\004%!', 'application/postscript'],
    [0, 'string', '=', '\000\000\001\272', 'video/mpeg'],
    [0, 'string', '=', '\000\000\001\263', 'video/mpeg'],
    [0, 'string', '=', '\x47\x3f\xff\x10', 'video/mpeg'],
    [0, 'string', '=', '\377\330\377', 'image/jpeg'],
    [0, 'string', '=', '\xed\xab\xee\xdb', 'application/x-rpm'],
    [0, 'string', '=', 'Rar!', 'application/x-rar'],
    [257, 'string', '=', 'ustar\0', 'application/x-tar'],
    [257, 'string', '=', 'ustar\040\040\0', 'application/x-gtar'],
    # the following detection of OOo is according to
    # http://books.evc-cit.info/oobook/ch01.html
    # and some heuristics found in hexeditor. if theres a better way to detect,
    # we should replace the signatures below.
    # best would to just read and evaluate the manifest file of the zip, but
    # the magic tests are running on the first 8kB, so we cant unzip the
    # manifest in files >8kB.
    [30, 'string', '=', 'mimetypeapplication/vnd.sun.xml.writer',
     'application/vnd.sun.xml.writer'],
    [30, 'string', '=', 'mimetypeapplication/vnd.sun.xml.calc',
     'application/vnd.sun.xml.calc'],
    [30, 'string', '=', 'mimetypeapplication/vnd.sun.xml.draw',
     'application/vnd.sun.xml.draw'],
    [30, 'string', '=', 'mimetypeapplication/vnd.sun.xml.impress',
     'application/vnd.sun.xml.impress'],
    [30, 'string', '=', 'mimetypeapplication/vnd.sun.xml.chart',
     'application/vnd.sun.xml.chart'],
    [30, 'string', '=', 'mimetypeapplication/vnd.sun.xml.global',
     'application/vnd.sun.xml.global'],
    # zip works now, after we have it with lower priority than OOo
    [0, 'string', '=', 'PK\003\004', 'application/zip'],
    [0, 'string', '=', 'GIF8', 'image/gif'],
    [4, 'string', '=', 'moov', 'video/quicktime'],
    [4, 'string', '=', 'mdat', 'video/quicktime'],
    [8, 'string', '=', 'mp42', 'video/quicktime'],
    [12, 'string', '=', 'mdat', 'video/quicktime'],
    [36, 'string', '=', 'mdat', 'video/quicktime'],
    [0, 'belong', '=', '0x3026b275', 'video/x-ms-asf'],
    [0, 'string', '=', 'ASF ', 'audio/x-ms-asx'],
    [0, 'string', '=', '<ASX', 'audio/x-ms-asx'],
    [0, 'string', '=', '<asx', 'audio/x-ms-asx'],
    [0, 'string', '=', 'MThd', 'audio/x-midi'],
    [0, 'string', '=', 'IMPM', 'audio/x-it'],
    [2, 'string', '=', '-lh0-', 'application/x-lha'],
    [2, 'string', '=', '-lh1-', 'application/x-lha'],
    [2, 'string', '=', '-lz4-', 'application/x-lha'],
    [2, 'string', '=', '-lz5-', 'application/x-lha'],
    [2, 'string', '=', '-lzs-', 'application/x-lha'],
    [2, 'string', '=', '-lh\40-', 'application/x-lha'],
    [2, 'string', '=', '-lhd-', 'application/x-lha'],
    [2, 'string', '=', '-lh2-', 'application/x-lha'],
    [2, 'string', '=', '-lh3-', 'application/x-lha'],
    [2, 'string', '=', '-lh4-', 'application/x-lha'],
    [2, 'string', '=', '-lh5-', 'application/x-lha'],
    [20, 'string', '=', '\375\304\247\334', 'application/x-zoo'],
    [0, 'string', '=', 'StuffIt ', 'application/x-stuffit'],
    [11,
     'string',
     '=',
     'must be converted with BinHex',
     'application/mac-binhex40'],
    [102, 'string', '=', 'mBIN', 'application/x-macbinary'],
    [4, 'string', '=', 'gtktalog ', 'application/x-gtktalog'],
    [0, 'string', '=', 'diff ', 'text/x-patch'],
    [0, 'string', '=', 'Index:', 'text/x-patch'],
    [0, 'string', '=', '*** ', 'text/x-patch'],
    [0, 'string', '=', 'Only in ', 'text/x-patch'],
    [0, 'string', '=', 'Common subdirectories: ', 'text/x-patch'],
    [0, 'string', '=', 'FONT', 'application/x-font-vfont'],
    [0, 'string', '=', 'IIN1', 'image/tiff'],
    [0, 'string', '=', 'MM\x00\x2a', 'image/tiff'],
    [0, 'string', '=', 'II\x2a\x00', 'image/tiff'],
    [0, 'string', '=', '\x89PNG', 'image/png'],
    [0,
     'string',
     '=',
     '8BPS\ \ \000\000\000\000 &0xffffffff0000ffffffff',
     'image/x-psd'],
    [0, 'string', '=', '#LyX', 'text/x-lyx'],
    [0, 'string', '=', 'DCMw', 'application/dicom'],
    [0, 'string', '=', 'gimp xcf', 'image/x-xcf'],
    [0, 'belong', '=', '0x59a66a95', 'image/x-sun-raster'],
    [0, 'belong', '=', '0x01da0000 &0xfcfeffff', 'image/x-sgi'],
    [0, 'belong', '=', '0xb168de3a', 'image/x-pcx'],
    [0, 'string', '=', '\x28\x00\x00\x00', 'image/x-dib'],
    [0, 'string', '=', 'SIMPLE  =', 'image/x-fits'],
    [0, 'belong', '=', '0x46506978', 'image/x-fpx'],
    [0, 'belong', '=', '0x00000200', 'image/x-icb'],
    [0, 'belong', '=', '0x53445058', 'image/dpx'],
    [0, 'string', '=', '[Desktop Entry]', 'application/x-gnome-app-info'],
    [0, 'string', '=', '[X-GNOME-Metatheme]', 'application/x-gnome-theme'],
    [0,
     'string',
     '=',
     '<nautilus_object nautilus_link',
     'application/x-nautilus-link'],
    [0, 'string', '=', 'URL:', 'application/x-gmc-link'],
    [0, 'string', '=', '/* XPM */', 'image/x-xpixmap'],
    [0, 'string', '=', '<!DOCTYPE xbel', 'application/xbel'],
    [0, 'string', '=', '<xbel', 'application/xbel'],
    [0,
     'string',
     '=',
     '<!DOCTYPE NETSCAPE-Bookmark-file-1\>',
     'application/x-mozilla-bookmarks'],
    [0,
     'string',
     '=',
     '<!DOCTYPE NETSCAPE-Bookmark-file-1\>',
     'application/x-netscape-bookmarks'],
    [0,
     'string',
     '=',
     '<ephy_bookmarks        ',
     'application/x-epiphany-bookmarks'],
    [0, 'string', '=', '<!DOCTYPE svg', 'image/svg+xml'],
    [0, 'string', '=', '<svg', 'image/svg+xml'],
    [0, 'string', '=', '<?php', 'application/x-php'],
    [0, 'string', '=', '<smil\>', 'application/smil'],
    [0, 'string', '=', '<SMIL\>', 'application/smil'],
    [0, 'string', '=', '<!DOCTYPE HTML', 'text/html'],
    [0, 'string', '=', '<!DOCTYPE html', 'text/html'],
    [0, 'string', '=', '<!doctype html', 'text/html'],
    [0, 'string', '=', '<!doctype Html', 'text/html'],
    [0, 'string', '=', '<!doctype HTML', 'text/html'],
    [10, 'string', '=', '<HEAD', 'text/html'],
    [10, 'string', '=', '<head', 'text/html'],
    [16, 'string', '=', '<TITLE', 'text/html'],
    [16, 'string', '=', '<title', 'text/html'],
    [10, 'string', '=', '<html', 'text/html'],
    [0, 'string', '=', '<HTML', 'text/html'],
    [0, 'string', '=', '<dia:diagram', 'application/x-dia-diagram'],
    [0, 'string', '=', '<abiword', 'application/x-abiword'],
    [0, 'string', '=', '<\!DOCTYPE abiword', 'application/x-abiword'],
    [0, 'string', '=', 'gmr:Workbook', 'application/x-gnumeric'],
    [0, 'string', '=', '<?xml', 'text/xml'],
    [0, 'string', '=', '{\\rtf', 'application/rtf'],
    [0, 'string', '=', '#!/bin/sh', 'text/x-sh'],
    [0, 'string', '=', '#!/bin/bash', 'text/x-sh'],
    [0, 'string', '=', '#!/bin/csh', 'text/x-csh'],
    [0, 'string', '=', '#!/bin/ksh', 'application/x-shellscript'],
    [0, 'string', '=', '#!/bin/perl', 'text/x-perl'],
    [0, 'string', '=', '#!/bin/zsh', 'application/x-shellscript'],
    [1, 'string', '=', '/bin/sh', 'text/x-sh'],
    [1, 'string', '=', '/bin/bash', 'text/x-sh'],
    [1, 'string', '=', '/bin/csh', 'text/x-csh'],
    [1, 'string', '=', '/bin/ksh', 'application/x-shellscript'],
    [1, 'string', '=', '/bin/perl', 'text/x-perl'],
    [0, 'string', '=', 'BEGIN:VCARD', 'text/x-vcard'],
    [0, 'string', '=', 'BEGIN:VCALENDAR', 'text/calendar'],
    [8, 'string', '=', 'CDR vrsn', 'application/vnd.corel-draw'],
    [8, 'string', '=', 'AVI ', 'video/x-msvideo'],
    [0, 'string', '=', 'MOVI', 'video/x-sgi-movie'],
    [0, 'string', '=', '.snd', 'audio/basic'],
    [8, 'string', '=', 'AIFC', 'audio/x-aifc'],
    [8, 'string', '=', 'AIFF', 'audio/x-aiff'],
    [0, 'string', '=', '.ra\375', 'audio/vnd.rn-realaudio'],
    [0, 'belong', '=', '0x2e7261fd', 'audio/vnd.rn-realaudio'],
    [0, 'string', '=', '.RMF', 'audio/x-pn-realaudio'],
    [8, 'string', '=', 'WAVE', 'audio/x-wav'],
    [8, 'string', '=', 'WAV ', 'audio/x-wav'],
    [0, 'string', '=', 'ID3', 'audio/mpeg'],
    [0, 'string', '=', '0xfff0', 'audio/mpeg'],
    [0, 'string', '=', '\x00\x00\x01\xba', 'video/mpeg'],
    [8, 'string', '=', 'CDXA', 'video/mpeg'],
    [0, 'belong', '=', '0x000001ba', 'video/mpeg'],
    [0, 'belong', '=', '0x000001b3', 'video/mpeg'],
    [0, 'string', '=', 'RIFF', 'audio/x-riff'],
    [0, 'string', '=', 'OggS   ', 'audio/ogg'],
    [0, 'string', '=', 'pnm:\/\/', 'audio/vnd.rn-realaudio'],
    [0, 'string', '=', 'rtsp:\/\/', 'audio/vnd.rn-realaudio'],
    [0, 'string', '=', 'SIT!', 'application/x-stuffit'],
    [0, 'string', '=', '\312\376\272\276', 'application/x-java'],
    [0, 'string', '=', 'Joy!', 'application/x-pef-executable'],
    [4, 'string', '=', '\x11\xAF', 'video/x-flic'],
    [4, 'string', '=', '\x12\xAF', 'video/x-flic'],
    [0, 'string', '=', '\x31\xbe\x00\x00', 'application/msword'],
    [0, 'string', '=', 'PO^Q`', 'application/msword'],
    [0, 'string', '=', '\376\067\0\043', 'application/msword'],
    [0, 'string', '=', '\320\317\021\340\241\261', 'application/msword'],
    [0, 'string', '=', '\333\245-\0\0\0', 'application/msword'],
    [0,
     'string',
     '=',
     'Microsoft Excel 5.0 Worksheet',
     'application/vnd.ms-excel'],
    [0, 'string', '=', 'Biff5', 'application/vnd.ms-excel'],
    [0,
     'string',
     '=',
     '*BEGIN SPREADSHEETS    ',
     'application/x-applix-spreadsheet'],
    [0,
     'string',
     '=',
     '*BEGIN SPREADSHEETS    ',
     'application/x-applix-spreadsheet'],
    [0, 'string', '=', '\x00\x00\x02\x00', 'application/vnd.lotus-1-2-3'],
    [0, 'belong', '=', '0x00001a00', 'application/vnd.lotus-1-2-3'],
    [0, 'belong', '=', '0x00000200', 'application/vnd.lotus-1-2-3'],
    [0, 'string', '=', 'PSID', 'audio/prs.sid'],
    [31, 'string', '=', 'Oleo', 'application/x-oleo'],
    [0, 'string', '=', 'FFIL', 'application/x-font-ttf'],
    [65, 'string', '=', 'FFIL', 'application/x-font-ttf'],
    [0, 'string', '=', 'LWFN', 'application/x-font-type1'],
    [65, 'string', '=', 'LWFN', 'application/x-font-type1'],
    [0, 'string', '=', 'StartFont', 'application/x-font-sunos-news'],
    [0, 'string', '=', '\x13\x7A\x29', 'application/x-font-sunos-news'],
    [8, 'string', '=', '\x13\x7A\x2B', 'application/x-font-sunos-news'],
    [0, 'string', '=', '%!PS-AdobeFont-1.', 'application/x-font-type1'],
    [6, 'string', '=', '%!PS-AdobeFont-1.', 'application/x-font-type1'],
    [0, 'string', '=', '%!FontType1-1.', 'application/x-font-type1'],
    [6, 'string', '=', '%!FontType1-1.', 'application/x-font-type1'],
    [0, 'string', '=', 'STARTFONT\040', 'application/x-font-bdf'],
    [0, 'string', '=', '\001fcp', 'application/x-font-pcf'],
    [0, 'string', '=', 'D1.0\015', 'application/x-font-speedo'],
    [0, 'string', '=', '\x14\x02\x59\x19', 'application/x-font-libgrx'],
    [0, 'string', '=', '\xff\x46\x4f\x4e', 'application/x-font-dos'],
    [7, 'string', '=', '\x00\x45\x47\x41', 'application/x-font-dos'],
    [7, 'string', '=', '\x00\x56\x49\x44', 'application/x-font-dos'],
    [0, 'string', '=', '\<MakerScreenFont', 'application/x-font-framemaker'],
    [0, 'string', '=', '\000\001\000\000\000', 'application/x-font-ttf'],
    [1, 'string', '=', 'WPC', 'application/x-wordperfect'],
    [0, 'string', '=', 'ID;', 'text/spreadsheet'],
    [0, 'string', '=', 'MZ', 'application/x-ms-dos-executable'],
    [0, 'string', '=', '%!', 'application/postscript'],
    [0, 'string', '=', 'BZh', 'application/x-bzip'],
    [0, 'string', '=', '\x1f\x8b', 'application/x-gzip'],
    [0, 'string', '=', '\037\235', 'application/x-compress'],
    [0, 'string', '=', '\367\002', 'application/x-dvi'],
    [0, 'string', '=', '\367\203', 'application/x-font-tex'],
    [0, 'string', '=', '\367\131', 'application/x-font-tex'],
    [0, 'string', '=', '\367\312', 'application/x-font-tex'],
    [2, 'string', '=', '\000\022', 'application/x-font-tex-tfm'],
    [0, 'string', '=', '\x36\x04', 'application/x-font-linux-psf'],
    [0, 'string', '=', 'FWS', 'application/x-shockwave-flash'],
    [0, 'string', '=', 'CWS', 'application/x-shockwave-flash'],
    [0, 'string', '=', 'NSVf', 'video/x-nsv'],
    [0, 'string', '=', 'BMxxxx\000\000 &0xffff00000000ffff', 'image/bmp'],
    [0, 'string', '=', 'Return-Path:', 'message/rfc822'],
    [0, 'string', '=', 'Path:', 'message/news'],
    [0, 'string', '=', 'Xref:', 'message/news'],
    [0, 'string', '=', 'From:', 'message/rfc822'],
    [0, 'string', '=', 'Received:', 'message/rfc822'],
    [0, 'string', '=', '[playlist]', 'audio/x-scpls'],
    [0, 'string', '=', '[Reference]', 'video/x-ms-asf'],
    [0, 'string', '=', 'fLaC', 'application/x-flac'],
    [32769, 'string', '=', 'CD001', 'application/x-cd-image'],
    [37633, 'string', '=', 'CD001', 'application/x-cd-image'],
    [32776, 'string', '=', 'CDROM', 'application/x-cd-image'],
    [0, 'string', '=', 'OTTO', 'application/x-font-otf'],
    [54, 'string', '=', 'S T O P', 'application/x-ipod-firmware'],
    [0, 'string', '=', 'BLENDER', 'application/x-blender'],
    [0, 'string', '=', 'import ', 'text/x-python'],
]

magicNumbers = []


def strToNum(n):
    val = 0
    col = long(1)
    if n[:1] == 'x':
        n = '0' + n
    if n[:2] == '0x':
        # hex
        n = string.lower(n[2:])
        while len(n) > 0:
            l = n[len(n) - 1]
            val = val + string.hexdigits.index(l) * col
            col = col * 16
            n = n[:len(n) - 1]
    elif n[0] == '\\':
        # octal
        n = n[1:]
        while len(n) > 0:
            l = n[len(n) - 1]
            if ord(l) < 48 or ord(l) > 57:
                break
            val = val + int(l) * col
            col = col * 8
            n = n[:len(n) - 1]
    else:
        val = string.atol(n)
    return val


class magicTest:

    def __init__(self, offset, t, op, value, msg, mask=None):
        if t.count('&') > 0:
            mask = strToNum(t[t.index('&') + 1:])
            t = t[:t.index('&')]
        if isinstance(offset, type('a')):
            self.offset = strToNum(offset)
        else:
            self.offset = offset
        self.type = t
        self.msg = msg
        self.subTests = []
        self.op = op
        self.mask = mask
        self.value = value

    def test(self, data):
        if self.mask:
            data = data & self.mask
        if self.op == '=':
            if self.value == data:
                return self.msg
        elif self.op == '<':
            pass
        elif self.op == '>':
            pass
        elif self.op == '&':
            pass
        elif self.op == '^':
            pass
        return None

    def compare(self, data):
        # print str([self.type, self.value, self.msg])
        try:
            if self.type == 'string':
                c = ''
                s = ''
                for i in range(0, len(self.value) + 1):
                    if i + self.offset > len(data) - 1:
                        break
                    s = s + c
                    [c] = struct.unpack('c', data[self.offset + i])
                data = s
            elif self.type == 'short':
                [data] = struct.unpack('h', data[self.offset: self.offset + 2])
            elif self.type == 'leshort':
                [data] = struct.unpack(
                    '<h',
                    data[
                        self.offset: self.offset +
                        2])
            elif self.type == 'beshort':
                [data] = struct.unpack(
                    '>H',
                    data[
                        self.offset: self.offset +
                        2])
            elif self.type == 'long':
                [data] = struct.unpack('l', data[self.offset: self.offset + 4])
            elif self.type == 'lelong':
                [data] = struct.unpack(
                    '<l',
                    data[
                        self.offset: self.offset +
                        4])
            elif self.type == 'belong':
                [data] = struct.unpack(
                    '>l',
                    data[
                        self.offset: self.offset +
                        4])
            else:
                # print 'UNKNOWN TYPE: ' + self.type
                pass
        except:
            return None

#    print str([self.msg, self.value, data])
        return self.test(data)


def guessMime(data):
    for test in magicNumbers:
        m = test.compare(data)
        if m:
            return m
    # no matching, magic number.
    return

for m in magic:
    magicNumbers.append(magicTest(m[0], m[1], m[2], m[3], m[4]))
