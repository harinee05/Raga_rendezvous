import streamlit as st
import ragarend
import contact


# Define the navigation bar
def navbar():
    st.sidebar.title("RAGA RENDEZVOUS")
    tab_selection = st.sidebar.selectbox(
        "", ["Home", "Learn", "Your Custom Routine", "Quiz App", "Contact Me"]
    )
    return tab_selection


# Integrate the navigation bar
page = navbar()

# Define the content for each page
if page == "Home":
    st.title("Welcome to Raga Rendezvous!")
    st.write(
        """Welcome to Raga Rendezvous! As a passionate computer science graduate and a devoted Carnatic music enthusiast, I’m on an exciting mission to merge the worlds of technology and traditional music. Raga Rendezvous is an innovative tool designed specifically for those who share a love for Carnatic music, offering an interactive and personalized learning experience through a chatbot tailored to your musical journey."""
    )
    st.title("What is Raga Rendezvous?")
    st.write(
        """
Raga Rendezvous is a unique application that brings the timeless art of Carnatic music into the digital age. This tool is designed to guide learners, enthusiasts, and professionals alike through the intricate world of ragas, talas, and compositions. Whether you're looking to learn, practice, or test your knowledge, Raga Rendezvous offers a seamless experience that adapts to your individual needs."""
    )
    st.title("The Motivation Behind Raga Rendezvous")
    st.write(
        """

As a lifelong learner of Carnatic music, I’ve always felt a deep connection to its rich traditions and profound complexities. However, I also recognize the challenges that come with mastering this ancient art form. With the rise of technology, I saw an opportunity to create something that not only honors the traditions of Carnatic music but also makes learning it more accessible and engaging for everyone.

My vision is to craft a chatbot experience that resonates with the specific needs of Carnatic music lovers. By meticulously gathering user requirements and understanding the motivations behind each learner’s journey, Raga Rendezvous is designed to harmonize the worlds of technology and music. The goal is to create a tool that not only educates but also inspires, supporting the musical growth of each user."""
    )
    st.title("Why Raga Rendezvous?")

    st.write(
        """In today’s fast-paced world, it’s essential to have tools that can adapt to our learning styles and needs. Raga Rendezvous does just that. It’s more than just a learning platform; it’s a companion on your musical journey. By engaging with users, understanding their unique requirements, and incorporating advanced AI technology, Raga Rendezvous aims to be a go-to resource for anyone passionate about Carnatic music.

Join me on this journey to explore, learn, and grow within the beautiful world of Carnatic music. Let’s bridge the gap between tradition and innovation, and create something truly special together. 🎵🤖🎶
"""
    )

elif page == "Learn":
    ragarend.main()

elif page == "Your Custom Routine":
    st.title("Practice Carnatic Music")
    # Here, you can call the content from practice_routine.py
    # For simplicity, let's use a placeholder
    st.write("This is the Practice page where you'll follow practice routines.")

elif page == "Quiz App":
    st.title("Test Your Knowledge with the Quiz App")
    # Here, you can call the content from quiz_app.py
    # For simplicity, let's use a placeholder
    st.write(
        "This is the Quiz App page where you'll test your knowledge of Carnatic music."
    )

elif page == "Contact Me":
    st.title("Contact Me")
    # Here, you can call the content from contact.py
    # For simplicity, let's use a placeholder
    contact.main()
