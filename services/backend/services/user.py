
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import UserRepository

from ..exceptions import (
    AdminRightsEditNotAllowedException,
    MemberRightsEditNotAllowedException,
    MemberSettingsEditNotAllowedException,
    UserNotFoundException
)
from ..schemas import EditUserSchema, UserSchema
from .depends import (
    get_session,
    get_user,
    get_user_repo,
)


class UserService:
    def __init__(self,
                 session: AsyncSession,
                 ur: UserRepository,
                 user_schema: UserSchema
                 ) -> None:
        self.session = session
        self.ur = ur
        self.user_schema = user_schema

    @classmethod
    def depends(cls,
                session: AsyncSession = Depends(get_session),
                ur: UserRepository = Depends(get_user_repo),
                user_schema: UserSchema = Depends(get_user)
                ) -> 'UserService':
        return cls(session, ur, user_schema)

    async def all(self) -> list[UserSchema]:
        return [UserSchema.from_db(u)
                for u in await self.ur.get_all()]

    async def edit(self,
                   user_id: UUID,
                   edited_user: EditUserSchema
                   ) -> None:  # TODO: analyze: mb need to fix
        user = await self.ur.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException()
        if edited_user.rights is not None:
            if self.user_schema.rights.is_user_editor is False:
                raise AdminRightsEditNotAllowedException()
            if edited_user.rights.is_admin_rights_editor is not None or self.user_schema.rights.is_admin_rights_editor is False:
                raise AdminRightsEditNotAllowedException()
            if edited_user.rights.is_member_rights_editor is True or self.user_schema.rights.is_member_rights_editor is False:
                raise AdminRightsEditNotAllowedException()
            await self.ur.update_rights(user, edited_user.rights.model_dump())

        if edited_user.settings is not None:
            if len(edited_user.settings.model_dump()) > 0 and self.user_schema.rights.is_user_editor is False:
                raise MemberSettingsEditNotAllowedException()
            await self.ur.update_settings(user, edited_user.settings.model_dump())

        if edited_user.telegram_id is not None:
            if self.user_schema.rights.is_user_editor is False:
                raise MemberRightsEditNotAllowedException()
            await self.ur.update_telegram_id(user, edited_user.telegram_id)

    async def get_self_info(self) -> UserSchema:
        return self.user_schema
