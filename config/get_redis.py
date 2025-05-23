from redis import asyncio as aioredis
from redis.exceptions import AuthenticationError, TimeoutError, RedisError
from config.env import RedisConfig
from utils.log_util import logger

# note: Redis初始化工具类
class RedisUtil:
    """
    Redis相关方法
    """

    @classmethod
    async def create_redis_pool(cls) -> aioredis.Redis:
        """
        应用启动时初始化redis连接

        :return: Redis连接对象
        """
        logger.info('开始连接redis...')
        redis = await aioredis.from_url(
            url=f'redis://{RedisConfig.redis_host}',
            port=RedisConfig.redis_port,
            username=RedisConfig.redis_username,
            password=RedisConfig.redis_password,
            db=RedisConfig.redis_database,
            encoding='utf-8',
            decode_responses=True,
        )
        try:
            connection = await redis.ping()
            if connection:
                logger.info('redis连接成功')
            else:
                logger.error('redis连接失败')
        except AuthenticationError as e:
            logger.error(f'redis用户名或密码错误，详细错误信息：{e}')
        except TimeoutError as e:
            logger.error(f'redis连接超时，详细错误信息：{e}')
        except RedisError as e:
            logger.error(f'redis连接错误，详细错误信息：{e}')
        return redis

    @classmethod
    async def close_redis_pool(cls, app):
        """
        应用关闭时关闭redis连接

        :param app: fastapi对象
        :return:
        """
        await app.state.redis.aclose()
        logger.info('关闭redis连接成功')