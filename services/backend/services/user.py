
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.backend.api import tariff
from shared.database import TariffRepository, Unset, UserRepository

from ..depends import get_session, get_user, get_user_repo
from ..exceptions import (
    AdminRightsEditNotAllowedException,
    MemberRightsEditNotAllowedException,
    MemberSettingsEditNotAllowedException,
    TariffNotFoundException,
    UserNotFoundException
)
from ..schemas import EditUserSchema, UserSchema


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        ur: UserRepository,
        user_schema: UserSchema
    ) -> None:
        self.session = session
        self.ur = ur
        self.user_schema = user_schema

    @classmethod
    def depends(
        cls,
        session: AsyncSession = Depends(get_session),
        ur: UserRepository = Depends(get_user_repo),
        user_schema: UserSchema = Depends(get_user)
    ) -> 'UserService':
        return cls(session, ur, user_schema)

    async def all(
        self,
        limit: int | None,
        offset: int | None
    ) -> list[UserSchema]:
        return [UserSchema.from_db(u)
                for u in await self.ur.get_all(limit, offset)]

    async def count(self) -> int:
        return await self.ur.count()

    async def get(self, user_id: UUID) -> UserSchema:
        user = await self.ur.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException()
        return UserSchema.from_db(user)

    async def edit(
        self,
        user_id: UUID,
        edited_user: EditUserSchema
    ) -> None:  # TODO: analyze: mb need to fix
        user = await self.ur.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException()
        if not isinstance(edited_user.rights, Unset):
            if self.user_schema.rights.is_user_editor is False:
                raise AdminRightsEditNotAllowedException()
            if not isinstance(edited_user.rights.is_admin_rights_editor, Unset) or self.user_schema.rights.is_admin_rights_editor is False:
                raise AdminRightsEditNotAllowedException()
            if edited_user.rights.is_member_rights_editor is True or self.user_schema.rights.is_member_rights_editor is False:
                raise AdminRightsEditNotAllowedException()
            await self.ur.update_rights(user, edited_user.rights.model_dump())

        if not isinstance(edited_user.settings, Unset):
            if len(edited_user.settings.model_dump()) > 0 and self.user_schema.rights.is_user_editor is False:
                raise MemberSettingsEditNotAllowedException()
            await self.ur.update_settings(user, edited_user.settings.model_dump())

        if not isinstance(edited_user.telegram_id, Unset):
            if self.user_schema.rights.is_user_editor is False:
                raise MemberRightsEditNotAllowedException()
            await self.ur.update_telegram_id(user, edited_user.telegram_id)
        if not isinstance(edited_user.description, Unset):
            if self.user_schema.rights.is_user_editor is False:
                raise MemberRightsEditNotAllowedException()
            await self.ur.update_description(user, edited_user.description)
        if not isinstance(edited_user.tariff_id, Unset):
            if self.user_schema.rights.is_user_editor is False:
                raise MemberRightsEditNotAllowedException()
            tr = TariffRepository(self.session)
            if edited_user.tariff_id is not None:
                tariff = await tr.get_by_id(edited_user.tariff_id)
                if tariff is None:
                    raise TariffNotFoundException()
            else:
                tariff = None
            await self.ur.update_tariff(user, tariff)

    async def get_self_info(self) -> UserSchema:
        return self.user_schema
