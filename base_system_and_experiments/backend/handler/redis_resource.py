import json
from datetime import datetime
import asyncio
import aioredis
import random
from collections import defaultdict
import traceback

import logging
logger = logging.getLogger(__name__)

class RedisResource:
    def __init__(self, redis, base_path, id_prefix):
        self.redis = redis
        self.base_path = base_path
        self.id_prefix = id_prefix
        self.key_counter = f"{base_path}/Counter"

    @classmethod
    def create_instance(cls):
        pass

    def id(self, cnt):
        return f"{self.id_prefix}:{cnt:08}"

    def key(self, cnt=None, id=None):
        if cnt:   return f"{self.base_path}/{self.id(cnt)}"
        elif id: return f"{self.base_path}/{id}"

    async def get_counter(self):
        return int(await self.redis.execute_str("GET", self.key_counter))

    async def next_count(self):
        return await self.redis.execute("INCR", self.key_counter)

    async def add(self, data):
        cnt = await self.next_count()
        id = self.id(cnt=cnt)
        data["Timestamp"] = datetime.now().timestamp()
        res = await self.redis.execute("SET", self.key(id=id), json.dumps(data))
        await self._on_add(id, data)
        return id

    async def update(self, id, data):
        await self.redis.execute("SET", self.key(id=id), json.dumps(data))
        await self._on_update(id, data)

    async def get(self, id):
        data = await self.redis.execute("GET", self.key(id=id))
        return json.loads(data) if data else None

    async def _delete(self, id):
        data = await self.get(id)
        await self.redis.execute("DEL", self.key(id=id))
        return data

    async def delete(self, id):
        data = await self._delete(id)
        await self._on_delete(id, data)

    async def delete_multi(self, ids):
        data = [await self._delete(id) for id in ids]
        await self._on_delete_multi(ids, data)
        
    async def all_keys(self):
        data = await self.redis.execute("KEYS", "*")
        return data
    
    async def type_data(self, key):
        data = await self.redis.execute("TYPE", key)
        return data
    
    async def get_set_members(self, key):
        data = await self.redis.execute("SMEMBERS", key)
        return data
    
    async def get_ttl(self, key):
        data = await self.redis.execute("TTL", key)
        return data

    async def _on_add(self, id, data):
        pass

    async def _on_update(self, id, data):
        pass

    async def _on_delete(self, id, data):
        pass

    async def _on_delete_multi(self, ids, data):
        pass


