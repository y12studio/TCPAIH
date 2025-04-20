# Google Agent Development Kit (ADK) Sample Agents (adk1003-team)

Welcome! This folder contains example "agents" built using Google's Agent Development Kit (ADK). Think of agents like specialized chatbots or assistants that can perform tasks. These examples show how multiple agents can work together as a team and use tools to get things done.

This is a great place to start if you're new to ADK and want to see how it works!

## What You'll Need (Prerequisites)

Before you start, make sure you have these things installed or ready:

1.  **Python 3.13 or newer:** This is a specific version of the Python programming language. You'll need it to run the code.
2.  **`uv`:** This is a fast tool to help manage the extra software packages (called dependencies) that this Python project needs. You can find installation instructions here: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
3.  **Google API Key:** This is like a secret password that lets your agents use Google's AI services (like Gemini). You can get one for free from:
    *   [Google AI Studio](https://aistudio.google.com/app/apikey) (Easiest for getting started)
    *   Google Cloud Vertex AI (More advanced)
4.  **A place to store your API Key:** You'll create a special file (called `.env`) to keep your API key secret and safe.

## Getting Set Up (Setup Instructions)

Follow these steps carefully:

1.  **Open Your Terminal:** Open your command prompt, terminal, or PowerShell window.
2.  **Go to the Right Directory:** Navigate into this specific project folder using the `cd` command:
    ```sh
    cd path/to/agents/adk1003-team
    ```
    (Replace `path/to/` with the actual path on your computer).
3.  **Create Secret Files (`.env`):**
    *   Inside the `adk1003-team` directory, you'll see example files like `.env.example`.
    *   You need to create a *real* secret file named `.env` (just `.env`, starting with a dot and no other name before it).
    *   Copy the contents from `.env.example` into your new `.env` file.
    *   **Important:** Edit the `.env` file and replace `"your-api-key-here"` with the actual Google API key you got in the prerequisites step.
    *   Make sure the file looks like this (if using an AI Studio key):
        ```
        GOOGLE_GENAI_USE_VERTEXAI="False"
        GOOGLE_API_KEY="your-actual-api-key-goes-here"
        ```
        *(If you are using a Vertex AI key and setup, you would change `False` to `True` and configure Vertex settings, but for beginners, `False` and an AI Studio key is recommended).*
4.  **Install Required Software:** Run this command in your terminal. `uv sync` will read the project's requirements and automatically download and install the necessary Python packages.
    ```sh
    uv sync
    ```

## Running the Agents!

Now for the fun part!

1.  **Start the ADK Web Server:** Run the following command in your terminal (make sure you're still in the `agents/adk1003-team` directory):
    ```sh
    uv run adk web
    ```
2.  **See it in Your Browser:** This command starts a local web server on your computer. Your terminal will likely show you an address like `http://127.0.0.1:8000` (it might be a different port number).
3.  **Interact:** Open your web browser (like Chrome, Firefox, etc.) and go to that address. You should see a web page where you can chat with the sample agents!

## How It Works (Development Details for the Curious)

If you want to understand how these agents are built:

*   **Agent Brains (`agent.py`):** The main logic and programming for how each agent behaves is inside the `agent.py` file.
*   **Agent Instructions (`.md` files):** Each agent gets its specific instructions, personality, and goals from a Markdown file (files ending in `.md`, like `agent_root.md`, `agent_greeting.md`, etc.).
*   **Agent Tools (Python Functions):** Sometimes agents need special tools to do things, like looking up information. These tools are defined as simple Python functions (like the `get_taichung_pubarts_list` example mentioned) and are given to the agents that need them.
*   **Making Agents Visible (`__init__.py`):** This special Python file helps the ADK system find and load your agent code when the server starts.

## License

This project code is shared under the Apache License 2.0. You can read the full details in the [LICENSE](/LICENSE) file.


# Google Agent Development Kit (ADK) 範例代理人 (adk1003-team)

歡迎！這個資料夾包含使用 Google Agent Development Kit (ADK) 建構的範例「代理人 (agents)」。您可以將代理人想像成能夠執行任務的特製聊天機器人或助理。這些範例展示了多個代理人如何像團隊一樣協同工作，並使用工具來完成任務。

如果您是 ADK 的新手，想看看它是如何運作的，這裡是個絕佳的起點！

## 您需要準備什麼 (事前準備 / Prerequisites)

在開始之前，請確保您已安裝或準備好以下項目：

1.  **Python 3.13 或更新版本：** 這是 Python 程式語言的一個特定版本。您需要它來運行程式碼。
2.  **`uv`：** 這是一個快速的工具，用於管理這個 Python 專案所需的額外軟體套件 (稱為依賴 / dependencies)。您可以在這裡找到安裝說明：[https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
3.  **Google API 金鑰 (API Key)：** 這就像一個秘密密碼，讓您的代理人可以使用 Google 的 AI 服務（例如 Gemini）。您可以從以下地方免費取得：
    *   [Google AI Studio](https://aistudio.google.com/app/apikey) (最容易上手)
    *   Google Cloud Vertex AI (較進階)
4.  **一個存放 API 金鑰的地方：** 您將建立一個特殊的檔案（名為 `.env`）來安全地保存您的 API 金鑰，避免洩漏。

## 如何設定 (設定步驟 / Setup Instructions)

請仔細按照以下步驟操作：

1.  **開啟您的終端機 (Terminal)：** 開啟您的命令提示字元、終端機或 PowerShell 視窗。
2.  **切換到正確的目錄：** 使用 `cd` 指令進入這個特定的專案資料夾：
    ```sh
    cd path/to/agents/adk1003-team
    ```
    (請將 `path/to/` 替換成您電腦上的實際路徑)。
3.  **建立秘密檔案 (`.env`)：**
    *   在 `adk1003-team` 目錄中，您會看到像 `.env.example` 這樣的範例檔案。
    *   您需要建立一個*真實*的秘密檔案，名稱就是 `.env`（只有 `.env`，前面有一個點，沒有其他名稱）。
    *   將 `.env.example` 的內容複製到您新建立的 `.env` 檔案中。
    *   **重要：** 編輯 `.env` 檔案，將 `"your-api-key-here"` 替換成您在「事前準備」步驟中取得的實際 Google API 金鑰。
    *   確保檔案內容如下所示（如果您使用的是 AI Studio 金鑰）：
        ```
        GOOGLE_GENAI_USE_VERTEXAI="False"
        GOOGLE_API_KEY="your-actual-api-key-goes-here"
        ```
        *(如果您使用的是 Vertex AI 金鑰和設定，您需要將 `False` 改為 `True` 並設定 Vertex 相關選項，但對於新手，建議使用 `False` 和 AI Studio 金鑰)。*
4.  **安裝所需軟體：** 在您的終端機中執行此指令。`uv sync` 會讀取專案的需求清單，並自動下載安裝必要的 Python 套件。
    ```sh
    uv sync
    ```

## 執行代理人！ (Running the Agents!)

現在來看看有趣的部分！

1.  **啟動 ADK 網路伺服器：** 在終端機中執行以下指令（請確保您仍在 `agents/adk1003-team` 目錄中）：
    ```sh
    uv run adk web
    ```
2.  **在瀏覽器中查看：** 這個指令會在您的電腦上啟動一個本地網路伺服器。您的終端機很可能會顯示一個網址，例如 `http://127.0.0.1:8000`（端口號可能會不同）。
3.  **開始互動：** 打開您的網路瀏覽器（如 Chrome、Firefox 等），然後前往該網址。您應該會看到一個網頁介面，您可以在那裡與範例代理人聊天！

## 它是如何運作的 (給好奇者的開發細節 / Development Details)

如果您想了解這些代理人是如何建構的：

*   **代理人的大腦 (`agent.py`)：** 每個代理人的主要邏輯和行為程式碼都在 `agent.py` 檔案中。
*   **代理人的指示 (`.md` 檔案)：** 每個代理人的具體指示、個性和目標來自一個 Markdown 檔案（以 `.md` 結尾的檔案，例如 `agent_root.md`, `agent_greeting.md` 等）。
*   **代理人的工具 (Python 函數)：** 有時代理人需要特殊的工具來做事，例如查找資訊。這些工具被定義為簡單的 Python 函數（例如提到的 `get_taichung_pubarts_list` 範例），並提供給需要它們的代理人使用。
*   **讓代理人被找到 (`__init__.py`)：** 這個特殊的 Python 檔案幫助 ADK 系統在伺服器啟動時找到並載入您的代理人程式碼。

## 授權 (License)

本專案程式碼依據 Apache License 2.0 授權分享。您可以在 [LICENSE](/LICENSE) 檔案中閱讀完整的詳細資訊。