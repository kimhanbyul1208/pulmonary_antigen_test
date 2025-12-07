"""
성능 최적화를 위한 데코레이터
"""

from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
import time
import logging
import hashlib
import json

logger = logging.getLogger(__name__)


def cached_view(timeout=300, key_prefix='view'):
    """
    뷰 결과를 캐싱하는 데코레이터

    Usage:
        @cached_view(timeout=600, key_prefix='patient_list')
        @api_view(['GET'])
        def get_patient_list(request):
            ...

    Args:
        timeout: 캐시 유효 시간 (초)
        key_prefix: 캐시 키 접두사
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # 캐시 키 생성 (경로 + 쿼리 파라미터 + 사용자)
            query_params = request.GET.urlencode()
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'

            cache_key = f'{key_prefix}:{request.path}:{query_params}:{user_id}'

            # 캐시 확인
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.info(f"Cache hit: {cache_key}")
                return cached_response

            # 캐시 미스 - 실제 뷰 실행
            logger.info(f"Cache miss: {cache_key}")
            response = func(request, *args, **kwargs)

            # 성공 응답만 캐싱
            if hasattr(response, 'status_code') and 200 <= response.status_code < 300:
                cache.set(cache_key, response, timeout)

            return response

        return wrapper
    return decorator


def cached_queryset(timeout=300, key_func=None):
    """
    쿼리셋 결과를 캐싱하는 데코레이터

    Usage:
        @cached_queryset(timeout=3600)
        def get_active_medications():
            return Medication.objects.filter(is_active=True)

    Args:
        timeout: 캐시 유효 시간 (초)
        key_func: 캐시 키 생성 함수 (기본: 함수명 + 인자)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 캐시 키 생성
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # 기본 캐시 키: 함수명 + 인자
                args_str = str(args) + str(sorted(kwargs.items()))
                args_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
                cache_key = f'queryset:{func.__name__}:{args_hash}'

            # 캐시 확인
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Queryset cache hit: {cache_key}")
                return cached_result

            # 캐시 미스 - 실제 쿼리 실행
            logger.debug(f"Queryset cache miss: {cache_key}")
            result = func(*args, **kwargs)

            # 쿼리셋을 리스트로 변환하여 캐싱
            if hasattr(result, '__iter__'):
                result = list(result)

            cache.set(cache_key, result, timeout)

            return result

        return wrapper
    return decorator


def invalidate_cache(*cache_keys):
    """
    캐시 무효화 데코레이터

    Usage:
        @invalidate_cache('active_medications', 'medication_list')
        def update_medication(medication_id, data):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # 캐시 삭제
            for key in cache_keys:
                cache.delete(key)
                logger.info(f"Invalidated cache: {key}")

            return result

        return wrapper
    return decorator


def query_debugger(func):
    """
    쿼리 수와 실행 시간을 로깅하는 데코레이터 (개발용)

    Usage:
        @query_debugger
        def get_patient_list(request):
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        from django.conf import settings
        from django.db import connection, reset_queries

        if not settings.DEBUG:
            return func(*args, **kwargs)

        # 쿼리 리셋
        reset_queries()

        # 실행 시간 측정
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # 쿼리 분석
        total_queries = len(connection.queries)
        total_time = sum(float(q['time']) for q in connection.queries)

        # 로깅
        logger.info(
            f"\n{'='*60}\n"
            f"Function: {func.__name__}\n"
            f"Total time: {(end_time - start_time)*1000:.2f}ms\n"
            f"Database queries: {total_queries}\n"
            f"Database time: {total_time*1000:.2f}ms\n"
            f"{'='*60}"
        )

        # 느린 쿼리 경고
        for query in connection.queries:
            query_time = float(query['time'])
            if query_time > 0.1:  # 100ms 이상
                logger.warning(
                    f"Slow query ({query_time*1000:.2f}ms):\n{query['sql'][:200]}"
                )

        return result

    return wrapper


def rate_limit(requests_per_minute=60):
    """
    Rate limiting 데코레이터

    Usage:
        @rate_limit(requests_per_minute=10)
        @api_view(['POST'])
        def expensive_operation(request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # 사용자 식별
            if request.user.is_authenticated:
                user_key = f'user:{request.user.id}'
            else:
                user_key = f'ip:{request.META.get("REMOTE_ADDR")}'

            cache_key = f'rate_limit:{func.__name__}:{user_key}'

            # 현재 요청 수 확인
            current_requests = cache.get(cache_key, [])
            now = time.time()

            # 1분 이내 요청만 유지
            current_requests = [req_time for req_time in current_requests if now - req_time < 60]

            # Rate limit 체크
            if len(current_requests) >= requests_per_minute:
                logger.warning(f"Rate limit exceeded for {user_key} on {func.__name__}")
                return JsonResponse({
                    'error': 'Too many requests',
                    'detail': f'Maximum {requests_per_minute} requests per minute',
                    'retry_after': 60 - (now - current_requests[0])
                }, status=429)

            # 요청 기록
            current_requests.append(now)
            cache.set(cache_key, current_requests, 60)

            return func(request, *args, **kwargs)

        return wrapper
    return decorator


def measure_performance(func):
    """
    함수 실행 시간을 측정하고 로깅하는 데코레이터

    Usage:
        @measure_performance
        def complex_calculation():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        duration = time.time() - start_time

        # 느린 함수 경고 (1초 이상)
        if duration > 1.0:
            logger.warning(
                f"Slow function: {func.__name__} took {duration:.2f}s"
            )
        else:
            logger.debug(
                f"Function: {func.__name__} took {duration*1000:.2f}ms"
            )

        return result

    return wrapper


def cache_per_user(timeout=300, key_prefix='user_data'):
    """
    사용자별로 캐시하는 데코레이터

    Usage:
        @cache_per_user(timeout=600, key_prefix='dashboard')
        def get_user_dashboard(request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return func(request, *args, **kwargs)

            # 사용자별 캐시 키
            cache_key = f'{key_prefix}:{request.user.id}'

            # 캐시 확인
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.info(f"User cache hit: {cache_key}")
                return cached_response

            # 캐시 미스
            logger.info(f"User cache miss: {cache_key}")
            response = func(request, *args, **kwargs)

            # 캐싱
            if hasattr(response, 'status_code') and 200 <= response.status_code < 300:
                cache.set(cache_key, response, timeout)

            return response

        return wrapper
    return decorator


def conditional_cache(condition_func, timeout=300):
    """
    조건부 캐싱 데코레이터

    Usage:
        @conditional_cache(
            condition_func=lambda request: not request.user.is_staff,
            timeout=600
        )
        def get_public_data(request):
            # 관리자가 아닌 경우에만 캐싱
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # 조건 체크
            should_cache = condition_func(request)

            if not should_cache:
                return func(request, *args, **kwargs)

            # 캐시 키 생성
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'
            cache_key = f'conditional:{func.__name__}:{request.path}:{user_id}'

            # 캐시 확인
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response

            # 캐시 미스
            response = func(request, *args, **kwargs)

            # 캐싱
            if hasattr(response, 'status_code') and 200 <= response.status_code < 300:
                cache.set(cache_key, response, timeout)

            return response

        return wrapper
    return decorator
