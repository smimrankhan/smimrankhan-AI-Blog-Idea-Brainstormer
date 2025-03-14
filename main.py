import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import re
from datetime import datetime
import base64

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="AI Blog Idea Brainstormer",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    h1, h2, h3 {
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        background-color: #cce5ff;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .download-link {
        display: inline-block;
        padding: 0.5rem 1rem;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin-right: 10px;
        text-align: center;
    }
    .download-link:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("AI Blog Idea Brainstormer ✨")
st.markdown("Generate creative blog post ideas and detailed outlines with AI assistance.")


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'generated_ideas' not in st.session_state:
        st.session_state.generated_ideas = []
    if 'selected_idea' not in st.session_state:
        st.session_state.selected_idea = None
    if 'outline' not in st.session_state:
        st.session_state.outline = ""
    if 'topic' not in st.session_state:
        st.session_state.topic = ""
    if 'audience' not in st.session_state:
        st.session_state.audience = ""
    if 'tone' not in st.session_state:
        st.session_state.tone = ""


def setup_openai_client():
    """
    Set up and return an OpenAI client using the API key from .env
    
    Returns:
        ChatOpenAI: Configured LLM instance
    """
    api_key = os.getenv('OPEN_API_KEY')
    
    if not api_key:
        st.error("OpenAI API key not found. Please check your .env file.")
        st.stop()
        
    return ChatOpenAI(
        model_name="gpt-4",  # Can be switched to gpt-3.5-turbo for cost efficiency
        temperature=0.7,
        openai_api_key=api_key
    )


def generate_blog_ideas(topic, audience, tone, keywords=None):
    """
    Generate blog post ideas using LangChain and OpenAI
    
    Args:
        topic (str): Blog topic or niche
        audience (str): Target audience
        tone (str): Writing tone
        keywords (str, optional): Optional keywords or goals
        
    Returns:
        list: List of generated blog post ideas
    """
    # Show progress indicator
    with st.spinner("Generating creative blog ideas..."):
        # Setup prompt template
        template = """
        You're a creative blogger. Generate 3-5 blog post ideas for the topic {topic}, 
        targeting {audience}, in a {tone} tone. {keywords_text}
        
        Format your response as a numbered list with only the ideas, one per line.
        Each idea should be catchy, specific, and tailored to the audience.
        """
        
        # Add keywords if provided
        keywords_text = f"Include these keywords or goals: {keywords}" if keywords else ""
        
        # Create prompt
        prompt = PromptTemplate(
            input_variables=["topic", "audience", "tone", "keywords_text"],
            template=template
        )
        
        # Setup LLM chain
        llm = setup_openai_client()
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate ideas
        response = chain.run(
            topic=topic,
            audience=audience,
            tone=tone,
            keywords_text=keywords_text
        )
        
        # Process response into a list of ideas
        ideas = []
        for line in response.strip().split('\n'):
            # Extract idea text, removing numbering
            match = re.match(r'^\d+\.?\s*(.+)$', line.strip())
            if match and match.group(1):
                ideas.append(match.group(1))
        
        return ideas


def generate_blog_outline(idea, topic, audience, tone):
    """
    Generate a detailed blog outline for the selected idea
    
    Args:
        idea (str): Selected blog post idea
        topic (str): Blog topic or niche
        audience (str): Target audience
        tone (str): Writing tone
        
    Returns:
        str: Formatted blog outline text
    """
    # Show progress indicator
    with st.spinner("Creating detailed outline for your selected idea..."):
        # Setup prompt template
        template = """
        You're a content strategist. Create a detailed blog outline for {selected_idea}.
        Include a title, intro, 2-3 main sections with subheadings, conclusion, and CTA.
        Use a {tone} tone for {audience} interested in {topic}.
        
        Format your response with these sections:
        
        TITLE: (A catchy, SEO-friendly title)
        
        INTRODUCTION:
        - (Hook to grab attention)
        - (Context about the topic)
        - (What readers will learn)
        
        SECTION 1: (Main section heading)
        - (Subpoint 1)
        - (Subpoint 2)
        - (Subpoint 3)
        
        SECTION 2: (Main section heading)
        - (Subpoint 1)
        - (Subpoint 2)
        - (Subpoint 3)
        
        SECTION 3: (Main section heading - optional)
        - (Subpoint 1)
        - (Subpoint 2)
        - (Subpoint 3)
        
        CONCLUSION:
        - (Summary of key points)
        - (Final thoughts)
        
        CALL TO ACTION:
        - (Specific action for reader to take)
        """
        
        # Create prompt
        prompt = PromptTemplate(
            input_variables=["selected_idea", "topic", "audience", "tone"],
            template=template
        )
        
        # Setup LLM chain with slightly lower temperature for more structured output
        llm = setup_openai_client()
        llm.temperature = 0.5
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate outline
        response = chain.run(
            selected_idea=idea,
            topic=topic,
            audience=audience,
            tone=tone
        )
        
        return response


