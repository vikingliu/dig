======
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

.. code:: bash

    pip install dig-spider

Usage
=======

.. code:: bash
    
    dig-spider crawl website -a config=xxx.yaml

use dig-spider to replace scrapy, website is the default spider, xxx.yaml is the webpage parse rule.