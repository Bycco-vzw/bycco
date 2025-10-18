from reddevil.core import DbBase, get_mongodb
from pymongo import ReturnDocument


class DbCounter(DbBase):
    COLLECTION = "counter"
    DOCUMENTTYPE = "Counter"
    VERSION = 1

    @classmethod
    async def next(cls, counter: str) -> int:
        """
        give the next value of a counter,
        returns 1 if the counter not yet exists
        """
        db = get_mongodb()
        doc = await db.counter.find_one_and_update(
            {"_id": counter},
            {"$inc": {"value": 1}},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )
        return doc["value"]