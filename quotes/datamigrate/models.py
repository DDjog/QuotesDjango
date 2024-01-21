#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateTimeField, ReferenceField, EmbeddedDocumentField, ListField, StringField


class Author(Document):
    fullname = StringField()
    #born_date = DateTimeField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField( StringField(max_length=60) )
    author = ReferenceField( Author )
    quote = StringField()


def find_quote_by_author( _fullname ):
    
    author = Author.objects( fullname = _fullname).first()
    
    if author == None:
        return None
    
    rslt = Quote.objects( author = author.id )
    
    return rslt

def find_single_tag( _tag ):
    
    rslt = Quote.objects( tags = _tag )
    
    if rslt == None:
        return None
    
    return rslt


def find_tags( _tags ):
    
    rslt = Quote.objects( tags__all = _tags )
    
    if rslt == None:
        return None
    
    return rslt    

