from app import DB_GROUPS_QUEUES, DB_GROUPS_ADMINS, DB_GROUPS_SKIPS

def get_queues_names(group_id: int) -> list:
    res = DB_GROUPS_QUEUES.find_one({"_id": group_id})
    if res is None:
        return None
    if len(res["queues"].keys()) == 0:
        return None
    names = res["queues"].keys()
    return names

def get_queue(group_id: int, queue_name: str) -> list:
    res = DB_GROUPS_QUEUES.find_one({"_id": group_id})
    if res["queues"].get(queue_name) is None:
        return None
    queue = res["queues"][queue_name]
    return queue

def update_queue(group_id: int, queue_name: str, user_id: int) -> int | None:
    res = DB_GROUPS_QUEUES.find_one({"_id": group_id})
    if res["queues"].get(queue_name) is None:
        return None
    queue = res["queues"][queue_name]
    if user_id in queue:
        queue.remove(user_id)
    queue.append(user_id)
    res["queues"][queue_name] = queue
    DB_GROUPS_QUEUES.update_one({"_id": group_id}, {"$set": res})

    position = len(queue)
    return position

def create_queue(group_id: int, queue_name: str):
    res = DB_GROUPS_QUEUES.find_one({"_id": group_id})
    if res is None:
        data = {
            "_id": group_id,
            "queues": {
                queue_name: []
            }
        }
        DB_GROUPS_SKIPS.insert_one(data)
        DB_GROUPS_QUEUES.insert_one(data)
        return True
    queues = res["queues"]
    if queue_name in queues.keys():
        return False
    queues[queue_name] = []
    res["queues"] = queues
    DB_GROUPS_QUEUES.update_one({"_id": group_id}, {"$set": res})
    DB_GROUPS_SKIPS.update_one({"_id": group_id}, {"$set": res})
    return True

def get_admins(group_id: int) -> list:
    res = DB_GROUPS_ADMINS.find_one({"_id": group_id})
    if res is None:
        return None
    admins = res["admins"]
    return admins

def drop_queue(group_id: int, queue_name: str):
    res = DB_GROUPS_QUEUES.find_one({"_id": group_id})
    res_skips = DB_GROUPS_SKIPS.find_one({"_id": group_id})
    queues = res["queues"]
    skips = res_skips["queues"]
    if queue_name not in queues.keys():
        return False
    queues.pop(queue_name)
    skips.pop(queue_name)
    res["queues"] = queues
    res_skips["queues"] = skips
    DB_GROUPS_QUEUES.update_one({"_id": group_id}, {"$set": res})
    DB_GROUPS_SKIPS.update_one({"_id": group_id}, {"$set": res_skips})
    return True

def get_skips(group_id: int, queue_name: str) -> list:
    res = DB_GROUPS_SKIPS.find_one({"_id": group_id})
    if res["queues"].get(queue_name) is None:
        return None
    skips = res["queues"][queue_name]
    return skips

def update_skips(group_id: int, queue_name: str, user_id: int):
    res = DB_GROUPS_SKIPS.find_one({"_id": group_id})
    queue = res["queues"][queue_name]
    if user_id in queue:
        queue.remove(user_id)
    queue.append(user_id)
    res["queues"][queue_name] = queue
    DB_GROUPS_SKIPS.update_one({"_id": group_id}, {"$set": res})

def remove_skip(group_id: int, queue_name: str, user_id: int):
    res = DB_GROUPS_SKIPS.find_one({"_id": group_id})
    if res["queues"].get(queue_name) is None:
        return None
    queue = res["queues"][queue_name]
    if user_id in queue:
        queue.remove(user_id)
    res["queues"][queue_name] = queue
    DB_GROUPS_SKIPS.update_one({"_id": group_id}, {"$set": res})
