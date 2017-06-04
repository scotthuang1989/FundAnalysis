from urllib.request import urlopen


def GetStockData(stock_code,start,end,filename):

    #stock_code, end with .ss (shanghai) or .sz (shenzhen)
    url_template = "http://ichart.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}&d={4}&e={5}&f={6}&g=d"
    url_data = url_template.format(stock_code,start.month-1,start.day,start.year,end.month-1,end.day,end.year)
    print(url_data)
    url_response = urlopen(url_data)
    file_data = open(filename,'w')

    file_data.write(url_response.read().decode("utf-8"))
    file_data.close()
    return True;
#    except:


