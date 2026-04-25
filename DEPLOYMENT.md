# Deployment Guide: Telegram Multi-Sender Bot

Follow these steps to deploy your bot to **Render** and connect it to your Telegram account.

## 1. Prepare Your Credentials
You need the following information before you start:

*   **API_ID & API_HASH**: Get these from [my.telegram.org](https://my.telegram.org) under "API Development Tools".
*   **PHONE_NUMBER**: The phone number of the Telegram account the bot will use (e.g., `+2519...`).
*   **MONGO_URI**: A MongoDB connection string. You can get a free cluster from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
    *   Example: `mongodb+srv://<username>:<password>@cluster.mongodb.net/test`

## 2. Generate a String Session (CRITICAL)
Since Render restarts periodically, you cannot use a standard session file. You must use a `STRING_SESSION`.

1.  Run the generation script locally:
    ```bash
    python generate_session.py
    ```
2.  Follow the prompts to log in.
3.  Copy the long string it outputs. **Keep this secret!**

## 3. Deploy to Render
You can deploy using the `render.yaml` Blueprint:

1.  Push your code to a GitHub or GitLab repository.
2.  Log in to [Render](https://render.com).
3.  Click **New +** and select **Blueprint**.
4.  Connect your repository.
5.  Render will detect `render.yaml` and ask for the following Environment Variables:
    *   `API_ID`
    *   `API_HASH`
    *   `PHONE_NUMBER`
    *   `MONGO_URI`
    *   `STRING_SESSION` (The long string you generated in Step 2)
6.  Click **Apply**.

## 4. Usage
Once the bot is "Live" on Render:
1.  Open Telegram and go to your **Saved Messages** or chat with yourself.
2.  Type `/start` to verify the bot is active.
3.  Use `/help` to see all commands.

### Keeping the Bot Alive
Render's free tier spins down after 15 minutes of inactivity. To keep it alive, you can use a free service like [Cron-job.org](https://cron-job.org) or [UptimeRobot](https://uptimerobot.com) to ping your Render URL every 10 minutes:
`https://your-app-name.onrender.com/` (The health check endpoint).
