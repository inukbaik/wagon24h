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

## Deployment with Crontab

This project can be deployed on a live system by executing the `main.py` file on a server with Python installed. You can automate the execution of `main.py` at regular intervals using `crontab`, a time-based job scheduler in Unix-like operating systems.

### Setting Up Crontab

1. **Access Your Server**: Connect to your Linux server using SSH.

2. **Open Crontab for Editing**: Run the following command to open the crontab file for editing:
   ```bash
   crontab -e
   ```

3. **Add a Cron Job**: In the crontab file, add a new line to specify when you want `main.py` to run. For example, to run `main.py` every day at 12 PM EST (5 PM UTC), you can add the following line:
   ```bash
   0 17 * * * /usr/bin/python3 /path/to/main.py
   ```
   Replace `/path/to/main.py` with the actual path to your `main.py` file.

4. **Save and Exit**: After adding the cron job, save and exit the crontab editor.

### Example Crontab Entry

Here's an example of a crontab entry to run `main.py` every day at 12 PM EST (5 PM UTC):
```bash
0 17 * * * /usr/bin/python3 /path/to/main.py
```

### Checking Crontab Status

To check the status of your crontab and verify that the cron job was successfully added, you can run the following command:
```bash
crontab -l
```

### Additional Notes

- Make sure that the Python interpreter path (`/usr/bin/python3`) is correct for your system.
- Ensure that the file permissions for `main.py` allow it to be executed by the user running the cron job.

## Built With

- Linux
- Python
- Selenium
- Tweepy
- Requests

## Environment

- **Operating System**: Ubuntu 20.04 LTS
- **Python Version**: Python 3.11.5

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.