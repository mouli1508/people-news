
# Reddit Data Extraction and Summarization

This project is a **Streamlit application** designed to extract data from Reddit discussions based on user-provided questions and summarize the extracted data using **Google Gemini LLM**. The application includes sentiment analysis to classify the overall tone of the discussions as positive, negative, or neutral.

---

## Features

- **Reddit Data Extraction**:
  - Retrieves Reddit posts and comments using Google Custom Search API and Reddit API (via `praw`).
  - Allows users to query Reddit discussions with a specific question.
  - Extracts key details including titles, post bodies, and top comments.

- **AI-Powered Summarization**:
  - Summarizes the extracted data using the **Google Gemini LLM API**.
  - Provides a concise summary and highlights the overall sentiment of the discussions.

- **Streamlit Interface**:
  - User-friendly interface for inputting questions and visualizing results.
  - Includes spinners and success/error notifications for better user experience.
 
---

## Figma Design

[View the Figma Board](https://embed.figma.com/board/xXcX8K3Eb9jM7Lb41HlXpU/Untitled?node-id=0-1&embed-host=share)


---

## Demo

<img src="static\image.png" alt="Application Screenshot" width="800">
<img src="static\image2.png" alt="Application Screenshot" width="800">

---

## Installation

### Prerequisites

- Python 3.12 or above
- API keys for:
  - **Google Custom Search API** (for Reddit URL scraping)
  - **Google Gemini LLM API** (for summarization)
  - **Reddit API** (for fetching Reddit posts and comments)

### 1. Clone the Repository

```bash
git clone https://github.com/mouli1508/people-news
cd people-news
```

### 2. Create a Conda Environment

```bash
conda create -n "reddit-summary" python=3.12
conda activate reddit-summary
```

### 3. Install Dependencies

Install the required Python packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```env
GOOGLE_API_KEY=your_google_api_key
SEARCH_ENGINE_ID=your_search_engine_id
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_reddit_user_agent
SEARCH_API_KEY=your_google_search_api_key
```

---

## Usage

### 1. Run the Streamlit Application

Start the application by running the following command:

```bash
streamlit run ask_people.py
```

### 2. Enter Your Query

- Provide a **question** to query Reddit discussions.
- The app will:
  1. Extract Reddit posts and comments related to your question.
  2. Generate a concise summary of the discussions.
  3. Analyze the sentiment of the extracted data.

### 3. View Results

- The app displays the extracted data, a detailed summary, and sentiment analysis.
- Example:
  - **Question**: "How will AI change the world?"
  - **Summary**: "Reddit discussions highlight both the transformative potential of AI and concerns about job loss, inequality, and ethical implications. Overall sentiment is mixed but leans slightly positive."

---

## Project Structure

```
.
├── reddit_data_extraction.py  # Library for extracting Reddit data
├── ask_people.py              # Main Streamlit app code
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # Project documentation
```

---

## Key Technologies

- **Streamlit**: For building an interactive UI.
- **Google Gemini LLM**: For summarization and sentiment analysis - gemini 1.5 flash (1M context).
- **Google Custom Search API**: For fetching Reddit links.
- **Reddit API (PRAW)**: For accessing Reddit posts and comments.
- **Python-dotenv**: For managing environment variables.

---

## API Setup

### Google Custom Search API

1. Visit [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Custom Search JSON API**.
3. Obtain the `GOOGLE_API_KEY` and `SEARCH_ENGINE_ID`.

### Reddit API

1. Log in to [Reddit](https://www.reddit.com/).
2. Create a new app under [Reddit Apps](https://www.reddit.com/prefs/apps).
3. Obtain the `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT`.

### Google Gemini LLM API

1. Visit the [Gemini API Documentation](https://cloud.google.com/genai/).
2. Enable the **Generative AI API** and obtain the `SEARCH_API_KEY`.

---

## Troubleshooting

- **Issue**: App crashes with "KeyError".
  - **Solution**: Verify the `.env` file contains correct API keys and is in the project directory.

- **Issue**: "No Reddit URLs found for the given question".
  - **Solution**: Ensure the Google Custom Search API is configured properly and the question is specific.

- **Issue**: "Unable to connect to Reddit".
  - **Solution**: Check Reddit API credentials and ensure they are active.

---

## Future Enhancements

- Add **multilingual support** for querying Reddit posts in different languages.
- Integrate **advanced visualizations** for displaying trends and insights.
- Expand to support summarization from **other data sources** like YouTube or Twitter.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributors

- Chandramouli

---

Feel free to reach out for any questions or feedback! 🚀
