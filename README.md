# Stock Trading Platform (Website)
Stock trading platform simulator to teach young kids about Finance/stock markets, uses IEX API to pull live stock prices from the NASDAQ.

## Description
### Tech Stack
- Flask: Manages database executions, routing and function calls
- HTML (Jinja) / CSS (Bootstrap): Used to render pages quickly and to make them look visually appealing
- SQL
- Python: Database executions, template rendering, function calls
- IEX Cloud API: Pulls live stock prices from the NASDAQ

### Challenges
- Executing SQL queries according to the user's actions (buying stocks/selling stocks/fetching portfolio etc.)

### Requirements
1. Install Python (https://python.org/download/)
1. Install SetupTools ($ pip install setuptools)
1. Install pip ($ easy_install pip)
1. Install Flask ($ pip install flask)
1. Install cs50 module ($ pip install cs50)
1. Install flask_session ($ pip install flask_session)
1. Install requests ($ pip install requests)
1. Create IEX API Access Token (see below)

### Create API Access Token
- Visit iexcloud.io/cloud-login#/register/.
- Select the “Individual” account type, then enter your name, email address, and a password, and click “Create account”.
- Once registered, scroll down to “Get started for free” and click “Select Start plan” to choose the free plan.
- Once you’ve confirmed your account via a confirmation email, visit https://iexcloud.io/console/tokens.
- Copy the key that appears under the Token column (it should begin with pk_).

### How to run (must execute code everytime the program is ran)
1. $ export API_KEY=value (where value is the generated key from the steps above) -- for UNIX shells
- $ set API_KEY=value (where value is the generated key from the steps above) -- for windows
1. $ flask run -- for UNIX shells
- $ python app.py -- for windows

# Features

## Login Page
![stockme-login-photo](https://user-images.githubusercontent.com/89746098/187583895-0a24481a-5189-4a2f-a0ee-9e8e34563249.jpg)

## Register Page
![stockme-register-photo](https://user-images.githubusercontent.com/89746098/187583899-be397d17-0053-4c14-abbc-3fd41703264b.jpg)

## Navbar
- stockme.io/logo: Redirects user to the home page, can quote stock prices.
- Buy: Redirects user to the buy page, can buy stocks.
- Sell: Redirects user to the sell page, can sell stocks.
- My Transactions: Redirects user to the transactions page, can view transaction history.
- My Friends: Redirects user to the friends page, can add friends and view their portfolios.
- My Portfolio: Redirects user to the portfolio page, can view their personal portfolio and its breakdown.
- Log Out: Logs user out.
![stockme-navbar-photo](https://user-images.githubusercontent.com/89746098/187583907-d03285ee-0eb5-42a5-9fb8-22948fbeaca9.jpg)

## Home Page
![stockme-home-photo](https://user-images.githubusercontent.com/89746098/187583913-2b890e61-df71-467f-ab98-a5a609ad4b0f.jpg)

## Buy Page
![stockme-buy-photo](https://user-images.githubusercontent.com/89746098/187583921-c15e9818-ae38-4560-8bd2-925c0f655736.jpg)

## Sell Page
![stockme-sell-photo](https://user-images.githubusercontent.com/89746098/187583930-29ca5e4d-5bbd-4e88-ac27-ee13783769a2.jpg)

## My Transactions Page
![stockme-history-photo](https://user-images.githubusercontent.com/89746098/187583946-296045ed-8ac5-44f9-80e1-b12ee43d12a1.jpg)

## My Friends Page
![stockme-friends-photo](https://user-images.githubusercontent.com/89746098/187583957-24a6bd49-a5b5-40c0-bb1d-0971ccb84d8e.jpg)

## My Portfolio Page
![stockme-portfolio-photo](https://user-images.githubusercontent.com/89746098/187583989-12f06bb9-b6fb-4db4-91e9-a5fbe5974e5f.jpg)