class UserResource(RedisResource):
    def __init__(self, redis):
        super().__init__(redis, "User", "WKR")

    def key_ids_for_pn(self,pn):                   return f"UserIds/PRJ:{pn}"
    def key_ids_assigned_for_nid(self,nid):        return f"UserIdsAssigned/{nid}"
    def key_ids_map_for_platform(self, platform):  return f"UserIdsMap/{platform}"
    def key_prj_ids(self,pn):                      return f"ProjectUserIds/PRJ:{pn}"
    def key_prj_id_counter(self,pn):               return f"ProjectUserIds/PRJ:{pn}/Counter"
    def key_active_ids_for_pn(self,pn):            return f"ActiveUserIds/PRJ:{pn}"
    def key_active_ids_for_ct(self,ct):            return f"ActiveUserIds/ClientToken:{ct}"
    def key_pws_for_id(self,id):                   return f"UserPassword/UserId:{id}"

    def key_data_for_id(self,id):                  return f"Data/UserId:{id}"
    def key_from_id_for_to_id(self,id):            return f"FromId/ToUserId:{id}"


    @classmethod
    def create_instance(cls, platform_wid, platform):
        return {
            "PlatformUserId": platform_wid,
            "Platform": platform
        }

    """async def _on_add(self, id, data):
        platform_wid = data["PlatformUserId"]
        platform = data["Platform"]
        await self.add_id_map_for_platform(platform, platform_wid, id)"""
    async def flushAll(self):
        await self.redis.execute("FLUSHALL")
    async def delete_data_key(self, id):
        await self.redis.execute("DEL", self.key_data_for_id(id))
    async def delete_from_key(self, id):
        await self.redis.execute("DEL", self.key_from_id_for_to_id(id))

    async def add_active_id_for_ct(self, id, ct):
        await self.redis.execute("SADD", self.key_active_ids_for_ct(ct), id)
    async def check_active_id_for_ct(self, id, ct):
        return await self.redis.execute("SISMEMBER", self.key_active_ids_for_ct(ct), id)
    async def delete_active_id_for_ct(self, id, ct):
        return await self.redis.execute("SREM", self.key_active_ids_for_ct(ct), id)
    async def check_existance_active_ct(self, ct):
        return await self.redis.execute("EXISTS", self.key_active_ids_for_ct(ct))
    async def expire_delete_active_ct(self, ct, second):
        return await self.redis.execute("EXPIRE", self.key_active_ids_for_ct(ct), second)
    async def persist_active_ct(self, ct):
        return await self.redis.execute("PERSIST", self.key_active_ids_for_ct(ct))
    async def fetch_all_active_ct(self):
        return await self.redis.execute("KEYS", self.key_active_ids_for_ct("*"))
    async def fetch_active_id_for_ct(self, ct):
        return await self.redis.execute("SMEMBERS", self.key_active_ids_for_ct(ct))

    async def add_password_for_id(self, pw, id):
        await self.redis.execute("SADD", self.key_pws_for_id(id), pw)
    async def check_password_for_id(self, pw, id):
        return await self.redis.execute("SISMEMBER", self.key_pws_for_id(id), pw)
    async def delete_password_for_id(self, pw, id):
        return await self.redis.execute("SREM", self.key_pws_for_id(id), pw)
    async def check_existance_key(self, id):
        return await self.redis.execute("EXISTS", self.key_pws_for_id(id))


    async def add_data_for_id(self, msg, id):
        await self.redis.execute("SADD", self.key_data_for_id(id), msg)
    async def delete_data_for_id(self, msg, id):
        return await self.redis.execute("SREM", self.key_data_for_id(id), msg)
    async def check_existance_data_for_id(self, id):
        return await self.redis.execute("EXISTS", self.key_data_for_id(id))
    async def fetch_data_for_id(self, id):
        return await self.redis.execute("SMEMBERS", self.key_data_for_id(id))
    async def fetch_all_key_data_for_id(self):
        return await self.redis.execute("KEYS", self.key_data_for_id("*"))
    

    async def add_from_id_for_to_id(self, from_id, to_id):
        await self.redis.execute("SADD", self.key_from_id_for_to_id(to_id), from_id)
    async def delete_from_id_for_to_id(self, from_id, to_id):
        return await self.redis.execute("SREM", self.key_from_id_for_to_id(to_id), from_id)
    async def check_existance_from_id_for_to_id(self, to_id):
        return await self.redis.execute("EXISTS", self.key_from_id_for_to_id(to_id))
    async def fetch_from_id_for_to_id(self, to_id):
        return await self.redis.execute("SMEMBERS", self.key_from_id_for_to_id(to_id))
    async def fetch_all_key_from_id_for_to_id(self):
        return await self.redis.execute("KEYS", self.key_from_id_for_to_id("*"))
    



    async def get_ids_for_pn(self, pn):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_for_pn(pn))

    async def add_id_map_for_platform(self, platform, platform_wid, id):
        await self.redis.execute("HSET", self.key_ids_map_for_platform(platform), platform_wid, id)

    async def get_id_for_platform(self, platform, platform_wid):
        return await self.redis.execute_str("HGET", self.key_ids_map_for_platform(platform), platform_wid)

    async def add_id_for_pn(self, pn, id):
        await self.redis.execute("SADD", self.key_ids_for_pn(pn), id)

    async def add_id_assigned_for_nid(self, nid, id):
        return await self.redis.execute("SADD", self.key_ids_assigned_for_nid(nid), id)

    async def delete_id_assigned_for_nid(self, nid, id):
        return await self.redis.execute("SREM", self.key_ids_assigned_for_nid(nid), id)

    async def get_ids_assigned_for_nid(self, nid):
        return await self.redis.execute_str("SMEMBERS", self.key_ids_assigned_for_nid(nid))

    async def add_prj_id(self, pn, id):
        if not (prj_id := await self.get_prj_id(pn, id)):
            next_prj_id = await self.redis.execute("INCR", self.key_prj_id_counter(pn))
            return await self.redis.execute("HSET", self.key_prj_ids(pn), id, next_prj_id)

    async def get_prj_id(self, pn, id):
        try:
            return int(await self.redis.execute_str("HGET", self.key_prj_ids(pn), id))
        except:
            return None
