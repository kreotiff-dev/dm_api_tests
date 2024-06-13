from datetime import datetime
from restclient.configuration import Configuration as MailhogConfiguration, Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from helpers.account_helper import AccountHelper
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)


def test_put_v1_account_token():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    now_date = datetime.now()
    login = f"s-test-{now_date.strftime('%Y%m%d%H%M%S%f')}"
    password = '12345678'
    email = f'{login}@m.ru'

    account_helper.register_new_user(login=login, password=password, email=email)
