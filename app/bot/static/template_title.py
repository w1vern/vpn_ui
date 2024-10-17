from enum import Enum

from app.bot.commands import toggle_auto_pay_command


class TemplateTitle(str, Enum):
    start_template = "start_template"
    toggle_auto_pay_template = "toggle_auto_pay_template"
    

    
