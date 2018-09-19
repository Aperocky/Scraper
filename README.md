# Scraper

A lightweight scraping class with selenium and binary file download support

## Restructuring

A major restructuring has happened! Gone was the old pass the argument to the class day! A well configured config file format in json is now designed to work with the core class and create csv files from the crawled.

With the new config files, batch processing becomes possible.

## Configs files

The examples are stored in the `configs/` directory. These included two different json files regarding reddit crawling. Recursion has enabled nested css search and creation of ordered csv files - with null values if corresponding search (column) didn't exist. More on that later.

## Old Project

The old project still exist in the `old/` directory. 
