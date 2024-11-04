dig-spider
======


Overview
========

Dig-spider is a BSD-licensed fast high-level web crawling and web scraping framework, used to
crawl websites and extract structured data from their pages. It can be used for
a wide range of purposes, from data mining to monitoring and automated testing.

Dig-spider is a code-free crawler. It is based on scrapy, and support the same command line with scrapy.



Requirements
============

* Python 3.9+
* Scrapy 2.11+
* Works on Linux, Windows, macOS, BSD

Install
=======

The quick way:

    pip install dig-spider

Usage
=======
    dig-spider gentemplate dst

generate template to target directory (dst)
modify config_template.yaml and code_template.py

    dig-spider crawl website -a config=dst/config_template.yaml

use dig-spider to replace scrapy, website is the default spider, dst/config_template.yaml is the webpage parse rule.
