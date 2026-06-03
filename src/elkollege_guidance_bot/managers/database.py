import pyquoks.managers.database

from .. import models


class DatabaseManager(pyquoks.managers.database.DatabaseManager):
    users: UsersDatabase


class UsersDatabase(pyquoks.managers.database.Database):
    _NAME = "users"

    _SQL = pyquoks.utils.format_multiline_string(
        """
        CREATE TABLE IF NOT EXISTS {0} (
        id INTEGER PRIMARY KEY NOT NULL,
        type INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        phone_number TEXT,
        email TEXT,
        institution TEXT NOT NULL,
        current_course TEXT,
        recommended_course TEXT NOT NULL,
        timestamp INT NOT NULL
        )
        """,
        _NAME,
    )

    def add_user(
            self,
            _type: models.UserType,
            full_name: str,
            phone_number: str | None,
            email: str | None,
            institution: str,
            current_course: str | None,
            recommended_course: str,
            timestamp: int,
    ) -> None:
        cursor = self.cursor()

        cursor.execute(
            pyquoks.utils.format_multiline_string(
                """
                INSERT OR IGNORE INTO {0} (
                type,
                full_name,
                phone_number,
                email,
                institution,
                current_course,
                recommended_course,
                timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._NAME,
            ),
            (
                _type,
                full_name,
                phone_number,
                email,
                institution,
                current_course,
                recommended_course,
                timestamp,
            ),
        )

        self.commit()

    def get_users_list(self) -> list[models.DatabaseUser]:
        cursor = self.cursor()

        cursor.execute(
            pyquoks.utils.format_multiline_string(
                """
                SELECT * FROM {0}
                """,
                self._NAME,
            ),
        )
        results = cursor.fetchall()

        return [models.DatabaseUser.model_validate(dict(result)) for result in results]
