<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/e8940dce-3346-47e5-9574-a0af8a9fe981" />
# 🤖 AI Sales Development Rep (SDR) Voice Agent

![Project Status: Beginner / Prototype](https://img.shields.io/badge/Status-Beginner%20%2F%20Prototype-yellow)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

**An automated AI voice agent that calls leads, explains services, and books meetings.**

This is a beginner-friendly project designed to build a functional AI SDR from scratch. It is currently in the **early prototype stage**. The goal is to create an agent that is triggered by a web event (like a user logging in), initiates a phone call, has a natural conversation to qualify a lead, and schedules a call on a calendar.

## 🏗️ Architecture

The project is built on a modern tech stack designed for low-latency, real-time voice interactions.

![AI Sales Agent Architecture Diagram](image_0.png)

1.  **Trigger:** A web login or event sends a signal to our backend.
2.  **Backend (Python/FastAPI):** The central brain that receives the trigger and orchestrates the workflow.
3.  **Telephony (Twilio):** Handles the physical phone call to the user.
4.  **AI Brain (OpenAI Realtime API):** A single model that listens, thinks, and speaks in real-time, providing a natural conversational experience.
5.  **Booking (Cal.com/Calendly):** The AI can call this API to check availability and book meetings.

## 🚀 Current Status (Beginner Stage)

This repository is a work in progress. We are following a 2-month roadmap to build the complete system.

| Feature | Status | Notes |
| :--- | :---: | :--- |
| **Basic Call Initiation** | ✅ Done | Can trigger a call from Python to a phone number. |
| **Simple Text-to-Speech** | ✅ Done | The call plays a static, pre-recorded message. |
| **Real-time AI Conversation**| 🚧 In Progress | Connecting Twilio Media Streams to OpenAI's Realtime API for dynamic talking. |
| **Web Login Trigger** | 📅 Planned | Automating the call based on a web event. |
| **Calendar Booking** | 📅 Planned | Integrating Calendly/Cal.com API for scheduling. |
| **Simultaneous Calls** | 📅 Planned | Handling multiple calls at once (requires Twilio upgrade). |

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Server Framework:** FastAPI
* **Telephony Provider:** Twilio (Voice & Media Streams)
* **AI Model:** OpenAI Realtime API (`gpt-4o-realtime-preview`)
* **Booking API:** Cal.com or Calendly
* **Environment Management:** `python-dotenv`

## 📋 Prerequisites

Before you begin, you will need accounts for the following services:

1.  **Twilio:** A free trial account and a purchased phone number with Voice capabilities.
2.  **OpenAI:** An API account with access to the `gpt-4o-realtime-preview` model.
3.  **Python:** Python 3.9 or higher installed on your machine.
4.  **ngrok:** A tool to expose your local server to the internet for Twilio to connect to.

## ⚡ Getting Started (Initial Prototype)

Follow these steps to run the most basic version of the calling bot.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/ai-sales-agent.git](https://github.com/your-username/ai-sales-agent.git)
    cd ai-sales-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```env
    TWILIO_ACCOUNT_SID=your_twilio_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=+1234567890
    OPENAI_API_KEY=your_openai_api_key
    ```

5.  **Run the initial script:**
    ```bash
    python simple_call.py
    ```

## 🗺️ Roadmap

* **Month 1:** Establish the core voice loop.
    * Connect Twilio Media Streams to OpenAI for low-latency speech-to-speech.
    * Create a basic system prompt for the sales persona.
    * Build the web trigger automation.
* **Month 2:** Add advanced features and scale.
    * Implement "tool calling" for calendar availability checks.
    * Handle interruptions and improve conversational flow.
    * Upgrade Twilio to handle simultaneous calls.

## 🤝 Contributing

Contributions are welcome, especially from other beginners learning alongside us! Please feel free to submit a Pull Request or open an Issue to discuss any changes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
