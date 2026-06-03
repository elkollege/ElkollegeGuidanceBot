import aiogram.fsm.state


class Flow(aiogram.fsm.state.StatesGroup):
    personal_data_agreement = aiogram.fsm.state.State()
    input_full_name = aiogram.fsm.state.State()
    input_phone_number = aiogram.fsm.state.State()
    input_email = aiogram.fsm.state.State()
    input_institution = aiogram.fsm.state.State()
    input_current_course = aiogram.fsm.state.State()
    career_guidance_test = aiogram.fsm.state.State()
    recommended_course_displayed = aiogram.fsm.state.State()
