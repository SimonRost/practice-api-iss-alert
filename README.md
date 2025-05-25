# ISS Alert Project

This project tracks the International Space Station (ISS) and sends an email alert when the ISS is overhead and it is nighttime at your location. The project uses Python and several APIs to achieve this functionality.

## Project Structure

```
day-33_iss_alert/
├── iss_alert.py
├── send_mail.py
├── send_telegram_message.py
├── requirements.txt
├── .env
└── README.md
```

### Files

1. **iss_alert.py**  
    The main script that runs the ISS tracking and alert system. It checks the ISS position, determines if it is overhead, and sends a notification if the conditions are met.

2. **send_mail.py**  
    A helper script to send email notifications using SMTP.

3. **send_telegram_message.py**  
    A helper script to send Telegram notifications using a bot.

4. **requirements.txt**  
    A file listing all the Python dependencies required for the project. Use `pip install -r requirements.txt` to install them.

5. **.env**  
    A file to store sensitive information such as email credentials, location coordinates, and Telegram bot details. Make sure to create this file and add your actual data.

6. **README.md**  
    This documentation file explaining the project.

## How It Works

1. The script fetches the current position of the ISS using the Open Notify API.
2. It checks if the ISS is overhead (within ±5 degrees of your latitude and longitude).
3. It checks if it is nighttime at your location using the Sunrise-Sunset API.
4. If both conditions are met, an email alert is sent to notify you.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/iss_alert.git
    cd iss_alert
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project directory and add the following environment variables:
    ```env
    MY_POS_LAT=your_latitude
    MY_POS_LNG=your_longitude
    EMAIL_FROM=your_email@example.com
    MY_PASSWORD=your_email_password
    EMAIL_TO=recipient_email@example.com
    BOT_TOKEN=your_telegram_bot_token
    CHAT_ID=your_telegram_chat_id
    ```

    - Replace `your_latitude` and `your_longitude` with your location's coordinates.
    - Replace `your_email@example.com` and `your_email_password` with your email credentials.
    - Replace `your_telegram_bot_token` and `your_telegram_chat_id` with your Telegram bot's token and chat ID.

    **Note**: Ensure your `.env` file is excluded from version control by adding it to your `.gitignore` file to keep sensitive information secure.

4. Run the script:
    ```bash
    python iss_alert.py
    ```

## Running on a Schedule

You can automate the script to run periodically using one of the following methods:

### **GitHub Actions**
Use GitHub Actions to run the script in the cloud. Create a workflow file in `.github/workflows/main.yml`:

```yaml
name: ISS Alert Workflow

on:
  schedule:
    # Run every 10 minutes between 8 PM and 6 AM (UTC)
    # Adjust the hours based on your timezone offset
    # To run it only at nighttime saves GitHub Actions minutes, especially as the script sends messages only at nighttime anyway.
    - cron: '*/10 22-23,0-7 * * *'

jobs:
  run-iss-alert:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run ISS Alert script
      env:
        MY_POS_LAT: ${{ secrets.MY_POS_LAT }}
        MY_POS_LNG: ${{ secrets.MY_POS_LNG }}
        EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
        MY_PASSWORD: ${{ secrets.MY_PASSWORD }}
        EMAIL_TO: ${{ secrets.EMAIL_TO }}
        BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
        CHAT_ID: ${{ secrets.CHAT_ID }}
      run: python iss_alert.py
```
Add your environment variables as GitHub Secrets under Settings > Secrets and variables > Actions.

## Dependencies

- `requests`
- `python-dotenv`
- `smtplib`
- `datetime`

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- The basic idea for this project originates from Angela Yu's Python course (100 Days of Code: The Complete Python Pro Bootcamp) and has been expanded by the author, particularly with the addition of sending messages via Telegram.
- [Open Notify API](http://open-notify.org/) for ISS location data.
- [Sunrise-Sunset API](https://sunrise-sunset.org/api) for sunrise and sunset times.

Feel free to contribute or raise issues in the repository!  