# FundAnalysis
Analyze fund data

# Code Structure

* crawler : web crawler built with scrapy framework
    * FundIdSpider: get fund basic inforamtion
    * FundZcpzSpier: get zcpz(resource allocation ) of funds.
    * FundCumulativeNet: Get cumulative value of fund.

* DataProcess : jupyter notebook for processing data
    * Basic information analysis
        * number of fund
        * number of fund per company
        * total asset of fund per company
        * number of fund per category
        * total asset of fund per catetory
    * Relationship between stock and fund 2015 - 2016
        * analyze relationship betwwen stock market and fund in 2015 - 2016
    * ACCNAV_Analysis
        * Verify is ACCNAV( fund net value will be similar for same category ) is right.
* GetStock Data : program which get stock data
    

