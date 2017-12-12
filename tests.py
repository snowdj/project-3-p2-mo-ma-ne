from modules import *
import pandas as pd
import numpy.testing as npt

def test_connection_and_dataframe_cols():
    """
    methods tested: dbConnect(), dbTableToDataFrame(conn, table):
    confirms successfully connected to p3 database and that a table
    converted to dataframe has the correct column names
    """

    conn = dbConnect()
    table = 'cb_objects'
    df = dbTableToDataFrame(conn, table)
    obj_cols = ['category_code', 'city', 'closed_at', 'country_code', 'created_at',
       'created_by', 'description', 'domain', 'entity_id', 'entity_type',
       'first_funding_at', 'first_investment_at', 'first_milestone_at',
       'founded_at', 'funding_rounds', 'funding_total_usd', 'homepage_url',
       'id', 'invested_companies', 'investment_rounds', 'last_funding_at',
       'last_investment_at', 'last_milestone_at', 'logo_height', 'logo_url',
       'logo_width', 'milestones', 'name', 'normalized_name', 'overview',
       'parent_id', 'permalink', 'region', 'relationships',
       'short_description', 'state_code', 'status', 'tag_list',
       'twitter_username', 'updated_at']
    npt.assert_array_equal(df.columns, obj_cols)

def test_connection_and_dataframe_shape():
    """
    methods tested: dbConnect(), dbTableToDataFrame(conn, table):
    confirms successfully connected to p3 database and that a table
    converted to dataframe is the correct dimension
    """
    conn = dbConnect()
    table = 'cb_objects'
    df = dbTableToDataFrame(conn, table)
    obj_shape = (462651, 40)
    assert df.shape == obj_shape

def test_SchoolID_remove_stopword():
    institutions = pd.Series(['harvard university', 'the university of oregon'])
    SD = SchoolTools()
    ids = SD.remove_stopwords(institutions)
    key = pd.Series(['harvard university','university oregon'])
    assert ids.equals(key)

def test_SchoolID_remove_punctuation():
    institutions = pd.Series(['university of california, berkeley','harvard.'])
    SD = SchoolTools()
    ids = SD.remove_punctuation(institutions)
    key = pd.Series(['university of california  berkeley', 'harvard'])
    assert ids.equals(key)

def test_SchoolID_delete_stems():
    institutions = pd.Series([['university','california'],['harvard','law']])
    SD = SchoolTools()
    for i in range(len(institutions)):
        institutions[i] = SD._delete_stems(institutions[i])
    key = pd.Series([['california'],['harvard']])
    assert institutions.equals(key)

def test_SchoolID_reduce_to_stems():
    institutions = pd.Series([['university','california'],['virginia','tech']])
    SD = SchoolTools()
    for i in range(len(institutions)):
        institutions[i] = SD._reduce_to_stems(institutions[i])
    key = pd.Series([['university','cal'],['virginia','tec']])
    assert institutions.equals(key)

def test_SchoolID_replace_by_keyword():
    institutions = pd.Series([['upenn','wharton'],['harvard','law']])
    SD = SchoolTools()
    for i in range(len(institutions)):
        institutions[i] = SD._replace_by_keyword(institutions[i])
    key = pd.Series([['wharton'],['harvard']])
    assert institutions.equals(key)

def test_SchoolID_replace_by_nickname():
    institutions = pd.Series([['cal'],['massachusetts','inst','tec']])
    SD = SchoolTools()
    for i in range(len(institutions)):
        institutions[i] = SD._replace_by_nickname(institutions[i])
    key = pd.Series([['berkeley'],['mit']])
    assert institutions.equals(key)
