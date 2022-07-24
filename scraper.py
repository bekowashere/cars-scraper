import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from helper import toFolderName, slugify

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def collect_brands():
    brand_data = []

    driver.get('https://www.autoevolution.com/cars/')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    brand_elements = soup.find_all('div', {'itemtype': 'https://schema.org/Brand'})

    # change directory > inside brands_logo folder
    os.chdir(os.path.join(os.getcwd(), 'brands_logo'))

    for brand_element in brand_elements:
        brand_name = brand_element.find('span', itemprop="name").get_text()
        brand_slug = ""
        brand_detail_url = brand_element.find('a')['href']
        brand_image_url = brand_element.find('img')['src']

        # SLUG
        http_text, slug_brand = brand_detail_url.split('.com/')
        brand_slug = slug_brand.replace('/', '')

        # Save image
        # Edit image name
        brand_image_path = f'{toFolderName(brand_name)}.jpg'

        with open(brand_image_path, 'wb') as f:
            b_im = requests.get(brand_image_url)
            f.write(b_im.content)

        # Brand name edit [space] - strip
        brand_new_name = brand_name.strip()

        brand = {
            "brand_name": brand_new_name,
            "brand_detail_url": brand_detail_url,
            "brand_slug": brand_slug,
            "brand_description": "",
            "brand_image_url": brand_image_url,
            "brand_image_path": brand_image_path,
        }

        brand_data.append(brand)

    os.chdir('..')

    with open('brands_summary.json', 'w') as f:
        json.dump(brand_data, f, indent=2)

    print('brands_summary.json oluşturuldu')
    driver.close()


