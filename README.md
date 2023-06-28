# Detikcom Scraper

Detikcom Scraper is a command-line interface (CLI) program written in Python for scraping news content from the Detikcom news portal. It provides a convenient way to access and analyze the latest news articles from Detikcom, one of Indonesia's prominent online news portals. Sample data scraped using this program can be found in the [data](data) directory.

## Features

- Scraping News Content: Detikcom Scraper allows you to scrape news articles from the Detikcom news portal, giving you access to a vast amount of up-to-date news content.
- Store Scraped Data: You can easily store the scraped news data in CSV or Excel files, making it convenient for further analysis or integration with other tools.
- Advanced Filtering Options: Detikcom Scraper offers advanced filtering options to refine your search. You can filter articles based on specific keywords, categories, and publication time, allowing you to focus on the news articles that matter to you.

## Prerequisites

Before running the program, ensure you have the following installed:
- Python 3.9 or above
- Required Python packages (specified in requirements.txt)

## Installation

1. Clone the repository:

   ```bash
   $ git clone https://github.com/harishartanto/detikcom-scraper.git
   ```

2. Change into the project directory: 

   ```bash
   $ cd detikcom-scraper
   ```
3. Install the required packages: 

   ```bash
   $ pip install -r requirements.txt
   ```

## Usage

To use Detikcom Scraper, follow these steps:

1. Make sure you are in the project directory:

   ```bash
   $ cd detikcom-scraper
   ```

2. Run the `main.py` file:

   ```bash
   $ python main.py
   ```

3. Follow the prompts to specify the topic, category, and publication date of the news articles you want to scrape.

4. The scraped data will be stored in the `data` directory as CSV or Excel files.

## Disclaimer

Detikcom Scraper is a program created for educational purposes only. The program utilizes web scraping techniques to automatically extract news content from the [Detikcom](https://www.detik.com/) news portal.

The program's developer has no official affiliation with Detikcom, and it is developed without official permission or endorsement from Detikcom.

The developer is not responsible for any misuse or improper use of the program. Users are fully responsible for their use of the program and must comply with applicable laws and respect Detikcom's copyright and privacy policies.

Detikcom and all related trademarks remain the property of Detikcom.

The use of this program in any way is solely the user's responsibility, and the developer is not liable for any legal consequences or damages arising from the use of this program.

## License

This project is licensed under the [MIT License](LICENSE). Please read the [LICENSE](LICENSE) file for more details.