def get_download_link(content, filename, link_text):
    """
    Create a download link for content
    
    Args:
        content (str): Text content to download
        filename (str): Name of the download file
        link_text (str): Text to display on the download link
        
    Returns:
        str: HTML for the download link
    """
    # Encode content as base64
    b64 = base64.b64encode(content.encode()).decode()
    
    # Create download link HTML
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-link">{link_text}</a>'
    
    return href


def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Input form
    with st.form("blog_input_form"):
        st.subheader("What would you like to blog about?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Blog Topic/Niche", 
                                  placeholder="e.g., travel, tech, fitness, cooking")
            audience = st.text_input("Target Audience", 
                                     placeholder="e.g., beginners, professionals, parents")
        
        with col2:
            tone_options = ["Casual", "Professional", "Humorous", "Informative", "Inspirational"]
            tone = st.selectbox("Writing Tone", tone_options)
            keywords = st.text_input("Keywords or Goals (Optional)", 
                                    placeholder="e.g., SEO, engagement, conversion")
        
        generate_button = st.form_submit_button("Generate Blog Ideas")
    
    # Process form submission
    if generate_button:
        if not topic or not audience:
            st.error("Please provide both a topic and target audience.")
        else:
            # Save inputs to session state for later use
            st.session_state.topic = topic
            st.session_state.audience = audience 
            st.session_state.tone = tone
            
            # Generate ideas
            ideas = generate_blog_ideas(topic, audience, tone.lower(), keywords)
            
            if ideas and len(ideas) >= 3:
                st.session_state.generated_ideas = ideas
                st.session_state.selected_idea = None
                st.session_state.outline = ""
            else:
                st.error("Failed to generate enough ideas. Please try again with different inputs.")
    
    # Display generated ideas
    if st.session_state.generated_ideas:
        st.markdown("""
        <div class="success-box">
            <h3>📝 Blog Ideas Generated!</h3>
            <p>Select one idea below to create a detailed outline.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display ideas with selection buttons
        for i, idea in enumerate(st.session_state.generated_ideas):
            cols = st.columns([5, 1])
            with cols[0]:
                st.write(f"**{i+1}. {idea}**")
            with cols[1]:
                if st.button(f"Select", key=f"btn_{i}"):
                    st.session_state.selected_idea = idea
                    # Generate outline for selected idea
                    st.session_state.outline = generate_blog_outline(
                        idea, 
                        st.session_state.topic, 
                        st.session_state.audience, 
                        st.session_state.tone.lower()
                    )
    
    # Display generated outline
    if st.session_state.outline:
        st.markdown("""
        <div class="info-box">
            <h3>✅ Outline Created!</h3>
            <p>Here's your detailed blog outline. You can download it as a text or PDF file.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the outline
        st.subheader("Your Blog Outline")
        st.text_area("", st.session_state.outline, height=400)
        
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Create download links
        txt_filename = f"blog_outline_{timestamp}.txt"
        pdf_filename = f"blog_outline_{timestamp}.pdf"
        
        txt_download_link = get_download_link(
            st.session_state.outline,
            txt_filename,
            "📄 Download as Text File"
        )
        
        pdf_download_link = get_download_link(
            st.session_state.outline,
            pdf_filename,
            "📑 Download as PDF"
        )
        
        # Display download links
        st.subheader("Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(txt_download_link, unsafe_allow_html=True)
        
        with col2:
            st.markdown(pdf_download_link, unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()

