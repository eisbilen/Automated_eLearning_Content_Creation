# Automated_eLearning_Content_Creation

##Automated e-Learning Content Creation with Web Scraping and NLP

If you aim to develop an e-learning platform, the first difficulty you have to overcome will probably be creating the course content. Unfortunately, creating course content is the most challenging part of the development process as it consumes a lot of time and energy. Fortunately, this process can be automated with the help of web scraping and natural language processing.
In this post, I will show you step by step how such automation can be achieved using Scrapy and spaCy. In the first step, I will use the Scrapy to scrape news articles from the web. In the second step, I will process the text data by spaCy to convert the news articles to something directly usable in an English e-learning platform.

The result of the above steps will be a JSON file containing 10K lines of questions in two categories which are 'Put the words in correct order' and 'Find the missing word'. The content of this JSON file then will be used in my demo web application, lingomoo.
