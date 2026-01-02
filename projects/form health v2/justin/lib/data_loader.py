'''
    This file contains convenience functions for loading transaction and form analytics data.
'''

import sys
from typing import List, Optional

import pandas as pd
from datetime import datetime

# sys.path.append('../../../scripts/')
# from s3_support import redshift_query_read

# TODO: Fix the import issue and remove this funcion

import psycopg2

def redshift_query_read(query, schema="public"):
    con = psycopg2.connect(
        dbname="dev",
        host="redshift-cluster-1.ciakb4n4btde.us-east-1.redshift.amazonaws.com",
        port=5439,
        user="redshiftuser",
        password="Keggyg-notpih-farhy4",
        options='-c search_path={}'.format(schema)
    )

    cur = con.cursor()

    data = pd.read_sql_query(query, con)
    
    con = None
    return data


def load_transactions(
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Loads the transaction data for 2019.

    columns (Optional[List[str]]): 
        The colums that will be fetched from the Transactions table, if None than all columns will be returned
    """

    def format_columns(table_name: str, columns: Optional[List[str]]):
        if columns is None:
            return '*'
        else:
            return ', '.join(list(map(lambda column: '{}'.format(column), columns)))

    columns = format_columns(
        table_name='',
        columns=columns
    )


    return redshift_query_read(
        '''
        SELECT {}
        FROM transactions
        WHERE year = 2019;
        '''
        .format(columns)
    )

# transactions = load_transactions(
#     columns=[
#         'id', 'org', 'form', 'amount', 'donations_amt', 'purchases_amt', 'events_amt', 'registrations_amt', 'source', 'source_id', 'date'
#     ]
# )

def load_qgiv_analytics(
    base_columns: Optional[List[str]] = None,
    qgiv_columns: Optional[List[str]] = None,
    filters: Optional[List[str]] = None
    
) -> pd.DataFrame:
    """
    Loads the analytics data for all Qgiv forms in 2019.

    Args:
        base_columns (Optional[List[str]]): 
            The colums that will be fetched from the BaseAnalytics table, if None than all columns will be returned

        qgiv_columns (Optional[List[str]]): 
            The colums that will be fetched from the QgivAnalytics table, if None than all columns will be returned
        
        filters(Optional[str]):
            A filter string that can be applied to the query.
    """

    def format_columns(table_name: str, columns: Optional[List[str]]):
        if columns is None:
            return '*'
        else:
            return ', '.join(list(map(lambda column: '{}.{}'.format(table_name, column), columns)))

    base_columns = format_columns(
        table_name='A',
        columns=base_columns
    )

    qgiv_columns = format_columns(
        table_name='QA',
        columns=qgiv_columns
    )
    
    if filters is None:
        filters = ""
    else:
        filters = 'AND ' + ' AND '.join(filters)
    
    return redshift_query_read(
        '''
        SELECT {}, {}
        FROM AnalyticsQgiv AS QA
        JOIN Analytics AS A on QA.analytics_base = A.id
        WHERE extract(year from A.date) = 2019
        {};
        '''
        .format(
            base_columns, 
            qgiv_columns,
            filters
        )
    )


def load_transactions_in_range(
    form: int,
    from_date: datetime,
    to_date: datetime,
) -> pd.DataFrame:
    return redshift_query_read(
        '''
        SELECT *
        FROM transactions
        WHERE form = {} AND date BETWEEN '{}' AND '{}'
        '''
        .format(
            form,
            from_date.strftime('%Y-%m-%d'),
            to_date.strftime('%Y-%m-%d')
        )
    )
