import streamlit as st
from modules.voice_control import VoiceControl
from modules.gesture_control import GestureControl
from modules.recipe_manager import RecipeManager
from modules.timer_manager import TimerManager
import time


def main():
    st.set_page_config(page_title="Smart Kitchen Assistant", layout="wide")

    # Initialize modules
    recipe_manager = RecipeManager()
    timer_manager = TimerManager()
    voice_control = VoiceControl(recipe_manager, timer_manager)
    gesture_control = GestureControl(recipe_manager, timer_manager)

    # UI Layout
    st.title("🍳 Smart Kitchen Assistant")

    col1, col2 = st.columns([3, 1])

    with col1:
        # Recipe display
        current_recipe = recipe_manager.get_current_recipe()
        st.header(f"🧑‍🍳 {current_recipe['name']}")

        st.subheader("📝 Ingredients")
        for ingredient in current_recipe["ingredients"]:
            st.markdown(f"- {ingredient}")

        st.subheader("👨‍🍳 Instructions")
        current_step = recipe_manager.get_current_step()
        st.markdown(f"**Step {recipe_manager.current_step_index + 1}:** {current_step}")

    with col2:
        # Controls
        st.header("🎛️ Controls")
        if st.button("Next Step"):
            recipe_manager.next_step()

        if st.button("Previous Step"):
            recipe_manager.previous_step()

        # Timers
        st.header("⏱️ Active Timers")
        for timer in timer_manager.get_active_timers():
            st.warning(f"⏰ {timer['message']} - {timer['remaining']}")

        # Voice status
        st.header("🎤 Voice Control")
        if st.button("Start Listening"):
            command = voice_control.listen()
            if command:
                st.success(f"Heard: {command}")
                voice_control.process_command(command)

    # Gesture detection (runs in background)
    gesture = gesture_control.detect()
    if gesture:
        gesture_control.process_gesture(gesture)
        st.toast(f"Gesture detected: {gesture}")


if __name__ == "__main__":
    main()
