from booking.booking import Booking

with Booking() as bot:
    try:
        bot.land_page()
        bot.change_currency(currency='USD')
        bot.search_dest(city=input("Where you want to go ? " ))
        bot.check_date(check_in_date=input("What is the check in date ? " ),
                             check_out_date=input("What is the check out date ? " ))
        bot.select_travel_options(adults=int(input("How many adults ? " )),
                                  children=input(input("How many children ? " )),
                                  rooms=int(input("How many rooms ? " )))
        bot.apply_filters()
        bot.refresh()  # A workaround to let our bot to grab the data properly
        bot.display_report()

    except Exception as e:
        if 'in PATH' in str(e):
            print(
                'You are trying to run the bot from command line \n'
                'Please add to PATH your Selenium Drivers \n'
                'Windows: \n'
                '    set PATH=%PATH%;C:path-to-your-folder \n \n'
                'Linux: \n'
                '    PATH=$PATH:/path/toyour/folder/ \n'
            )
        else:
            raise

    finally:
        bot.quit()

