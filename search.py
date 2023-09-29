import psycopg2
from autocorrect import Speller
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, text, case, func


development = False


def text_search(search: str):
    def connect_psql():
        if development == True:
            try:
                conn = psycopg2.connect(database="restore_Oct_13",
                                        host="localhost",
                                        user="postgres",
                                        password="password")
                print("connected")
            except:
                print("failed")
            cursor = conn.cursor()
            return cursor, conn

        if development == False:
            conn = psycopg2.connect(database="defaultdb",
                                    host="db-postgresql-fra1-kyr-0001-do-user-12476250-0.b.db.ondigitalocean.com",
                                    user="doadmin",
                                    password="AVNS_SbC_UqXYG665R47kxY4",
                                    port=25060,
                                    sslmode='require')
            cursor = conn.cursor()
            return cursor, conn
    cursor, conn = connect_psql()
    spell = Speller()
    corrected = (spell(search))
    if corrected == search:
        search_term = search
    else:
        search_term = corrected
    sql_query = """
        SELECT item_id, url, case_title, importance_number, judgment_date, facts, conclusion, ts_headline('english', entire_text, query, 'StartSel = <b>, StopSel = </b>, ShortWord = 3, MinWords = 50, MaxWords = 60') as entire_text_highlights
        FROM (
            SELECT item_id, url, entire_text, case_title, importance_number, judgment_date, facts, conclusion, ts_rank_cd(textsearchable_index_col, query) AS rank, query
            FROM english_search, websearch_to_tsquery('english', %s) AS query
            WHERE textsearchable_index_col @@ query
            ORDER BY rank DESC
            LIMIT 10
            ) 
        AS query_results;
        """
    sql_tuple = (search_term,)
    cursor.execute(sql_query, sql_tuple)
    # The result structure is a list of tuples
    results = [cursor.fetchall()]
    conn.close()
    return results


def search_text2(search_term, db, EnglishSearch):
    squery = func.websearch_to_tsquery('english', search_term)
    query = db.session.query(
        EnglishSearch.url,
        EnglishSearch.case_title, EnglishSearch.importance_number,
        EnglishSearch.judgment_date, EnglishSearch.facts, EnglishSearch.conclusion,
        func.ts_headline('english', EnglishSearch.entire_text, squery,
                         'StartSel = <b>, StopSel = </b>, ShortWord = 3, MinWords = 50, MaxWords = 60').label(
            'highlighted_text'),
        func.ts_rank_cd(EnglishSearch.textsearchable_index_col, squery).label('rank')
    ).where(
        EnglishSearch.textsearchable_index_col.op('@@')(squery)
    ).order_by(
        text('rank DESC')
    ).limit(5)
    return query