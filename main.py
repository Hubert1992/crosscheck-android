import json
from random import choice
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

# 1) Wczytanie bazy pytań
with open('questions.json', 'r', encoding='utf-8') as f:
    QUESTIONS = json.load(f)

class CategoryScreen(Screen):
    pass

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.questions = []
        self.current_question = None
        self.attempts_remaining = 0

    def start_quiz(self, category):
        self.attempts_remaining = 2
        self.questions = QUESTIONS.get(category, []).copy()
        self.ids.score_label.text = f'Wynik: {self.score}'
        self.next_question()

    def next_question(self):
        if not self.questions:
            App.get_running_app().stop()
            return
        self.current_question = choice(self.questions)
        self.ids.question.text = self.current_question['question']
        self.ids.answer.text = ''

    def show_answer(self):
        if self.current_question:
            self.ids.answer.text = self.current_question['answer']

    def on_answer(self, correct):
        if correct:
            self.score += 1
            self.ids.score_label.text = f'Wynik: {self.score}'
            App.get_running_app().stop()
        else:
            self.attempts_remaining -= 1
            # usuwamy bieżące pytanie, by nie powróciło
            if self.current_question in self.questions:
                self.questions.remove(self.current_question)
            if self.attempts_remaining > 0 and self.questions:
                self.next_question()
            else:
                self._show_late_popup()

    def _show_late_popup(self):
        popup = Popup(
            title='Notice',
            content=Label(text='Later or tomorrow'),
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=True
        )
        popup.bind(on_dismiss=lambda *a: App.get_running_app().stop())
        popup.open()

class CrossCheckApp(App):
    title = 'Cross check'
    def build(self):
        sm = Builder.load_file('quiz.kv')
        # wypełniamy spinner od razu kategoriami
        spinner = sm.get_screen('categories').ids.category_spinner
        spinner.values = list(QUESTIONS.keys())
        spinner.text = 'Wybierz kategorię'
        return sm

if __name__ == '__main__':
    CrossCheckApp().run()
