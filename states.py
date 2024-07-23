from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    phone_number = State()
    name = State()


class Booking(StatesGroup):
    event_id = State()
    book_type = State()
    num_seats = State()
