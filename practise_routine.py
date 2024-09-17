import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

# Set up Streamlit page
st.set_page_config(page_title="Practice Routine Generation", page_icon="🎵")
st.title("Practice Routine Generator")

# Define top performers and their practice styles
top_performers = {
    "Vocal": {
        "M.S. Subbulakshmi": "Known for her rigorous voice culture exercises, focus on breath control, and meticulous approach to lyrical clarity.",
        "T.M. Krishna": "Emphasizes extensive manodharma (improvisation) practice, exploration of rare ragas, and innovative approach to concert structure.",
        "Semmangudi Srinivasa Iyer": "Renowned for his systematic approach to voice training, emphasis on patantara (lineage-based learning), and focus on classic compositions.",
    },
    "Instrument": {
        "Lalgudi Jayaraman (Violin)": "Known for his emphasis on bowing techniques, extensive practice of gamaka (ornamentations), and innovative approach to playing thukkadas (short pieces).",
        "Karaikkudi R. Mani (Mridangam)": "Focuses on developing complex rhythmic patterns, extensive practice of solkattu (vocal percussion), and maintaining perfect timing and control.",
        "U. Srinivas (Mandolin)": "Adapted Carnatic music to the mandolin, emphasizing speed and dexterity exercises, and innovative approach to gamakas on a non-traditional instrument.",
    },
}

# User inputs
practice_type = st.selectbox("What do you want to practice?", ["Vocal", "Instrument"])
instrument = (
    st.text_input("If instrument, which one?", "")
    if practice_type == "Instrument"
    else ""
)

proficiency_level = st.select_slider(
    "Proficiency Level", ["Beginner", "Amateur", "Intermediate", "Advanced"]
)
practice_time = st.number_input(
    "Practice Time (minutes)", min_value=15, max_value=180, value=60, step=10
)
focus_area = st.multiselect(
    "Focus Areas",
    [
        "Rhythm (Tala)",
        "Composition",
        "Raga alapana",
        "Swarakalpana",
        "Ragam Tanam Pallavi(RTP)",
        "General",
    ],
)

# Generate routine button
if st.button("Generate Routine"):
    if not focus_area:
        st.error("Please select at least one focus area.")
    else:
        # Set up LangChain
        llm = OpenAI(temperature=0.5, max_tokens=300)

        # Randomly select performers and their styles
        vocal_performers = "\n".join(
            [f"- {name}: {style}" for name, style in top_performers["Vocal"].items()]
        )
        instrumental_performers = "\n".join(
            [
                f"- {name}: {style}"
                for name, style in top_performers["Instrument"].items()
            ]
        )

        # Create a prompt template
        template = """
        Create a crisp script within 290 words Carnatic music practice routine based on the following information:
        - Practice Type: {practice_type}
        - Instrument (if applicable): {instrument}
        - Proficiency Level: {proficiency_level}
        - Available Practice Time: {practice_time} minutes
        - Focus Areas: {focus_areas}

        Consider the practice styles of these top performers:

        If chosen Vocal performers:
        {vocal_performers}

        If chosen Instrumental performers:
        {instrumental_performers}

        The routine should include:
        1. A warm-up session inspired by appropriate techniques for {practice_type}. If chosen vocal, make sure you include breathing exercises, help explanding the vocal cords. 
        2. Main practice activities tailored to the practice type, proficiency level, and incorporating elements from top performers' styles without giving unncecssary details about the performers and their styles. 
        3. Focused practice sessions for each selected focus area, drawing inspiration from relevant top performers
        4. A cool-down session
        5. Specific exercises or techniques for each part of the routine, reflecting best practices in Carnatic music

        Please provide a step-by-step routine with time allocations for each activity, ensuring it fits within the total practice time of {practice_time} minutes. 
        Tone: Avoid using too many words of jargon and consider word limit to generate within 100 words. 

        """

        prompt = PromptTemplate(
            input_variables=[
                "practice_type",
                "instrument",
                "proficiency_level",
                "practice_time",
                "focus_areas",
                "vocal_performers",
                "instrumental_performers",
            ],
            template=template,
        )

        # Create the LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)

        # Generate the routine
        routine = chain.run(
            {
                "practice_type": practice_type,
                "instrument": instrument,
                "proficiency_level": proficiency_level,
                "practice_time": practice_time,
                "focus_areas": ", ".join(focus_area),
                "vocal_performers": vocal_performers,
                "instrumental_performers": instrumental_performers,
            }
        )

        # Display the generated routine
        st.subheader("Your Personalized Carnatic Music Practice Routine:")
        st.write(routine)


st.sidebar.info(
    "This app is created using Streamlit and LangChain, powered by OpenAI's language model. "
    "It generates personalized Carnatic music practice routines based on user inputs and inspired by top performers' practice styles."
)
