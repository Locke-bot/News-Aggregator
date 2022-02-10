# News-Aggregator
This is my first project using the react library, the project is about scraping popular news sites in Nigeria and displaying their top stories all in one place without a need for 'website hopping'.

It uses a django rest api for the backend, BeautifulSoup and requests for the news site scraping, apscheduler to schedule the site scraping, and ReactJS fir the frontend.


<h2>Django Instructions:</h2>
<ul>
    <li>set up a virtual environment and activate it</li>
    <li>git clone https://github.com/Locke-bot/News-Aggregator.git</li>
    <li>cd News-Aggregator</li>
    <li>pip install -r requirements.txt</li>
    <li>if there is an issue, upgrading pip using python -m pip install --upgrade pip should solve it</li>
    <li>run python manage.py runserver</li>
    <li>the site is being served at http://localhost:8000/ by default</li>
</ul>

<h2>React Instructions:</h2>
<ul>
    <li>you must have node installed and npm available on the command line</li>
    <li>activate the virtual environment</li>
    <li>cd News-Aggregator/news-agg-frontend</li>
    <li>run npm install</li>
    <li>run npm start, you should be redirected to http://localhost:3000/</li>
</ul>


The interval between when the websites would be scraped is defined in settings;
SCRAPE_INTERVAL = 10; it is given in minutes, it can be changed as deemed fit.
