import json

import requests
from bs4 import BeautifulSoup


def get_data(url):
    url = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': '*/*',
    }
    data = []
    #
    # Take first page for find max pagination
    request = requests.get(url, headers=headers)
    with open(f'htmls/index_1.html', 'w') as file:
        file.write(request.text)
        print('Index_1 создан для нахождения максимальной страницы')

    # Find max page pagination
    with open('htmls/index_1.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    max_pages_pagination = soup.find('div', class_='css-4mw0p4').find('ul', class_='css-1vdlgt7').find_all('li', class_='css-ps94ux')[-1].text
    print(f'Нашли максимальное количество страниц она равна {max_pages_pagination}')
    # # Take all pages for find links in product
    for i in range(2, int(max_pages_pagination) + 1):
        url_next_page = url + f'?page={i}'
        request = requests.get(url_next_page, headers=headers)
        with open(f'htmls/index_{i}.html', 'w') as file:
            file.write(request.text)
            print(f'Создана страница index_{i}')

        # # Find all links in product on page
    for j in range(1, int(max_pages_pagination) + 1):
        with open(f'htmls/index_{j}.html') as file:
            src = file.read()
            print(f'Обрабатываем страницу №{j}')

            soup = BeautifulSoup(src, 'lxml')
            links = soup.find_all('a', class_='css-rc5s2u')
            count = 0
            # Add all info about product in data
            for link in links[2:]:
                count += 1
                print('https://www.olx.ua' + link['href'])
                print(f'Обрабатываем продукт № {count} страницы {j}')
                link_product = 'https://www.olx.ua' + link['href']
                try:
                    request_to_product = requests.get(link_product, headers=headers)
                    src = request_to_product.text
                    soup = BeautifulSoup(src, 'lxml')
                    name_product = soup.find_all('div', class_='css-1yzzyg0')[1].text
                    published = soup.find_all('div', class_='css-1yzzyg0')[0].text
                    description = soup.find('div', class_='css-1t507yq er34gjf0').text
                    price = soup.find('div', class_='css-e2ir3r').find('h3').text
                    salesman = soup.find('div', class_='css-1fp4ipz').find('h4').text
                    date_registration_salesman = soup.find('div', class_='css-16h6te1 er34gjf0').text
                    data.append({
                        'name_product': name_product,
                        'link_product': link_product,
                        'publised': published,
                        'description': description,
                        'price': price,
                        'salesman': salesman,
                        'date_registration_salesman': date_registration_salesman
                    })
                    print(f'Создали запись в данные продукта №{count} страницы №{j}')
                except Exception as err:
                    print(20 * '*')
                    print(err)
                    print(20 * '*')

    with open('data.json', 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


get_data('https://www.olx.ua/uk/list/q-Corsair/')
print('Все готово')