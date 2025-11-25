#!/usr/bin/python3
# coding: latin-1
blob = """AAAAAAAAAAAAAAAAA’Yû7x<ð§€kn©çPTþ=ß–EÚ(H^z	Ñ¢“z²ùÈŠÇÒçÍp2î“~ú§8¦±òæ¼ýïôÌ¹’c£ýnÕ²¾pˆ-	}Á_&mÖþ®K’>éÉZ~ËìÞoÐcžØ—äBz/IOH<õ*/ªVšu±rÝÙác‹ÈíY0"""
f = open(__file__, 'rb')
data = f.read()
if b'\x93~' in data:
    print("MD5 is perfectly secure!")
else:
    print("Use SHA-256 instead!")