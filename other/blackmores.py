import urllib
import urllib2
import re


def get_id_name(html):
    result=[]
    links=re.findall(r'(.+)product\.asp\?id=([0-9]*)&pname(.+) alt="(.+)" title',html)

    print len(links)
    for link in links:
        # print link[1],link[3].replace(' ','_')
        result.append((link[1],link[3].replace(' ','_').replace('/','_')))
    return result


FOLDER='static/blackmores'

def save_pic(id,name):
    url = 'http://www.chemistwarehouse.com.au/images/productimages/%s/original_CW.jpg' % id
    filename='%s/%s.jpg' % (FOLDER,name)
    urllib.urlretrieve(url, filename)
    print id,name,'Done'

#http://www.chemistwarehouse.com.au/product.asp?id=58108&pname=Swisse+Ultiboost+Sleep+100+Tablets
#/images/ProductImages/71529/150_CW
pagelist=['http://www.chemistwarehouse.com.au/category.asp?id=513&page=1',
          'http://www.chemistwarehouse.com.au/category.asp?id=513&page=2',
          'http://www.chemistwarehouse.com.au/category.asp?id=513&page=3',
          'http://www.chemistwarehouse.com.au/category.asp?id=513&page=4',
          'http://www.chemistwarehouse.com.au/category.asp?id=513&page=5',
          'http://www.chemistwarehouse.com.au/category.asp?id=513&page=6',
          'http://www.chemistwarehouse.com.au/category.asp?id=513&page=7']


if __name__ == '__main__':

    for p in pagelist:
        html=urllib2.urlopen(p).read()

        id_names=get_id_name(html)
        print id_names
        for id,name in id_names:
            save_pic(id,name)

        print p,'DONE'













