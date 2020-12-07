# Imports for functions
import bs4
import requests, json
from grocery_obj import grocery as groc
from urllib.parse import quote
import os, time
from datetime import datetime

# Imports for GUI
from tkinter import *
from tkinter import StringVar, Tk
from tkinter import messagebox
from PIL import ImageTk, Image


def redo():
    # #########################################Walmart Scrapper#######################################
    # Coder: Rebecca Makus

    class WS:

        def __init__(self):
            self.__searchTerm = ""
            self.__title1 = ""
            self.__title2 = ""
            self.__price = ""
            self.__search = bs4.BeautifulSoup(features="html.parser")
            self.__items = {}
            self.notAvail = "Price not available online"
            self.__userCount = ""
            count = 0

        def searchWalmart(self, searchTerm, userCount):
            self.__searchTerm = searchTerm
            self.__userCount = userCount
            self.scrapeWalmart(searchTerm)
            self.fileText(self.__search)
            for count in range(0, (self.__userCount - 1)):
                self.findTitle()
                self.findPrice()
                self.getItems(self.__title2, self.__price)
                with open('rawText.txt', 'r', encoding="utf-8") as f:
                    cleanFile = f.read()
                cleanFile = cleanFile.replace(("Product Title" + self.__title1 + "Average rating"), "")
                cleanFile = cleanFile.replace(("Current Price" + self.__price + "$"), "")
                with open('rawText.txt', 'w', encoding="utf-8") as f:
                    f.write(cleanFile)
                count = count + 1
            with open('final.txt', 'w', encoding="utf-8") as f:
                fileItems = str(self.__items)
                f.write(fileItems)
            return self.__items

        def scrapeWalmart(self, searchTerm):
            self.__searchTerm = searchTerm
            # Enter item they are looking for
            # Search webpage for item
            page = 'https://www.walmart.com/search/?query=' + self.__searchTerm + '&cat_id=976759'
            res = requests.get(page)
            try:
                res.raise_for_status()
            except Exception as exc:
                print('There was a problem: %s' % (exc))
            var = res.status_code == requests.codes.ok
            # pull webpage into text
            self.__search = bs4.BeautifulSoup(res.text, features="html.parser")
            return self.__search

        def fileText(self, search):
            # search text for title
            rawText = search.get_text()
            rawText = str(rawText)
            with open("rawText.txt", "w", encoding="utf-8") as f:
                f.write(rawText)
            with open("fullRaw.txt", "w", encoding="utf-8") as f:
                f.write(rawText)

        def findPrice(self):
            # search text for price
            with open("rawText.txt", "r", encoding="utf-8") as f:
                rawPrices = f.read()
            start = 'Current Price$'
            end = '$'
            try:
                self.__price = ((rawPrices.split(start))[1].split(end)[0])
                self.__price = ("$" + self.__price)
            except AttributeError:
                self.__price = self.notAvail
            except IndexError:
                self.__price = self.notAvail
            except self.__price == []:
                start = 'Current Price$'
                end = '$'
                self.__price = ((rawPrices.split(start))[1].split(end)[0])
            return self.__price

        def findTitle(self):
            # search text for title
            with open("rawText.txt", "r", encoding="utf-8") as f:
                rawTitle = f.read()
            start = 'Product Title'
            end = 'Average rating'
            self.__title1 = ((rawTitle.split(start))[1].split(end)[0])
            if len(self.__title1) <= 100:
                self.__title2 = self.__title1.replace('...', '')
                self.__title2 = self.__title2.replace(';', '')
                self.__title2 = self.__title2.replace('&', '')
                return self.__title2
            else:
                pass

        def getItems(self, title, price):
            self.__title = title
            self.__price = price
            self.__items[self.__title] = self.__price
            return self.__items

    """
    while True:
        srchTerm = input("Enter Search Term: ")
        cnt = int(input("Enter Count: "))
        x = WS()
        answer = x.searchWalmart(srchTerm, cnt)
        product_price = x.findPrice()
         for i in answer:
            print()
            print(i)
            print(product_price)
            print()
    """

    # #########################################Walmart Scrapper#######################################
    # Coder: Chels

    class YelpData:

        def __init__(self, authfile, term, location, limit=10):

            self.api_host = 'https://api.yelp.com'
            self.search_path = '/v3/businesses/search'
            self.bus_path = '/v3/businesses/'  # Business id comes after. Didn't impliment
            self.authfile = authfile  # Json file containing validation keys
            self.term = term  # The term we will be searching for (E.g. grocery stores)
            self.location = location  # The area. Even takes general areas like "Midtown"
            self.limit = limit  # How many response to check
            self.grocery_list = []  # A list to contain the grocery business objects

            self.term_val()
            self.auth_file_val()
            self.limit_val()
            self.loc_val()

        def loc_val(self):
            try:
                a = int(self.location)
                if len(self.location) != 5:
                    # print("Please only enter five digit zipcode")
                    messagebox.showinfo("Zip code", "Please only enter five digit zipcode")
                    window.destroy()
                    redo()
                    # sys.exit()
            except ValueError as e:
                # print("Please only enter integers. Not strings.")
                messagebox.showinfo("Zip code", "Please only enter numbers, not letters")
                window.destroy()
                redo()
                # sys.exit()

        def term_val(self):
            if not self.term.isalpha:
                # print("Term Should only be letters a-z.")
                messagebox.showinfo("Error", "Term Should only be letters a-z")
                window.destroy()
                redo()
                # sys.exit()

        def auth_file_val(self):
            if not os.path.isfile(self.authfile):
                # print("{} is does not exist.".format(self.authfile))
                messagebox.showinfo("Error", "{} is does not exist.".format(self.authfile))
                window.destroy()
                redo()
                # sys.exit()

        def limit_val(self):
            try:
                int(self.limit)
            except ValueError as e:
                # print("Please only enter integers. Not strings.")
                messagebox.showinfo("Zip code", "Please only enter numbers, not letters")
                window.destroy()
                redo()
                # sys.exit()

        def authentication(self):

            self.auth_file_val()
            with open(self.authfile, 'r') as cs:
                data = json.load(cs)

                auth_info = data[0]
                api_key = auth_info["api_key"]
                client_id = auth_info["client_id"]

            headers = {'Authorization': 'Bearer {}'.format(api_key)}
            return headers

        def request(self, host, path, url_params=None):
            """
          Cribbed doc strings from: https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py
          Given your API_KEY, send a GET request to the API.
             Args:
                 host (str): The domain host of the API.
                 path (str): The path of the API after the domain.
                 url_params (dict): An optional set of query parameters in the request.
             Returns:
                 dict: The JSON response from the request.
             """
            url_params = url_params or {}  # Gets the optional parameters or sets the field to blank
            url = '{0}{1}'.format(host, quote(path.encode('utf8')))  # encodes path to utf8 standards.
            headers = self.authentication()  # api_key dictionary

            print(u'Querying {0} ...'.format(url))

            response = requests.request('GET', url, headers=headers, params=url_params)

            return response.json()

        def search_params(self) -> dict:
            """
            Creates a dictionary of search parameters.
            :return: dict
            """
            url_params = {'term': self.term.replace(' ', '+'),
                          'location': self.location.replace(' ', '+'),
                          # location.replace() replaces any spaces " " with a "+".
                          'limit': self.limit}  # limits the number of items in response

            return url_params

        def perform_search(self):

            params = self.search_params()
            response = self.request(self.api_host, self.search_path, params)

            return response

        def grocery(self):
            """
            Takes the search and returns a json like response.
            Pulls out the businesses from the response.
            Iterates over the businesses creating grocery business objects.
            appends those grocery B.O. to a list.
            :return:
            """
            response = self.perform_search()
            bus = response.get("businesses")
            # print(response)
            for b in bus:
                g = groc()
                g.set_name(b["name"])
                loc = b["location"]
                g.set_address1(loc["address1"])
                g.set_address2(loc["address2"])
                g.set_city(loc["city"])
                g.set_state(loc["state"])
                g.set_zipcode(loc["zip_code"])

                self.grocery_list.append(g)

        def get_list(self):
            """
            returns the list of objects
            :return:
            """
            if self.grocery:
                return self.grocery_list
            else:
                print("Empty grocery list")

        def display_list_unfiltered(self) -> list:
            """
            PATRICIA!!!!!!!!!!
            Formats strings for name/address output.
            This returns a list.
            DOES NOT FILTER RESULTS
            :return: list
            """
            self.grocery()  # Runs the api call.
            disp_obj = self.get_list()
            new_list = []
            new_string = ""
            for i in disp_obj:
                if i.get_address2() != None:
                    new_string = """
    {}
    {}
    {}
    {}, {} {}
     """.format(i.get_name(), i.get_address1(), i.get_address2(), i.get_city(), i.get_state(), i.get_zipcode())

                else:
                    new_string = """
    {}
    {}
    {}, {} {}
     """.format(i.get_name(), i.get_address1(), i.get_city(),
                i.get_state(), i.get_zipcode())

                if new_string not in new_list:
                    new_list.append(new_string)
                    print(new_string)

            return new_list

        def display_string_list(self) -> list:
            """
            PATRICIA!!!!!!!!!!
            Formats strings for name/address output.
            This returns a list.
            :return: list
            """
            self.grocery()  # Runs the api call.
            disp_obj = self.get_list()
            new_list = []
            new_string = ""
            for i in disp_obj:
                if i.get_address2() != None:
                    new_string = """
    {}
    {}
    {}
    {}, {} {}
     """.format(i.get_name(), i.get_address1(), i.get_address2(), i.get_city(), i.get_state(), i.get_zipcode())

                else:
                    new_string = """
    {}
    {}
    {}, {} {}
     """.format(i.get_name(), i.get_address1(), i.get_city(),
                i.get_state(), i.get_zipcode())

                if "walmart" in new_string.lower():
                    if new_string not in new_list:
                        new_list.append(new_string)
                        for j in new_list:
                            listbox_place.insert(1, j)
                            break
                break

            return new_list

        def display_list(self):
            """
            Prints contents of list to the console.
            :return:
            """
            for gr in self.get_list():
                gr.display()

    def write_to_file(results):
        """
        THIS CREATES 8 files when run through repeated tests. This creates
        deliverables for testing.
        :param results: list
        :return:
        """
        global fileName
        now = datetime.now()
        fileName = "{}{}{}SearchResults.txt".format(now.hour, now.minute, now.second)
        with open(fileName, "wt+") as fn:
            for i in results:
                n = i + "\n"
                fn.write(n)

    def repeated_tests():
        zip_code_again = entry_zip.get()
        test_list = [("Walmart", zip_code_again)]
        count = 1

        for i in test_list:
            # print("Test #",count)
            # print("-"*100)
            # print("{}: {}".format(*i))
            yd = YelpData("clientsecret.json", i[0], i[1], 10)
            # a = yd.display_list_unfiltered()
            a = yd.display_string_list()
            write_to_file(a)
            count += 1
            time.sleep(10)

    # if __name__ == "__main__":
    # yd = YelpData("clientsecret.json", "Walmart", "30157", 10) #filename of json for api, "search term" "location" "limit of results"
    # yd.grocery() #compiles the list, call yd.get_list() after to use it as an iterable object.
    # yd.display_string_list()

    # #########################################Walmart Scrapper#######################################
    # Coder: Rebecca Makus

    class krogLoc:

        def __init__(self):
            self.__loc = ""
            self.__secret = ""
            self.__ID = ""
            self.__t = object
            self.__r = object
            self.__cnt = ""
            self.__info = {}
            self.__prod = {}
            self.__idAddressDict = {}
            self.__listIds = []
            self.__srch = ""
            self.__fpDict = {}
            self.__fullList = []

        def main(self, userLoc, userCnt, userSrch):
            self.__loc = userLoc
            self.__cnt = userCnt
            self.__srch = userSrch
            self.getID()
            self.getSecret()
            self.getAccess()
            self.getLoc(self.__loc, self.__cnt)
            self.dictLoc()
            self.getProd(self.__cnt, self.__srch)
            self.dictProd()
            self.getInfo()
            return self.__fullList

        def getID(self):
            with open("kroger2.txt", "r") as f:
                lines = f.readlines()
                self.__ID = lines[0].rstrip()
            return self.__ID

        def getSecret(self):
            with open("kroger2.txt", "r") as f:
                lines = f.readlines()
                self.__secret = lines[1].rstrip()
            return self.__secret

        def getAccess(self):
            URL = 'https://api.kroger.com/v1/connect/oauth2/token'
            DATA = {'grant_type': 'client_credentials', 'scope': "product.compact"}
            HEADER = {'Content-Type': "application/x-www-form-urlencoded"}
            self.__t = requests.post(url=URL, headers=HEADER, data=DATA, auth=(self.__ID, self.__secret))
            return self.__t

        def getLoc(self, userLoc, userCnt):
            self.__loc = userLoc
            self.__cnt = userCnt
            rDict = self.__t.json()
            myAuth = rDict['access_token']
            URL = 'https://api.kroger.com/v1/locations'
            PARAMS = {'filter.chain': 'Kroger', 'filter.zipCode.near': self.__loc, 'filter.limit': self.__cnt,
                      'filter.radiusInMiles': '100'}
            HEADER = {'Cache-Control': 'no-cache', 'Authorization': 'Bearer {}'.format(myAuth)}
            self.__r = requests.get(url=URL, headers=HEADER, params=PARAMS)
            self.__info = self.__r.json()
            with open("krogerLocInfo.txt", "w") as f:
                f.write(str(self.__info))
            return self.__info

        def dictLoc(self):
            a = self.__info['data']
            ids = {}
            group = {}
            count = 0
            for i in a:
                group[count] = i
                b = group[count]
                c = b['locationId']
                self.__listIds.append(c)
                d = b['address']
                e = d['addressLine1'] + ", " + d['city'] + ", " + d['state'] + " " + d['zipCode']
                ids[c] = e
                count = count + 1
            with open("locDict.txt", "w") as f:
                f.write(str(ids))
            self.__idAddressDict = ids
            return self.__idAddressDict

        def getProd(self, userCnt, userSrch):
            self.__cnt = userCnt
            self.__srch = userSrch
            rDict = self.__t.json()
            x = 0
            myAuth = rDict['access_token']
            URL = 'https://api.kroger.com/v1/products'
            HEADER = {'Authorization': 'Bearer {}'.format(myAuth), 'Content-Type': 'application/json',
                      'scope': "product.compact"}
            while x < (int(self.__cnt)):
                loc = self.__listIds[x]
                PARAMS = {'filter.locationId': loc, 'filter.term': self.__srch, 'filter.limit': self.__cnt,
                          'filter.fulfillment': "ais", 'filter.radiusInMiles': '100'}
                self.__r2 = requests.get(url=URL, headers=HEADER, params=PARAMS)
                prod = self.__r2.json()
                self.__prod[loc] = prod
                x = x + 1
            else:
                with open("krogerProdInfo.txt", "w") as f:
                    f.write(str(self.__prod))
                return self.__prod

        def dictProd(self):
            fullDict = {}
            for l in self.__listIds:
                z = self.__prod[l]
                a = z['data']
                prods = {}
                group = {}
                count = 0
                for i in a:
                    group[count] = i
                    b = group[count]
                    c = b['description']
                    d = b['items']
                    da = d[0]
                    try:
                        e = da['price']
                        f = e['regular']
                    except KeyError:
                        f = "Price not available"
                    prods[c] = f
                    count = count + 1
                fullDict[l] = prods
                # print(prods)
            else:
                with open("prodDict.txt", "w") as f:
                    f.write(str(fullDict))
                self.__fpDict = fullDict
                return self.__fpDict

        def getInfo(self):
            s_num_1 = 300  # start number

            for l in self.__listIds:
                listbox_product.insert(0, "")
                listbox_Price.insert(0, "")
                a = self.__idAddressDict[l]
                b = self.__fpDict[l]
                c = a, b
                listbox_place.insert(0, a)
                for i in b:
                    listbox_product.insert(1, i)
                    listbox_Price.insert(1, b[i])
                    listbox_place.insert(0, "")
                    s_num_1 += 35
                self.__fullList.append(c)
            with open("fullList.txt", "w") as f:
                f.write(str(self.__fullList))
            return self.__fullList

    # Make the GUI window
    window = Tk()
    window.title("Grocery Adviser")

    image2 = Image.open('vegetables.jpg')
    image1 = ImageTk.PhotoImage(image2)
    w = image1.width()
    h = image1.height()

    # window.configure(background=image1)
    window.geometry("%dx%d+0+0" % (w, h))
    image = Label(window, image=image1)
    image.pack()

    ment = StringVar(window)

    canvas1 = Canvas(image, width=w, height=h, borderwidth=10, relief='raised', bg="papaya whip")
    canvas1.pack(pady=65, padx=100)
    welcome = Label(window, text='Welcome to Grocery Adviser',
                    anchor="w", bd=12, font=('Times New Roman', 40, "bold"), bg="papaya whip", fg="red")

    canvas1.create_window(650, 50, window=welcome, )

    # #########################################Functions#######################################

    def walmart_kroger():

        global variable

        try:
            # Grabs entry of Product name
            product_n = product_entry.get()

            # Grabs entry of zip
            zip_code_entry = entry_zip.get()

            # How many
            how_many = int(variable.get())

            kroger_info = krogLoc()
            kroger_info.main(zip_code_entry, how_many, product_n)

            x = WS()

            # Get the price of the product
            price_product = x.findPrice()

            # Get the product name from the area
            info = x.searchWalmart(product_n, how_many)

            # Test List
            try_list = []

            for i in info:
                # Appends file to list to test
                try_list.append(i)
                try_list.append(price_product)

                # Puts the items to the listbox
                listbox_product.insert(0, i)
                listbox_Price.insert(0, price_product)

            print(try_list)

        except ValueError:
            messagebox.showinfo("Number not chosen", "You need to put in whether you want 5 or 10 items shown")
        except KeyError:
            messagebox.showinfo("Zip code", "You need to put in a 5 digit zip code")
        except IndexError as e:
            messagebox.showinfo("Not enough",
                                "No search results with given search location / item / or number of items\n"
                                "for Krogers or Walmart\n"
                                "Try to change zip code")
            print(str(e), str(e).__class__())

            repeated_tests()

    # ######################################### List Boxes #######################################

    # Listbox for price
    listbox_Price = Listbox(window, width=30, height=15, bg="old lace", fg="red", borderwidth=10, relief='sunken')
    canvas1.create_window(625, 400, window=listbox_Price)

    # Listbox for Product
    listbox_product = Listbox(window, width=30, height=15, bg="old lace", fg="red", borderwidth=10, relief='sunken')
    canvas1.create_window(400, 400, window=listbox_product)

    # Listbox for Place
    listbox_place = Listbox(window, width=35, height=15, bg="old lace", fg="red", borderwidth=10, relief='sunken')
    canvas1.create_window(850, 400, window=listbox_place)

    # #########################################Entry Boxes#######################################

    global product_entry
    global entry_zip

    # 1st entry box and title (product)
    enter_name = Label(window, text='(Enter Product Name)')
    enter_name.config(font=('Times New Roman', 15), bg="papaya whip", fg="red")
    canvas1.create_window(450, 120, window=enter_name)

    product_entry = Entry(window, textvariable=ment)
    canvas1.create_window(450, 150, window=product_entry)

    # 2nd entry box and title (Zip)
    zip_code = Label(window, text='(Zip code)')
    zip_code.config(font=('Times New Roman', 15), bg="papaya whip", fg="red")
    canvas1.create_window(650, 120, window=zip_code)

    entry_zip = Entry(window)
    canvas1.create_window(650, 150, window=entry_zip)

    # #########################################Labels for List Boxes#######################################

    # Product place
    p_name = Label(window, text='Store Information', bg="papaya whip", fg="red")
    p_name.config(font=('Times New Roman Bold', 15))
    canvas1.create_window(850, 250, window=p_name)

    # Product Detail title (Information goes under this)
    product_detail = Label(window, text='Product Detail', bg="papaya whip", fg="red")
    product_detail.config(font=('Times New Roman Bold', 15))
    canvas1.create_window(400, 250, window=product_detail)

    # Product Price title (Information goes under this)
    product_price = Label(window, text='Product Price', bg="papaya whip", fg="red")
    product_price.config(font=('Times New Roman Bold', 15))
    canvas1.create_window(625, 250, window=product_price)

    # ############################## Search Button ########################################

    var = StringVar(window)

    searchButton = Button(window, text="Search", command=walmart_kroger, bg="pink")
    canvas1.create_window(800, 150, window=searchButton)

    # ############################## Reset Button ########################################

    def clear_entry():
        listbox_place.delete(0, 'end')
        listbox_Price.delete(0, 'end')
        listbox_product.delete(0, 'end')
        product_entry.delete(0, 'end')
        entry_zip.delete(0, 'end')

    varReset = StringVar(window)

    resetButton = Button(window, text="Reset", command=clear_entry, bg="pink", )
    canvas1.create_window(900, 150, window=resetButton)

    # ############################## Drop Down List ########################################

    global num_choice
    global variable

    var = StringVar(window)

    choices = {"5", "10"}  # Dictionary with options
    var.set('Display No.')  # set the default option

    variable = StringVar(window)
    variable.set("Choose Number")

    w = OptionMenu(window, variable, *choices)
    w.config(bg="pink")

    canvas1.create_window(450, 200, window=w)

    # ############################## Sort By List ########################################

    # global either_or
    #
    # var2 = StringVar(window)
    #
    # choices2 = {'Store', 'Price'}  # Dictionary with options
    # var2.set('Search By')  # set the default option
    #
    # either_or = StringVar(window)
    # either_or.set("Search By")
    #
    # y = OptionMenu(window, either_or, *choices2, )
    # y.config(bg="pink")
    #
    # canvas1.create_window(650, 200, window=y)
    #
    # window.mainloop()


redo()
