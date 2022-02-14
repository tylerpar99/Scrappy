import scrapy


class AptechSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['https://www.politico.com/search?q=Technology']
    start_urls = ['https://www.politico.com/search?q=Technology']

    def parse(self, response):
        for articles in response.css('article.story-frag.format-ml'):
            yield {
                'Title': articles.css('img').attrib['alt'],
                'Link': articles.css('a').attrib['href'],
                'Intro': articles.css('div.tease').css('p::text').get(),
                'Category': articles.css('p.categroy::text').get(),
                'DateandTime': articles.css('time').attrib['datetime'],
            }
        for button in response.css('a.button'):
            if button.css('::text').get() == 'Next page >>':
                next_page = button.attrib['href']
                print(" \n Next Page :" + next_page + "\n")
                yield response.follow(next_page, callback=self.parse)
