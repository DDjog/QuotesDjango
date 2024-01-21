#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import connect
import psycopg2

from models import Author, Quote


def load_data(filename):
    with open(filename, "r", encoding='utf-8') as f:
        return json.load(f)

def delete_data():
    Quote.drop_collection()
    Author.drop_collection()

def put_data_to_mongo():
    authors_data = load_data("authors.json")
    quotes_data = load_data("quotes.json")
        
    for a in authors_data:
        adata = Author ( **a )
        adata.save()
               
    for q in quotes_data:
        qdata = Quote()
        
        _fn=None
        if type(q["author"]) is str:
            _fn = q["author"]
        if type(q["author"]) is list:
            _fn = q["author"][0]       
        
        qdata.author = Author.objects( fullname = _fn ).first()
        qdata.tags = q["tags"]
        qdata.quote = q["quote"]
        qdata.save()

    
def get_id_for_author(fullname):

    pg_url = "postgresql://worker:worker@localhost:5432/testdbORM"    
    
    rows=None
    
    with psycopg2.connect( pg_url ) as connection:
        cursor = connection.cursor()

        cursor.execute( """select id from quotesapp_author where fullname = %s;""", [ str(fullname) ] )
        rows = cursor.fetchall()

    if rows == []:
        return None
    return rows[0][0]

def get_id_for_tag(name):

    pg_url = "postgresql://worker:worker@localhost:5432/testdbORM"    
    
    rows=None
    
    with psycopg2.connect( pg_url ) as connection:
        cursor = connection.cursor()

        cursor.execute( """select id from quotesapp_tag where name = %s;""", [ str(name) ] )
        rows = cursor.fetchall()

    if rows == []:
        return None
    return rows[0][0]


def copy_data_from_mongo_to_postgres():
    
    pg_url = "postgresql://worker:worker@localhost:5432/testdbORM"    

    
    # copy author to PG table quotesapp_author
    # with id>=100
    with psycopg2.connect( pg_url ) as connection:

        cursor = connection.cursor()

        aid=100
    
        for a in Author.objects():
            
            #print(a.fullname)
            #print(a.born_date)
            #print(a.born_location)
            #print(a.description)
            #print("-" * 64)
            
            cursor.execute("""insert into quotesapp_author (id, fullname, born_date, born_location, description)
                            values (%s, %s, %s, %s, %s);""", (str(aid), a.fullname, a.born_date, a.born_location, a.description) )
            aid=aid+1

    
    # tags list
    # with id>=100
    tags_list=[]
    for q in Quote.objects():
        #print(q.tags)
        for t in q.tags:
            if t not in tags_list:
                tags_list.append(t)
    #print(tags_list)
    
    with psycopg2.connect( pg_url ) as connection:
        cursor = connection.cursor()
        tid=100
        for t in tags_list:
            cursor.execute("""insert into quotesapp_tag (id, name)
                              values (%s, %s);""", ( str(tid), str(t) ) )
            print(t)
            tid=tid+1
            
        
    # copy quote to PG tables:  quotesapp_quote and quotesapp_quote_tags
    with psycopg2.connect( pg_url ) as connection:
        cursor = connection.cursor()
        
        qid=100
        qtid=100
        for q in Quote.objects():
            aid=get_id_for_author(q.author.fullname)

            cursor.execute("""insert into quotesapp_quote (id, quote, author_id)
                             values (%s, %s, %s);""", ( str(qid), str(q.quote), str(aid) ) )

            
            for t in q.tags:
                tid=get_id_for_tag( t )
                cursor.execute("""insert into quotesapp_quote_tags (id, quote_id, tag_id)
                                  values (%s, %s, %s);""", ( str(qtid), str(qid), str(tid) ) )
                qtid = qtid + 1
            
            
            qid = qid + 1
        

        
    