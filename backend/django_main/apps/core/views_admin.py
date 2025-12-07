"""
관리자 도구 뷰
성능 모니터링, 로그 조회, 시스템 통계
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import APIUsageLog
import logging
import psutil
import os

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def performance_dashboard(request):
    """
    성능 대시보드 데이터

    Returns:
        - API 응답 시간 통계
        - 데이터베이스 쿼리 통계
        - 캐시 히트율
        - 시스템 리소스 사용량
    """

    # 기간 설정 (최근 24시간)
    since = timezone.now() - timedelta(hours=24)

    # === API 사용량 통계 ===
    api_stats = APIUsageLog.objects.filter(
        created_at__gte=since
    ).aggregate(
        total_requests=Count('id'),
        avg_response_time=Avg('response_time_ms'),
        max_response_time=Max('response_time_ms'),
        error_count=Count('id', filter=Q(status_code__gte=400)),
        cache_hits=Count('id', filter=Q(cached=True))
    )

    # 캐시 히트율 계산
    total_requests = api_stats['total_requests'] or 0
    cache_hits = api_stats['cache_hits'] or 0
    cache_hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0

    # 서비스별 사용량
    service_usage = list(
        APIUsageLog.objects.filter(
            created_at__gte=since
        ).values('service').annotate(
            count=Count('id'),
            avg_time=Avg('response_time_ms'),
            errors=Count('id', filter=Q(status_code__gte=400))
        ).order_by('-count')[:10]
    )

    # 시간대별 요청 수 (1시간 단위)
    hourly_requests = []
    for i in range(24):
        hour_start = timezone.now() - timedelta(hours=23-i)
        hour_end = hour_start + timedelta(hours=1)

        count = APIUsageLog.objects.filter(
            created_at__gte=hour_start,
            created_at__lt=hour_end
        ).count()

        hourly_requests.append({
            'hour': hour_start.strftime('%Y-%m-%d %H:00'),
            'count': count
        })

    # === 시스템 리소스 ===
    try:
        # CPU 사용률
        cpu_percent = psutil.cpu_percent(interval=1)

        # 메모리 사용률
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024 ** 3)
        memory_total_gb = memory.total / (1024 ** 3)

        # 디스크 사용률
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 ** 3)
        disk_total_gb = disk.total / (1024 ** 3)

        system_resources = {
            'cpu_percent': round(cpu_percent, 2),
            'memory_percent': round(memory_percent, 2),
            'memory_used_gb': round(memory_used_gb, 2),
            'memory_total_gb': round(memory_total_gb, 2),
            'disk_percent': round(disk_percent, 2),
            'disk_used_gb': round(disk_used_gb, 2),
            'disk_total_gb': round(disk_total_gb, 2)
        }
    except Exception as e:
        logger.error(f"Failed to get system resources: {e}")
        system_resources = {}

    # === Redis 캐시 통계 ===
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("default")
        redis_info = redis_conn.info('stats')

        redis_stats = {
            'total_commands': redis_info.get('total_commands_processed', 0),
            'keyspace_hits': redis_info.get('keyspace_hits', 0),
            'keyspace_misses': redis_info.get('keyspace_misses', 0),
            'hit_rate': cache_hit_rate
        }
    except Exception as e:
        logger.error(f"Failed to get Redis stats: {e}")
        redis_stats = {}

    return Response({
        'api_statistics': {
            'total_requests': total_requests,
            'avg_response_time_ms': round(api_stats['avg_response_time'] or 0, 2),
            'max_response_time_ms': api_stats['max_response_time'] or 0,
            'error_count': api_stats['error_count'],
            'error_rate': round((api_stats['error_count'] / total_requests * 100) if total_requests > 0 else 0, 2),
            'cache_hit_rate': round(cache_hit_rate, 2)
        },
        'service_usage': service_usage,
        'hourly_requests': hourly_requests,
        'system_resources': system_resources,
        'redis_stats': redis_stats,
        'period': {
            'start': since.isoformat(),
            'end': timezone.now().isoformat()
        }
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def slow_queries(request):
    """
    느린 쿼리 목록 조회

    Query params:
        - threshold_ms: 임계값 (밀리초, 기본 100ms)
        - limit: 결과 수 제한 (기본 50)
    """
    threshold_ms = int(request.GET.get('threshold_ms', 100))
    limit = int(request.GET.get('limit', 50))

    # 최근 24시간
    since = timezone.now() - timedelta(hours=24)

    slow_queries = APIUsageLog.objects.filter(
        created_at__gte=since,
        response_time_ms__gte=threshold_ms
    ).order_by('-response_time_ms').values(
        'service',
        'endpoint',
        'response_time_ms',
        'status_code',
        'created_at'
    )[:limit]

    return Response({
        'threshold_ms': threshold_ms,
        'count': len(slow_queries),
        'queries': list(slow_queries)
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def error_logs(request):
    """
    에러 로그 조회

    Query params:
        - hours: 조회 시간 범위 (기본 24시간)
        - service: 서비스 필터
        - limit: 결과 수 제한 (기본 100)
    """
    hours = int(request.GET.get('hours', 24))
    service = request.GET.get('service')
    limit = int(request.GET.get('limit', 100))

    since = timezone.now() - timedelta(hours=hours)

    errors = APIUsageLog.objects.filter(
        created_at__gte=since,
        status_code__gte=400
    )

    if service:
        errors = errors.filter(service=service)

    errors = errors.order_by('-created_at').values(
        'service',
        'endpoint',
        'status_code',
        'error_message',
        'user__username',
        'created_at'
    )[:limit]

    # 에러 통계
    error_stats = APIUsageLog.objects.filter(
        created_at__gte=since,
        status_code__gte=400
    ).values('status_code').annotate(
        count=Count('id')
    ).order_by('-count')

    return Response({
        'period_hours': hours,
        'total_errors': len(errors),
        'errors': list(errors),
        'error_stats': list(error_stats)
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_cache(request):
    """
    캐시 클리어

    Body:
        - pattern: 캐시 키 패턴 (선택, 없으면 전체 클리어)
    """
    pattern = request.data.get('pattern')

    try:
        if pattern:
            # 패턴 매칭 캐시 삭제
            from apps.core.utils.query_optimizer import cache_helper
            cache_helper.invalidate_pattern(pattern)
            message = f"Cleared cache matching '{pattern}'"
        else:
            # 전체 캐시 삭제
            cache.clear()
            message = "Cleared all cache"

        logger.info(f"Cache cleared by admin: {request.user.username}")

        return Response({
            'success': True,
            'message': message
        })

    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def database_stats(request):
    """
    데이터베이스 통계
    """
    from django.db import connection

    stats = {}

    try:
        with connection.cursor() as cursor:
            # 테이블 크기 (MySQL)
            cursor.execute("""
                SELECT
                    table_name,
                    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb,
                    table_rows
                FROM information_schema.TABLES
                WHERE table_schema = DATABASE()
                ORDER BY (data_length + index_length) DESC
                LIMIT 20
            """)

            tables = cursor.fetchall()
            stats['top_tables'] = [
                {
                    'name': row[0],
                    'size_mb': row[1],
                    'rows': row[2]
                }
                for row in tables
            ]

            # 총 데이터베이스 크기
            cursor.execute("""
                SELECT
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS total_size_mb
                FROM information_schema.TABLES
                WHERE table_schema = DATABASE()
            """)

            total_size = cursor.fetchone()
            stats['total_size_mb'] = total_size[0]

    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        stats = {'error': str(e)}

    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_activity(request):
    """
    사용자 활동 통계

    Query params:
        - hours: 조회 시간 범위 (기본 24시간)
    """
    hours = int(request.GET.get('hours', 24))
    since = timezone.now() - timedelta(hours=hours)

    # 활성 사용자 수
    active_users = APIUsageLog.objects.filter(
        created_at__gte=since,
        user__isnull=False
    ).values('user').distinct().count()

    # 사용자별 요청 수 (Top 10)
    top_users = list(
        APIUsageLog.objects.filter(
            created_at__gte=since,
            user__isnull=False
        ).values(
            'user__username',
            'user__first_name',
            'user__last_name'
        ).annotate(
            request_count=Count('id'),
            avg_response_time=Avg('response_time_ms')
        ).order_by('-request_count')[:10]
    )

    return Response({
        'period_hours': hours,
        'active_users': active_users,
        'top_users': top_users
    })


# 필요한 import 추가
from django.db.models import Max
