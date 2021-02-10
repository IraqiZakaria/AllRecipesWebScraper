import pandas as pd
from selenium import webdriver



def setup_webscraper():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--no-startup-window")
    options.add_argument("--headless")

    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome()


def scrape_pages(category, start_page, end_page):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--no-startup-window")
    options.add_argument("--headless")

    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome()
    hrefs = []
    for page_number in range(start_page, end_page + 1):
        page_name = category + "/?page=" + str(page_number)

        driver.get(page_name)

        main_class = "tout__titleLink"
        links = driver.find_elements_by_class_name(main_class)
        for link in links:
            hrefs.append(link.get_attribute("href"))
        print(hrefs)
        print(page_number)
    f = open("allrecipes.txt", "a")
    f.write("\n".join(hrefs))
    f.close()

    driver.close()


def scrape_links(links):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--no-startup-window")
    options.add_argument("--headless")

    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome()
    lines = []
    for link in links:
        try:

            driver.get(link)
            description_class = "margin-0-auto"
            description = driver.find_element_by_class_name(description_class).get_attribute('textContent').encode(
                'utf-8')
            recipe_name = driver.find_element_by_class_name("recipe-title").get_attribute('textContent').encode('utf-8')
            servings_class = "recipe-adjust-servings__size-quantity"
            servings = int(driver.find_elements_by_class_name(servings_class)[0].text)
            ingredients_class = "ingredients-item-name"
            ingredients = []
            for element in driver.find_elements_by_class_name(ingredients_class):
                ingredients.append(element.text.encode('utf-8'))
            instructions_class = "instructions-section"
            instructions = driver.find_element_by_class_name(instructions_class).text.encode('utf-8')

            nutrition_class = "nutrient-name"
            nutritions = []
            for nutrition_element in driver.find_elements_by_class_name(nutrition_class):
                # html = nutrition_element.get_attribute('outerHTML')
                nutritions.append(
                    nutrition_element.get_attribute('textContent').encode('utf-8').replace('\n', '').replace(' ', ''))
            line = [recipe_name,
                    link.replace("\n", ""),
                    description,
                    "\n".join(ingredients),
                    instructions,
                    "\n".join(nutritions),
                    servings]
            lines.append(line)
            print(link)
        except:
            print("failed " + link)

    driver.close()
    data = pd.DataFrame(lines, columns=["recipe name", "recipe link", "descritption", "ingredients", "instructions",
                                        "nutritient", "servings"])
    return data


def process_links(txt_file):
    f = open(txt_file, "r")
    links = f.readlines()
    data = scrape_links(links)
    data.to_json("allrecipes.json")


if __name__ == "__main__":
    category = "https://www.allrecipes.com/recipes/138/drinks/smoothies"
    #scrape_pages(category, 2, 38)
    process_links("allrecipes.txt")
