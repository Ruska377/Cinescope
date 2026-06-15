import time
from config.user_creds import  SuperAdminCreds
from playwright.sync_api import Page, expect
from page_object.page_object_models import CinescopLoginPage
import pytest
import allure

@allure.epic("Cinescop")
@allure.feature("Movie_UI")
@allure.story("Отзывы")
@allure.title("Проверка отзыва на фильм")
@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.regression
def test_review(created_movie_with_cleanup, super_admin, page: Page):
    with allure.step("Создаем тестовый фильм"):
        movie_id = created_movie_with_cleanup["id"]
        login_page = CinescopLoginPage(page)  # Создаем объект страницы Login

    with allure.step("Авторизируемся под СуперАдмином"):
        login_page.open()
        login_page.login(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)  # Осуществяем вход
        login_page.assert_was_redirect_to_home_page()

    with allure.step("Переходим в карточку тестового фильма"):
         page.goto(f"https://dev-cinescope.coconutqa.ru/movies/{movie_id}")

    with allure.step("Пишем и отправляем отзыв"):
        page.get_by_placeholder("Написать отзыв").fill("Привет, тестовый отзыв")
        page.click("button:has-text('Отправить')")


    toast = page.get_by_text("Отзыв успешно создан")
    with allure.step("Проверяем появление тоста с надписью: 'Отзыв успешно создан"):
        expect(toast).to_be_visible()
    with allure.step("Проверяем удаление тоста с надписью: 'Отзыв успешно создан"):
        expect(toast).not_to_be_visible(timeout=5000)

    with allure.step("Проверяем появления отзыва на странице"):
        search_review = 'xpath=/html/body/div[2]/main/div/div/div/div/div[2]/p'
        expect(page.locator(search_review)).to_have_text("Привет, тестовый отзыв")
        time.sleep(10)