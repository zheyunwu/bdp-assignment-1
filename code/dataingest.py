import os
import sys
import csv
import pandas as pd
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from coredms import create_connection

# https://docs.datastax.com/en/drivers/python/3.2/api/cassandra/query.html

def handle_listings(filename):
    session = create_connection()
    insert_stmt = session.prepare("INSERT INTO listings (id, listing_id, scrape_id, last_scraped, name, description, neighborhood_overview, picture_url, host_id, host_url, host_name, host_since, host_location, host_about, latitude, longitude, property_type, room_type, accommodates, bathrooms, bathrooms_text, bedrooms, beds, amenities, price)) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

    # read csv in chunks
    count = 0
    reader = pd.read_csv(os.getcwd() + '/../data/' + filename, chunksize=50)
    try:
        for chunk_df in reader:
            for row in chunk_df.itertuples():
                batch.add(insert_stmt, (row.id, row.listing_id, row.scrape_id, row.last_scraped, row.name, row.description, row.neighborhood_overview, row.picture_url, row.host_id, row.host_url, row.host_name, row.host_since, row.host_location, row.host_about, row.latitude, row.longitude, row.property_type, row.room_type, row.accommodates, row.bathrooms, row.bathrooms_text, row.bedrooms, row.beds, row.amenities, row.price))
                count+=1
            # insert every 50 rows
            session.execute(batch)
            batch.clear()
            print("[listings] Inserted %s rows of data" % count)
    except Exception as e:
        print('[listings] Error: %s, count: %s' % (e, count))


def handle_calendar(filename):
    session = create_connection()
    insert_stmt = session.prepare("INSERT INTO calendar (listing_id, date, available, price, adjusted_price, minimum_nights, maximum_nights) VALUES (?, ?, ?, ?, ?, ?, ?)")
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

    # read csv in chunks
    count = 0
    reader = pd.read_csv(os.getcwd() + '/../data/' + filename, chunksize=50)
    try:
        for chunk_df in reader:
            for row in chunk_df.itertuples():
                batch.add(insert_stmt, (row.listing_id, row.date, row.available, row.price, row.adjusted_price, row.minimum_nights, row.maximum_nights))
                count+=1
            # insert every 50 rows
            session.execute(batch)
            batch.clear()
            print("[calendar] Inserted %s rows of data" % count)
    except Exception as e:
        print('[calendar] Error: %s, count: %s' % (e, count))


def handle_reviews(filename):
    session = create_connection()
    insert_stmt = session.prepare("INSERT INTO reviews (listing_id, id, date, reviewer_id, reviewer_name, comments) VALUES (?, ?, ?, ?, ?, ?)")
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

    # read csv in chunks
    count = 0
    reader = pd.read_csv(os.getcwd() + '/../data/' + filename, chunksize=50)
    try:
        for chunk_df in reader:
            for row in chunk_df.itertuples():
                batch.add(insert_stmt, (row.listing_id, row.id, row.date, row.reviewer_id, row.reviewer_name, row.comments))
                count+=1
            # insert every 50 rows
            session.execute(batch)
            batch.clear()
            print("[reviews] Inserted %s rows of data" % count)
    except Exception as e:
        print('[reviews] Error: %s, count: %s' % (e, count))


if __name__ == '__main__':

    table = sys.argv[1]
    filename = sys.argv[2]

    if table == 'listings':
        handle_listings(filename)
    if table == 'calendar':
        handle_calendar(filename)
    if table == 'reviews':
        handle_reviews(filename)
        