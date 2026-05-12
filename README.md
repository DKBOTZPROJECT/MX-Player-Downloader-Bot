# 🚀 MX Player Downloader Bot

MX Player Downloader Bot Is A Powerful Telegram Bot That Allows Users To Easily Download Videos From MX Player. Simply Send The Video Link, And The Bot Will Automatically Fetch And Upload It To Telegram.

## ✨ Features

* 🎬 Download Videos From MX Player Links
* ⚡ Fast Processing & High-Speed Downloads
* 📥 Automatic Link Detection & Fetching
* 📤 Direct Upload To Telegram
* 📦 Output Format Choice (MP4 / MKV) Before Each Download
* ☁️ Automatic Gofile.io Fallback For Files Larger Than Telegram's 2 GB Limit
* 📜 /logs Admin Command To Inspect The Live Bot Log File
* 🧠 Smart Error Handling & Retry System
* 📊 Clean And User-Friendly Experience

---
## ⚙️ Environment Variables

| Variable  | Description                      |
| --------- | -------------------------------- |
| API_ID    | Get From https://my.telegram.org |
| API_HASH  | Get From https://my.telegram.org |
| BOT_TOKEN | Get From @BotFather              |

<details>
<summary>🧩 Optional Variables</summary>

<br>

| Variable         | Description                                        |
| ---------------- | -------------------------------------------------- |
| OWNER_USERNAME   | Bot Owner Username (default: DKBOTZHELP)           |
| UPI_ID           | Your UPI ID For Payments (default: dkbotzpro@ybl)  |
| CHANNEL_USERNAME | Your Channel Username Without @ (default: DKBOTZ)  |
| LOG_CHANNEL      | Private Channel ID For Logs (must start with -100) |
| FSUB_CHANNEL     | Force Subscribe Channel ID (must start with -100)  |
| ADMINS           | Space Separated Admin User IDs                     |
| DATABASE_URL     | MongoDB Database URL                               |
| DATABASE_NAME    | Database Name (default: DKBOTZMXDOWNLOADER)        |
| TG_UPLOAD_LIMIT  | Max Bytes To Upload To Telegram Before Falling Back To Gofile (default: 2147483648 = 2 GiB) |
| GOFILE_TOKEN     | Optional Gofile.io Account Token (default: guest uploads) |
| LOG_FILE         | Path For The Bot Log File Used By /logs (default: bot.log) |

</details>

---

## Deploy Option
### ⚠️ Before Deploy Or Hosting, Read Notes Section

[Please Read The Notes Section Here](https://github.com/DKBOTZPROJECT/MX-Player-Downloader-Bot/blob/DKBOTZ/README.md#notes)

<details><summary>Deploy To Heroku</summary>
<p>
<br>
<a href="https://heroku.com/deploy?template=https://github.com/DKBOTZPROJECT/MX-Player-Downloader-Bot">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy To Heroku">
</a>
</p>
</details>

<details><summary>💻 Deploy On VPS (Manual Setup)</summary>
<p>

#### 📌 Step 1: Update System

```bash
apt update && apt upgrade -y
```

#### 📌 Step 2: Install Required Packages

```bash
apt install python3 python3-pip ffmpeg git -y
```

#### 📌 Step 3: Clone Repository

```bash
git clone https://github.com/DKBOTZPROJECT/MX-Player-Downloader-Bot
cd MX-Player-Downloader-Bot
```

#### 📌 Step 4: Install Requirements

```bash
pip3 install -r requirements.txt
```

#### 📌 Step 5: Set Environment Variables

```bash
export API_ID=your_api_id
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token
```

#### 📌 Step 6: Run Bot

```bash
bash start.sh
```
</p>
</details>

---

## 💡 How To Use

1. Copy The MX Player Video Link
2. Send It To The Bot
3. Pick The Video Quality
4. Pick The Audio Track(s) (Optional)
5. Choose The Output Format (🎬 MP4 Or 🎞️ MKV)
6. Wait A Few Seconds
7. Get Your Video Ready To Download 🎉 (Or A Gofile Link For Files > 2 GB)

### Admin Commands

* `/logs` — Reply With The Live Bot Log File (Restricted To `ADMINS`)

---

## 🐞 Report Issues / Request Features

If You Face Any Issues Or Want New Features, You Can:

### 📢 Report On Telegram

* 👨‍💻 Developer: [𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬](https://t.me/DKBOTZHELP)
* 📢 Support Channel: [𝐃𝐊𝐁𝐎𝐓𝐙](https://t.me/DKBOTZ)
* 💬 Support Group: [𝐃𝐊𝐁𝐎𝐓𝐙 𝐒𝐔𝐏𝐏𝐎𝐑𝐓](https://t.me/DKBOTZSUPPORT)

<details><summary>🛠️ Report On GitHub (Recommended)</summary>
<p>

👉 Go To: [Github Issues](https://github.com/DKBOTZPROJECT/MX-Player-Downloader-Bot/issues)

#### 📌 While Reporting Issue, Include:

* Full Error Logs
* Screenshot (If Possible)
* Proper Description Of Problem
* Steps To Reproduce Issue

#### 💡 For Feature Request:

* Clearly Explain Feature Idea
* Provide Use Case
* Add Example If Possible

</p>
</details>

---

## ⭐ Support The Project

If You Like This Project, Don’t Forget To ⭐ Star The Repository
It Helps A Lot And Motivates For More Updates 🚀

---

## Notes
<details><summary>🚀 How To Increase Download Speed</summary>
<p>
Download Speed Basically Depends On 2 Factors:<br>

1. 🇮🇳 <b>Use Indian Server</b> - MX Player Links Work Faster On Indian Servers. You Can Use A Proxy Or Indian Server To Increase Speed.<br><br>

2. ⚡ <b>Use Fast VPS Server</b> - Use A High-Speed VPS With Good Network Performance. If The Server Is Located In India, Speed Will Be Even Better And More Stable.
</p>
</details>

<details><summary>👨‍💻 By Developer</summary>
<p>

- Iski Speed Ka Issue Indian Server Use Karne Se Fix Ho Jaayega Pata Nahi Yesa Kyu Hai Mujhko Baad Me Time Milega To Me Iske Upper Ek Baar Kaam Karunga Solve Karne Ki Kosis Karunga. 

- Jo API isme Use Kiya Hu Vah Local Server Par Run Ho Raha Hai isliye Jyda Requests Mat Dalana. Baad Me isko Other Server Par Daal Dunga.

- Agar Bot Me Koi Issues Ho To Mere Support Group Ya Github ke Issues Me Daal Sakte Ho.

</p>
</details>

---

## 💳 Credits

* 👨‍💻 Developer: [𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬](https://t.me/DKBOTZHELP)
* 📢 Support Channel: [𝐃𝐊𝐁𝐎𝐓𝐙](https://t.me/DKBOTZ)
* 💬 Support Group: [𝐃𝐊𝐁𝐎𝐓𝐙 𝐒𝐔𝐏𝐏𝐎𝐑𝐓](https://t.me/DKBOTZSUPPORT)

📌 Report Issues To Developer Or Support Group

---
