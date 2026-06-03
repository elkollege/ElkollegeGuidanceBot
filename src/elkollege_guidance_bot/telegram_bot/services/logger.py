import aiogram
import pyquoks.services.logger


class LoggerService(pyquoks.services.logger.LoggerService):
    def log_telegram_user_interaction(self, user: aiogram.types.User, interaction: str) -> None:
        if user.username is None:
            user_info = f"{user.full_name}"
        else:
            user_info = f"{user.full_name} | @{user.username}"

        self.info(f"{user_info} ({user.id}) - \"{interaction}\"")