def collect_brands_data():
    """
    brands_summary.json:
    brand_name
    brand_detail_url
    brand_slug
    brand_description
    brand_image_url
    brand_image_path
    """
    brand_data = []

    with open('brands_summary.json', 'r', encoding="UTF-8") as f:
        all_data = json.load(f)

    for brand in all_data:
        brand_name = brand['brand_name']
        brand_slug = brand['brand_slug']
        brand_detail_url = brand['brand_detail_url']
        brand_image_url = brand['brand_image_url']
        brand_image_path = brand['brand_image_path']

        driver.get(brand_detail_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(2)

        # EN Description
        try:
            en_description_element = soup.find('div', {'itemprop': 'description'})
            en_description = en_description_element.get_text()
        except:
            en_description = ""
        finally:
            print(f'{brand_name} -- EN DONE')
        time.sleep(2)

        # DE ve FR de hata çıkarsa urlleri EN ile aynı oluyor -default-
        # DE Description
        try:
            de_url_element = soup.find('link', {'hreflang': 'de'})
            de_url = de_url_element['href']
            driver.get(de_url)
            de_soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(1)
            de_description_element = de_soup.find('div', {'itemprop': 'description'})
            de_description = de_description_element.get_text()
        except:
            de_description = ""
            de_url = brand['brand_detail_url']
        finally:
            print(f'{brand_name} -- DE DONE')
        time.sleep(2)

        # FR Description
        try:
            fr_url_element = soup.find('link', {'hreflang': 'fr'})
            fr_url = fr_url_element['href']
            driver.get(fr_url)
            fr_soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(1)
            fr_description_element = fr_soup.find('div', {'itemprop': 'description'})
            fr_description = fr_description_element.get_text()
        except:
            fr_description = ""
            fr_url = brand['brand_detail_url']
        finally:
            print(f'{brand_name} -- FR DONE')
        time.sleep(2)

        brand = {
            "brand_name": brand_name,
            "brand_slug": brand_slug,
            "brand_detail_url": brand_detail_url,
            "brand_image_url": brand_image_url,
            "brand_image_path": brand_image_path,
            "brand_detail_url_en": brand_detail_url,
            "brand_description_en": en_description,
            "brand_detail_url_de": de_url,
            "brand_description_de": de_description,
            "brand_detail_url_fr": fr_url,
            "brand_description_fr": fr_description,
        }

        print(f'{brand_name} done')

        brand_data.append(brand)

    with open('all_brands.json', 'w') as f:
        json.dump(brand_data, f, indent=2)

    print('all_brands.json oluşturuldu')
    driver.close()


def collect_series_with_images():
    series_data = []

    with open('all_brands.json', 'r', encoding="UTF-8") as f:
        brands_data = json.load(f)

    for _brand in brands_data:
        # IMAGE: create folder with brand name -> BMW (toFolderName functions helps us)
        folder_name = toFolderName(_brand['brand_name'])

        try:
            os.chdir(os.path.join(os.getcwd(), 'images'))
            os.mkdir(os.path.join(os.getcwd(), folder_name))
        except:
            print(f'{folder_name} oluşturulamadı (IMAGE)')

        os.chdir(os.path.join(os.getcwd(), folder_name))

        brand_detail_url = _brand['brand_detail_url_en']
        brand_slug = _brand['brand_slug']
        time.sleep(1)
        driver.get(brand_detail_url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(1)

        series_elements = soup.find_all('div', {'class': 'carmod'})

        for se in series_elements:
            series_brand_name = _brand['brand_name']
            series_title = se.find('h4').get_text()
            _series_name = series_title.replace(series_brand_name, "")
            series_name = _series_name.strip()
            series_slug = ""
            series_detail_url = se.find('a')['href']
            series_image = se.find('img')
            series_image_url = se.find('img')['src']

            # SLUG
            http_text, _slug_series = series_detail_url.split(brand_slug)
            slug_series = _slug_series.replace('/', '')
            series_slug = slug_series.strip()

            try:
                bodyStyle = se.find('p', class_=["body"]).get_text().upper()
            except:
                bodyStyle = None

            isDiscontinued = False
            if series_image.has_attr('class'):
                if series_image.attrs['class'][0] == 'faded':
                    isDiscontinued = True

            try:
                series_generation_count = se.find('b', {'class': 'col-green2'}).text
            except:
                series_generation_count = None

            series_fuel_types = []

            fuel_element = se.find('p', {'class': 'eng'})
            fuels = fuel_element.find_all('span')
            for fuel in fuels:
                fuel_text = fuel.text.title()
                series_fuel_types.append(fuel_text)

            # IMAGE
            folder_title = toFolderName(series_name)
            series_image_path = f'{toFolderName(series_name)}.jpg'
            os.mkdir(os.path.join(os.getcwd(), folder_title))
            os.chdir(os.path.join(os.getcwd(), folder_title))
            with open(series_image_path, 'wb') as f:
                s_im = requests.get(series_image_url)
                f.write(s_im.content)

            os.chdir('..')

            series = {
                "brand_name": series_brand_name,
                "brand_detail_url": brand_detail_url,
                "brand_slug": brand_slug,
                "series_name": series_name,
                "series_detail_url": series_detail_url,
                "series_slug": series_slug,
                "series_bodyStyle": bodyStyle,
                "series_isDiscontinued": isDiscontinued,
                "series_image_url": series_image_url,
                "series_image_path": series_image_path,
                "series_fuelType": series_fuel_types,
                "series_generation_count": series_generation_count
            }

            series_data.append(series)

        os.chdir('..')
        os.chdir('..')

    with open('all_series.json', 'w') as f:
        json.dump(series_data, f, indent=2)

    print('all_series.json oluşturuldu')
    driver.close()


def collect_models_summary():
    model_data = []
    car_data = []

    with open('all_series.json', 'r', encoding="UTF-8") as f:
        series_data = json.load(f)

    for series in series_data:
        brand_name = series['brand_name']
        brand_detail_url = series['brand_detail_url']
        brand_slug = series['brand_slug']
        series_name = series['series_name']
        series_detail_url = series['series_detail_url']
        series_slug = series['series_slug']

        driver.get(series_detail_url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(1)

        model_elements = soup.find_all('div', {'data-itemtype': 'https://schema.org/Car'})
        for _model in model_elements:
            h2_element = _model.find('h2', {'itemprop': 'name'})
            model_detail_url = h2_element.find('a')['href']
            model_name = h2_element.find('span', {'class': 'col-red'}).get_text()
            model_slug = ""
            model_image_url = _model.find('img', {'itemprop': 'image'})['src']

            # SLUG
            http_text, _slug_model = model_detail_url.split('/cars/')
            slug_model, html_text = _slug_model.split('.')
            model_slug = slug_model.strip()

            # Image Path
            txt1, jpg_path = model_image_url.rsplit('/', 1)
            model_image_path = jpg_path

            try:
                years_element = _model.find('p', {'class': 'years'})
                years = years_element.get_text()
            except:
                years = ""

            if "-" in years:
                first_year, last_year = years.split(' - ')
            else:
                first_year = years
                last_year = years

            car_elements = _model.find_all('a', {'class': 'engurl semibold'})
            for _car in car_elements:
                car_url = _car['href']
                main_url, alt_url = car_url.split('#a')
                car_name = _car.find('span', {'class': 'col-green2'}).get_text()

                car_global = {
                    "brand_name": brand_name,
                    "brand_detail_url": brand_detail_url,
                    "brand_slug": brand_slug,
                    "series_name": series_name,
                    "series_detail_url": series_detail_url,
                    "series_slug": series_slug,
                    "model_name": model_name,
                    "model_detail_url": model_detail_url,
                    "model_slug": model_slug,
                    "car_name": car_name,
                    "car_detail_url": car_url,
                    "car_alt_url": alt_url
                }

                car_data.append(car_global)

            model = {
                "brand_name": brand_name,
                "brand_detail_url": brand_detail_url,
                "brand_slug": brand_slug,
                "series_name": series_name,
                "series_detail_url": series_detail_url,
                "series_slug": series_slug,
                "model_name": model_name,
                "model_detail_url": model_detail_url,
                "model_slug": model_slug,
                "model_image_url": model_image_url,
                "model_image_path": model_image_path,
                "model_first_year": first_year,
                "model_last_year": last_year,
            }

            model_data.append(model)

    with open('cars_all.json', 'w') as f:
        json.dump(car_data, f, indent=2)

    with open('models_summary.json', 'w') as f:
        json.dump(model_data, f, indent=2)

    print("cars_all.json oluşturuldu")
    print("models_summary.json oluşturuldu")
    driver.close()


def collect_models_data():
    all_models = []

    with open('models_summary.json', 'r', encoding="UTF-8") as f:
        models_data = json.load(f)

    for _model in models_data:
        brand_name = _model['brand_name']
        brand_detail_url = _model['brand_detail_url']
        brand_slug = _model['brand_slug']
        series_name = _model['series_name']
        series_detail_url = _model['series_detail_url']
        series_slug = _model['series_slug']
        model_name = _model['model_name']
        model_detail_url = _model['model_detail_url']
        model_slug = _model['model_slug']
        model_image_url = _model['model_image_url']
        model_image_path = _model['model_image_path']
        model_first_year = _model['model_first_year']
        model_last_year = _model['model_last_year']

        driver.get(model_detail_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Segment
        try:
            p_element = soup.find('p', {'class': 'mgbot_20 nomgtop'})
            b_element = p_element.find('b', string="Segment:")
            segment_element = b_element.next_sibling
            segment = segment_element.text.strip()
        except:
            print(f'{model_name} does not have SEGMENT')
            segment = None

        # BodyStyle
        try:
            p_element = soup.find('p', {'class': 'mgbot_20 nomgtop'})
            b_element = p_element.find('b', string="Body style:")
            bodystyle_element = b_element.next_sibling
            bodyStyle = bodystyle_element.text.strip()
        except:
            print(f'{model_name} does not have BODY STYLE')
            bodyStyle = None

        # Infotainment
        infotainment = []
        try:
            p_element = soup.find('p', {'class': 'mgbot_20 nomgtop'})
            inf_elements = p_element.find_all('img', {'align': 'absmiddle'})
            for inf in inf_elements:
                inf_full_name = inf['alt']
                inf_name = inf_full_name.replace(" icon", "")
                infotainment.append(inf_name)
        except:
            print(f'{model_name} does not have INFOTAINMENT')
            infotainment = []

        # Other Images
        images_url = []
        try:
            image_elements = soup.find_all('a', {'class': 's_gallery'})
            if len(image_elements) > 15:
                for index, element in enumerate(image_elements, start=1):
                    if index == 16:
                        break
                    image_url = element['href']
                    images_url.append(image_url)
            else:
                for element in image_elements:
                    image_url = element['href']
                    images_url.append(image_url)
        except:
            print(f'{model_name} does not have IMAGES')
            images_url = []

        # Fuel Type
        fuel_data = []
        try:
            fuel_type_elements = soup.find_all('div', {'class': 'tt'})
            for ft_element in fuel_type_elements:
                fuel_element = ft_element.find('i')
                fuel_type = fuel_element['title']
                fuel_data.append(fuel_type)
        except:
            print(f'{model_name} does not have FUEL TYPE')
            fuel_data = []

        print("Languages activate")
        # ENG Description
        try:
            en_description_element = soup.find('div', {'itemprop': 'description'})
            en_description = en_description_element.get_text()
            print(f'{model_name} -- ENG is completed successfully')
        except:
            en_description = ""
        finally:
            print(f'{model_name} -- EN DONE')
        time.sleep(1)

        # DE ve FR de hata çıkarsa urlleri EN ile aynı oluyor -default-
        # DE Description
        try:
            de_url_element = soup.find('link', {'hreflang': 'de'})
            de_url = de_url_element['href']
            driver.get(de_url)
            de_soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(1)
            de_description_element = de_soup.find('div', {'itemprop': 'description'})
            de_description = de_description_element.get_text()
            print(f'{model_name} -- DE is completed successfully')
        except:
            de_description = ""
            de_url = model_detail_url
        finally:
            print(f'{model_name} -- DE DONE')
        time.sleep(1)

        # FR Description
        try:
            fr_url_element = soup.find('link', {'hreflang': 'fr'})
            fr_url = fr_url_element['href']
            driver.get(fr_url)
            fr_soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(1)
            fr_description_element = fr_soup.find('div', {'itemprop': 'description'})
            fr_description = fr_description_element.get_text()
            print(f'{model_name} -- FR is completed successfully')
        except:
            fr_description = ""
            fr_url = model_detail_url
        finally:
            print(f'{model_name} -- FR DONE')
        time.sleep(1)

        model = {
            "brand_name": brand_name,
            "brand_detail_url": brand_detail_url,
            "brand_slug": brand_slug,
            "series_name": series_name,
            "series_detail_url": series_detail_url,
            "series_slug": series_slug,
            "model_name": model_name,
            "model_detail_url": model_detail_url,
            "model_slug": model_slug,
            "model_image_url": model_image_url,
            "model_image_path": model_image_path,
            "model_first_year": model_first_year,
            "model_last_year": model_last_year,
            "model_segment": segment,
            "model_bodyStyle": bodyStyle,
            "model_infotainment": infotainment,
            "model_fuelType": fuel_data,
            "model_images_url": images_url,
            "model_detail_url_en": model_detail_url,
            "model_description_en": en_description,
            "model_detail_url_de": de_url,
            "model_description_de": de_description,
            "model_detail_url_fr": fr_url,
            "model_description_fr": fr_description,
        }

        all_models.append(model)

    with open('all_models.json', 'w') as f:
        json.dump(all_models, f, indent=2)

    print("all_models.json oluşturuldu")
    driver.close()


def create_model_images():
    with open('models_summary.json', 'r', encoding="UTF-8") as f:
        models_data = json.load(f)

    for model in models_data:
        model_image_url = model['model_image_url']
        model_image_path = model['model_image_path']
        model_brand_name = model['brand_name']
        model_series_name = model['series_name']

        # /images
        os.chdir(os.path.join(os.getcwd(), 'images'))
        # / BMW
        os.chdir(os.path.join(os.getcwd(), model_brand_name))
        # / X7
        os.chdir(os.path.join(os.getcwd(), model_series_name))

        with open(model_image_path, 'wb') as f:
            m_im = requests.get(model_image_url)
            f.write(m_im.content)

        print(f'{model_image_path} is saved successfully')

        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        time.sleep(1)

    print("Model Images DONE")


def collect_cars():
    all_cars = []
    specification_types = []
    specifications = []

    with open('cars_all.json', 'r', encoding="UTF-8") as f:
        cars_data = json.load(f)

    for car in cars_data:
        brand_name = car['brand_name']
        brand_detail_url = car['brand_detail_url']
        brand_slug = car['brand_slug']
        series_name = car['series_name']
        series_detail_url = car['series_detail_url']
        series_slug = car['series_slug']
        model_name = car['model_name']
        model_detail_url = car['model_detail_url']
        model_slug = car['model_slug']
        car_name = car['car_name']
        car_detail_url = car['car_detail_url']
        car_alt_url = car['car_alt_url']

        time.sleep(1)
        driver.get(car_detail_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(1)

        try:

            _engine, _enginePower = car_name.split('(')
            engine = _engine.strip()
            enginePower, txt = _enginePower.split(' ')
        except:
            engine = car_name
            enginePower = None
        finally:
            print(f'Car: {car_name} -- engine: & enginePower')

        # car_slug
        car_txt, car_slug = car_detail_url.split('#aeng_')

        # car_fuel_type
        car_fuel_type = ""

        # SPECIFICATION
        information_dict = {}
        car_specification_element = soup.find('div', {'id': car_alt_url})
        main_element = car_specification_element.find('div', {'class': 'enginedata engine-inline'})
        techdata_elements = main_element.find_all('div', {'class': 'techdata'})
        for techdata_element in techdata_elements:
            dl_element = techdata_element.find('dl')
            # General Specs
            spc_title = dl_element['title']

            specification_type = {
                "name": spc_title
            }

            specification_types.append(specification_type)

            my_dict = {}
            dt_elements = dl_element.find_all('dt')
            for dt_element in dt_elements:
                value = dt_element.next_sibling.text.strip()
                my_dict[dt_element.text] = value

                if dt_element.text == "Fuel":
                    car_fuel_type = value.strip()

                specification = {
                    "cs_type": spc_title,
                    "name": dt_element.text
                }

                specifications.append(specification)

            information_dict[spc_title] = my_dict

        car = {
            "brand_name": brand_name,
            "brand_detail_url": brand_detail_url,
            "brand_slug": brand_slug,
            "series_name": series_name,
            "series_detail_url": series_detail_url,
            "series_slug": series_slug,
            "model_name": model_name,
            "model_detail_url": model_detail_url,
            "model_slug": model_slug,
            "car_name": car_name,
            "car_detail_url": car_detail_url,
            "car_slug": car_slug,
            "car_alt_url": car_alt_url,
            "car_fuelType": car_fuel_type,
            "car_engine": engine,
            "car_enginePower": enginePower,
            "car_information": information_dict

        }

        all_cars.append(car)

    time.sleep(1)

    with open('all_specification_types.json', 'w') as f:
        json.dump(specification_types, f, indent=2)

    with open('all_specifications.json', 'w') as f:
        json.dump(specifications, f, indent=2)

    with open('all_cars.json', 'w') as f:
        json.dump(all_cars, f, indent=2)

    print("all_cars.json oluşturuldu")
    driver.close()
