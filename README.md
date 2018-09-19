# Scraper

A lightweight scraping class with selenium and binary file download support

## Usage:

In Terminal:

`python core.py --config config_file_path`

e.g

`python core.py --config configs/reddit.json`

assuming you're executing within this directory.

---

Importing:

    from core import Scraper
    
    sc = Scraper(config_file_path)
    result = sc.run() # result should contain pandas dataframes/ dictionary depending how you set config.

## Restructuring

A major restructuring has happened! Gone was the old pass the argument to the class day! A well configured config file format in json is now designed to work with the core class and create csv files from the crawled.

With the new config files, batch processing becomes possible.

## Configs files

The examples are stored in the `configs/` directory. These included two different json files regarding reddit crawling. Recursion has enabled nested css search and creation of ordered csv files - with null values if corresponding search (column) didn't exist. More on that later.

## Example Data

In the config, there are options to save to csv, The `example_data` directory contains the files that were created by core.py running configuration file `reddit.json` and `worldnews.json` in `configs/` folder, demonstrating different capabilities.

## Old Project

The old project still exist in the `old/` directory. 
