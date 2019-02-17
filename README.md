# Scraper

A lightweight scraping class with selenium and binary file download support

The core class output dataframe based on set of rule specified in the config.json files.

selenium_core extend core class functionality by adding selenium (read: JavaScript) support to this scraper.

## Usage:

    from core import Scraper
    from selenium_core import SeleniumScraper

    sc = Scraper(config_file_path) # Or SeleniumScraper
    result = sc.run() # result is a list of pandas dataframe.

## Restructuring

A major restructuring has happened! Gone was the old pass the argument to the class day! A well configured config file format in json is now designed to work with the core class and create csv files from the crawled.

With the new config files, batch processing becomes possible.

## Configs files

The examples are stored in the `configs/` directory. These included two different json files regarding reddit crawling. Recursion has enabled nested css search and creation of ordered csv files - with null values if corresponding search (column) didn't exist. More on that later.

## Example Data

In the config, there are options to save to csv, The `example_data` directory contains the files that were created by core.py running configuration file `reddit.json` and `worldnews.json` in `configs/` folder, demonstrating different capabilities.

## Old Project

The old project still exist in the `old/` directory.
