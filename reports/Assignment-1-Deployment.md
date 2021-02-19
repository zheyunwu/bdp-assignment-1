# This is a deployment/installation guide

## Prerequisites  
Docker and Python3 should be installed

## Setup mysimbdp-coredms
1. Create the Cassandra cluster on Google Cloud Platform.  
2. Log into one of the Cassandra nodes.  
3. Use following command in the shell to interact with Cassandra:  
    ```shell
    $ cqlsh
    ```

4. Create keyspace:  
    ```shell
    cqlsh> CREATE KEYSPACE airbnb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
    ```

5. Create tables:  
- listings.csv:  
    ```shell
    cqlsh> CREATE TABLE airbnb.listings (
        id bigint,
        listing_url text,
        scrape_id text,
        last_scraped date,
        name text,
        description text,
        neighborhood_overview text,
        picture_url text,
        host_id bigint,
        host_url text,
        host_name text,
        host_since date,
        host_location text,
        host_about text,
        host_response_time text,
        host_response_rate text,
        host_acceptance_rate text,
        host_is_superhost boolean,
        host_thumbnail_url text,
        host_picture_url text,
        host_neighbourhood text,
        host_listings_count int,
        host_total_listings_count int,
        host_verifications list<text>,
        host_has_profile_pic boolean,
        host_identity_verified boolean,
        neighbourhood text,
        neighbourhood_cleansed text,
        neighbourhood_group_cleansed text,
        latitude text,
        longitude text,
        property_type text,
        room_type text,
        accommodates int,
        bathrooms int,
        bathrooms_text int,
        bedrooms int,
        beds int,
        amenities list<text>,
        price text,
        minimum_nights int,
        maximum_nights int,
        minimum_minimum_nights int,
        maximum_minimum_nights int,
        minimum_maximum_nights int,
        maximum_maximum_nights int,
        minimum_nights_avg_ntm double,
        maximum_nights_avg_ntm double,
        has_availability boolean,
        availability_30 int,
        availability_60 int,
        availability_90 int,
        availability_365 int,
        calendar_last_scraped date,
        number_of_reviews int,
        number_of_reviews_ltm int,
        number_of_reviews_l30d int,
        first_review date,
        last_review date,
        review_scores_rating int,
        review_scores_accuracy int,
        review_scores_cleanliness int,
        review_scores_checkin int,
        review_scores_communication int,
        review_scores_location int,
        review_scores_value int,
        instant_bookable boolean,
        calculated_host_listings_count int,
        calculated_host_listings_count_entire_homes int,
        calculated_host_listings_count_private_rooms int,
        calculated_host_listings_count_shared_rooms int,
        reviews_per_month double,
        PRIMARY KEY (id, host_id)
    );
    ```

- calendar.csv:  
    ```shell
    cqlsh> CREATE TABLE airbnb.calendar (
        listing_id bigint,
        date date,
        available text,
        price text,
        adjusted_price text,
        minimum_nights int,
        maximum_nights int,
        PRIMARY KEY (listing_id, date)
    );
    ```

- reviews.csv:  
    ```shell
    cqlsh> CREATE TABLE airbnb.reviews (
        listing_id bigint,
        id bigint,
        date date,
        reviewer_id bigint,
        reviewer_name text,
        comments text,
        PRIMARY KEY (id, listing_id, reviewer_id)
    );
    ```

## Setup mysimdp-dataingest
1. Go to the /code directory of this project
2. Install required packages using following command:
    ```shell
    $ pip3 install -r requirements.txt
    ```

## Start to test!
1. Put airbnb datasets in the /data directory of this project
2. Go to the /code directory of this project
3. Run following command to use dataingest:  
    ```shell
    $ python3 dataingest.py [table] [filename]
    ```
    where 'table' could be 'listings', 'calendar' or 'reviews'  
    and 'filename' is the filename of the data csv file with extension such as 'reviews.csv'