# Wagon24h
## Bring A Trailer Wagon Scraper

This Python script scrapes wagon listings from Bring A Trailer website, downloads images, and creates tweets with information about each wagon. It is intended to automate the process of sharing wagon listings on Twitter.
Check out the Twitter account created with this script: [Wagon24h](https://twitter.com/Wagon24h)

## Getting Started

To get a copy of the project up and running on your local machine, follow these steps:

### Prerequisites

Ensure you have Python installed on your system.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/inukbaik/wagon24h.git
   ```

2. Install dependencies:

   ```bash
   pip install selenium tweepy requests python-dotenv
   ```

3. Set up environment variables:

   - Create a `.env` file in the project directory.
   - Add the following variables to the `.env` file and replace `YOUR_VALUE` with your actual API keys and tokens:

     ```dotenv
     BEARER_TKN=YOUR_VALUE
     API_KEY=YOUR_VALUE
     API_SECRET=YOUR_VALUE
     ACCESS_TKN=YOUR_VALUE
     ACCESS_SECRET=YOUR_VALUE
     ```

## Usage

1. Ensure you have set up the `.env` file correctly with your Twitter API keys and tokens.
2. Run the `main.py` file:

   ```bash
   python main.py
   ```

## Running the Tests

This project does not currently include automated tests.

## Deployment

This project can be deployed on a live system by executing the `main.py` file on a server with Python installed. You may want to schedule it to run at regular intervals using tools like cron jobs.

## Built With

- Python
- Selenium
- Tweepy
- Requests

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.