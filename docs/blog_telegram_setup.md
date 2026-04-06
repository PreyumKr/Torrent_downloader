# Building an Intelligent Media Downloader: From Telegram Bot to LLM Selection

In the age of self-hosted media, the challenge isn't just downloading content—it's downloading the *right* content and organizing it perfectly for servers like Jellyfin. This post explores the architecture of an automated torrent downloader that uses FastAPI, Telegram, and local LLMs (Ollama) to manage your library.

---

## <a id="index"></a>Index
- <a href="#architecture">The Microservices Architecture</a>
- <a href="#ollama">Intelligent Selection with Ollama</a>
- <a href="#tvmd">Metadata Sync with TVMD API</a>
- <a href="#telegram-setup">Creating Your Telegram Interface</a>
- <a href="#token-security">Securing Your API Token</a>
- <a href="#deployment">Launching the Services</a>

---

## <a id="architecture"></a>The Microservices Architecture
The system is built as a set of decoupled services to ensure reliability and scalability. By separating the Movie API from the Series API, the system can handle different logic paths (like complex season/episode planning for TV shows) without interference.

- **Movie API (Port 8001):** Handles rapid search and high-quality selection for films.
- **Series API (Port 8002):** Manages canonical metadata lookups and local file syncing.
- **Telegram Bot:** A unified client that communicates with both APIs via REST, providing a simple mobile interface for the user.

---

## <a id="ollama"></a>Intelligent Selection with Ollama
One of the biggest pain points in automation is the "wrong download" (e.g., downloading Moana 2 when you wanted Moana). 

The project solves this by passing the search results from PirateBay directly to a local **Ollama** instance (running Llama 3). The LLM performs a semantic analysis of the titles, seed counts, and file sizes. It is instructed to reject sequels and prequels unless specifically asked for, ensuring that your library stays clean and accurate.

---

## <a id="tvmd"></a>Metadata Sync with TVMD API
For TV Series, the system needs to know more than just a name. It needs to know which episodes you already have and which ones are missing. 

1.  The system queries the **TVMD API** to get the canonical structure of a show (number of seasons and episodes per season).
2.  It scans your local **Jellyfin** library to see what's already on disk.
3.  It produces a "Download Plan" that only targets missing content, preventing wasted bandwidth and duplicate files.

---

## <a id="telegram-setup"></a>Creating Your Telegram Interface
The Telegram bot is your remote control. To set it up, you'll need to interact with the "BotFather."

### Finding the BotFather
Search for `@BotFather` on Telegram. Ensure it has the official blue checkmark.

> **[PLACEHOLDER: Image showing BotFather search results]**

### Initiating a New Bot
Use the `/newbot` command. You will be asked for a **Display Name** (what you see in chat) and a **Username** (must end in `bot`, e.g., `my_media_downloader_bot`).

> **[PLACEHOLDER: Image showing the /newbot command flow]**

---

## <a id="token-security"></a>Securing Your API Token
Once the bot is created, BotFather will give you an **HTTP API Token**. 

> **[PLACEHOLDER: Image showing the successful creation message and the API Token]**

**CRITICAL:** This token is a secret key. If someone else has it, they can control your bot. In this project, we store the token in a local `.env` file which is ignored by Git to prevent accidental leaks.

---

## <a id="deployment"></a>Launching the Services
With your token ready, deployment is a simple three-step process:

1.  **Configure:** Copy `.env.example` to `.env` and add your `TELEGRAM_BOT_TOKEN`.
2.  **Start the APIs:** Run `python run_api.py` to launch the Movie and Series services.
3.  **Start the Bot:** Run `python run_telegrambot.py`.

Now, you can simply message your bot `/movie Moana` and let the LLM-powered backend handle the rest.

---
