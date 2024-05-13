# weibo-spider
## Introduction

This is a Sina Weibo (mobile site) crawler program. Weibo is the most popular social media in Chinese Mainland. We clean and organize the data crawled, based on which word-cloud figure can be carried out.

## Code Structure
`scrapy startproject [yourproject]` will create a scrapy project.

`scrapy.cfg` is the configuration file for the project.

`setting.py` is used to set the parameters of the request, use the proxy, crawl the data after file saving.

`/spider/sinaSpider.py` is the main code of the crawler.

`middlewares.py` is the middleware for scrapy's request and its related processing. It is mainly the rotation of UserAgent, Cookies and agents.

`items.py` is the definition file of the data structure that needs to be extracted.

`pipelines.py` is to further process the data extracted from items, and the connection to mongdb is in this.

## Libraries
[*scrapy*](https://docs.scrapy.org/en/latest/) is an application framework for crawling website data and extracting structured data. It is a very powerful and easy-to-use crawler framework that not only provides some basic components out of the box, but also provides powerful customization capabilities.

[*selenium*](https://pypi.org/project/selenium/) is a tool for testing Web applications. Selenium tests run directly in the browser, just as real users do. We use selenium mainly to simulate the behavior of users to log in to Weibo and get cookies.

[*PhantomJS*](https://phantomjs.org/) is a non-interface, scriptable WebKit browser engine. It natively supports several web standards: DOM manipulation, CSS selectors, JSON, Canavs, etc.

## Reference
![web_scraping_with_python](https://github.com/konhay/weibo-spider/assets/26830433/dccb56dd-7fec-4b26-8f05-c50311fda1e8)

