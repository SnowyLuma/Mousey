# -*- coding: utf-8 -*-

"""
Mousey: Discord Moderation Bot
Copyright (C) 2016 - 2021 Lilly Rose Berner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.routing import Router

from ..auth import is_authorized
from ..config import SHARD_COUNT
from ..permissions import has_permissions


router = Router()


def serialize_rule(data):
    data = dict(data)

    data['updated_at'] = data['updated_at'].isoformat()
    data['inactive_timeout'] = data['inactive_timeout'].total_seconds()

    return data


# TODO: Re-enable configuration
@router.route('/autoprune', methods=['GET'])
@is_authorized
@has_permissions(administrator=True)
async def get_autopurge(request):
    try:
        shard_id = int(request.query_params['shard_id'])
    except (KeyError, ValueError):
        raise HTTPException(400, 'Invalid or missing "shard_id" query param.')

    async with request.app.db.acquire() as conn:
        records = await conn.fetch(
            """
            SELECT
              autoprune.guild_id,
              autoprune.role_ids,
              autoprune.activity_type,
              autoprune.inactive_timeout,
              autoprune.updated_at
            FROM autoprune
            JOIN guilds ON autoprune.guild_id = guilds.id
            WHERE (guild_id >> 22) % $2 = $1 AND guilds.removed_at IS NULL
            """,
            shard_id,
            SHARD_COUNT,
        )

    if records:
        return JSONResponse(list(map(serialize_rule, records)))

    raise HTTPException(404, 'No autoprune rules found.')
