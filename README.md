# AI Blog Idea Brainstormer with Content Outline

A Streamlit-based web application that helps content creators generate creative blog post ideas and detailed content outlines using AI.

## Overview

This application uses OpenAI's GPT models via LangChain to help content creators:

1. Generate creative blog post ideas based on a specific topic/niche
2. Create detailed content outlines for selected ideas
3. Download the outlines for further development

The tool is designed to streamline the brainstorming process and help overcome writer's block by providing AI-powered inspiration and structure.

## Features

- **Idea Generation**: Get 3-5 creative blog post ideas tailored to your topic, audience, and tone
- **Outline Creation**: Generate comprehensive content outlines with title, introduction, main sections, conclusion, and call-to-action
- **User-Friendly Interface**: Clean, intuitive Streamlit interface with feedback indicators
- **Customization Options**: Specify your blog topic, target audience, writing tone, and optional keywords
- **Download Options**: Save your outlines as text or PDF files for later use

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Required Packages

This application requires the following Python packages:

```
streamlit
langchain
openai
python-dotenv
```

### Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd ai-blog-brainstormer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPEN_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Start the application:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Fill in the form with your blog details:
   - **Blog Topic/Niche**: The general subject area (e.g., travel, technology, cooking)
   - **Target Audience**: Who you're writing for (e.g., beginners, professionals, parents)
   - **Writing Tone**: The style of writing (e.g., casual, professional, humorous)
   - **Keywords/Goals** (optional): Specific terms or objectives to include

4. Click "Generate Blog Ideas" to create 3-5 custom blog post ideas

5. Select one of the generated ideas to create a detailed outline

6. Download your outline as a text file or PDF for future reference

## Example

**Input:**
- Topic: Travel
- Audience: Budget travelers
- Tone: Casual
- Keywords: Europe, backpacking

**Generated Ideas:**
1. "10 Hacks to Travel Europe on a Shoestring Budget"
2. "The Ultimate Backpacker's Guide to Eastern Europe"
3. "How I Explored 5 European Countries for Under $1000"

**Sample Outline (for idea 1):**
```
TITLE: 10 Hacks to Travel Europe on a Shoestring Budget

INTRODUCTION:
- Wanna see Europe without draining your savings? Here's how!
- The common misconception that European travel must be expensive
- Brief overview of the 10 money-saving strategies covered

SECTION 1: Smart Booking Tricks
- Using fare comparison tools and price alerts
- The best times to book flights to Europe
- Alternative airports and budget airlines to consider

SECTION 2: Sleep on a Budget
- Hostel strategies and how to find the best deals
- Couchsurfing and home exchange opportunities
- Budget-friendly alternatives to traditional accommodations

SECTION 3: Eating and Exploring for Less
- Finding affordable local eateries away from tourist areas
- Free and low-cost attractions in major European cities
- City passes and transportation hacks

CONCLUSION:
- Europe's yours, no fat wallet needed!
- Recap of key money-saving strategies
- Encouragement to start planning a budget-friendly European adventure

CALL TO ACTION:
- Which hack's your fave? Let me know in the comments!
- Share your own budget travel tips for Europe
```

## Customization

You can modify the code to:
- Change the OpenAI model (e.g., switch to gpt-3.5-turbo for cost efficiency)
- Adjust temperature settings for more/less creative outputs
- Modify prompt templates for different types of blog content
- Add additional output formats or UI elements

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly set in the .env file
- **Generation Failures**: If idea generation fails, try adjusting your inputs or check your API usage limits
- **UI Problems**: Make sure you're using a recent version of Streamlit (1.10.0+)

## License

[MIT License](LICENSE)

## Acknowledgments

- This application uses the OpenAI API
- Built with Streamlit and LangChain

## Author 
S. M. Imran Khan