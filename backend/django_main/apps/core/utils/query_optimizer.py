"""
데이터베이스 쿼리 최적화 유틸리티
"""

from django.db.models import Prefetch, Count, Q, Exists, OuterRef
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """
    쿼리 최적화 헬퍼 클래스
    """

    @staticmethod
    def optimize_patient_queryset(queryset):
        """
        환자 쿼리셋 최적화

        Args:
            queryset: Patient 쿼리셋

        Returns:
            최적화된 쿼리셋
        """
        from apps.emr.models import Encounter, FormVitals

        return queryset.select_related(
            'user'  # 1:1 관계 JOIN
        ).prefetch_related(
            # 최근 진료 기록 5개만 prefetch
            Prefetch(
                'encounters',
                queryset=Encounter.objects.select_related(
                    'doctor'
                ).order_by('-encounter_date')[:5]
            ),
            # 최근 바이탈 사인 3개만
            Prefetch(
                'vitals',
                queryset=FormVitals.objects.order_by('-date')[:3]
            )
        ).annotate(
            # 집계 데이터 미리 계산
            total_encounters=Count('encounters'),
            pending_encounters=Count(
                'encounters',
                filter=Q(encounters__status='pending')
            )
        )

    @staticmethod
    def optimize_encounter_queryset(queryset):
        """
        진료 기록 쿼리셋 최적화
        """
        return queryset.select_related(
            'patient__user',  # 환자 정보 JOIN
            'doctor'          # 의사 정보 JOIN
        ).prefetch_related(
            'soap',   # SOAP 노트
            'vitals'  # 바이탈 사인
        )

    @staticmethod
    def batch_load_related(instances, related_field, queryset=None):
        """
        N+1 쿼리 방지를 위한 배치 로드

        Args:
            instances: 모델 인스턴스 리스트
            related_field: 관련 필드명
            queryset: 커스텀 쿼리셋 (선택)

        Returns:
            관련 객체 딕셔너리 {instance_id: [related_objects]}
        """
        if not instances:
            return {}

        model = instances[0].__class__
        related_model = model._meta.get_field(related_field).related_model

        # 인스턴스 ID 수집
        instance_ids = [inst.id for inst in instances]

        # 배치 쿼리
        if queryset is None:
            related_objects = related_model.objects.filter(
                **{f'{model.__name__.lower()}_id__in': instance_ids}
            )
        else:
            related_objects = queryset

        # 그룹핑
        related_dict = {}
        for obj in related_objects:
            parent_id = getattr(obj, f'{model.__name__.lower()}_id')
            if parent_id not in related_dict:
                related_dict[parent_id] = []
            related_dict[parent_id].append(obj)

        return related_dict

    @staticmethod
    def get_or_none(model, **kwargs):
        """
        객체 조회 (없으면 None 반환)
        DoesNotExist 예외 처리 불필요

        Args:
            model: Django 모델
            **kwargs: 필터 조건

        Returns:
            모델 인스턴스 또는 None
        """
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    @staticmethod
    def exists_subquery(related_model, filter_field, **filters):
        """
        Exists 서브쿼리 생성 (성능 최적화)

        Usage:
            Patient.objects.annotate(
                has_pending_encounters=QueryOptimizer.exists_subquery(
                    Encounter,
                    'patient',
                    status='pending'
                )
            )

        Args:
            related_model: 관련 모델
            filter_field: 필터할 필드
            **filters: 추가 필터 조건

        Returns:
            Exists 쿼리
        """
        subquery = related_model.objects.filter(
            **{filter_field: OuterRef('pk')},
            **filters
        )
        return Exists(subquery)

    @staticmethod
    def chunked_bulk_create(model, objects, chunk_size=500):
        """
        대량 데이터 삽입 (청크 단위)

        Args:
            model: Django 모델
            objects: 삽입할 객체 리스트
            chunk_size: 청크 크기

        Returns:
            삽입된 객체 수
        """
        total_created = 0

        for i in range(0, len(objects), chunk_size):
            chunk = objects[i:i + chunk_size]
            model.objects.bulk_create(chunk, ignore_conflicts=True)
            total_created += len(chunk)
            logger.info(f"Bulk created {total_created}/{len(objects)} objects")

        return total_created

    @staticmethod
    def chunked_bulk_update(model, objects, fields, chunk_size=500):
        """
        대량 데이터 업데이트 (청크 단위)

        Args:
            model: Django 모델
            objects: 업데이트할 객체 리스트
            fields: 업데이트할 필드 리스트
            chunk_size: 청크 크기

        Returns:
            업데이트된 객체 수
        """
        total_updated = 0

        for i in range(0, len(objects), chunk_size):
            chunk = objects[i:i + chunk_size]
            model.objects.bulk_update(chunk, fields)
            total_updated += len(chunk)
            logger.info(f"Bulk updated {total_updated}/{len(objects)} objects")

        return total_updated

    @staticmethod
    def analyze_query(queryset):
        """
        쿼리 분석 (EXPLAIN)

        Args:
            queryset: Django 쿼리셋

        Returns:
            EXPLAIN 결과
        """
        from django.db import connection

        query = str(queryset.query)

        with connection.cursor() as cursor:
            cursor.execute(f"EXPLAIN {query}")
            results = cursor.fetchall()

        logger.info(f"Query: {query}")
        logger.info(f"EXPLAIN:\n{results}")

        return results

    @staticmethod
    def get_slow_queries(threshold_ms=100):
        """
        느린 쿼리 목록 조회

        Args:
            threshold_ms: 임계값 (밀리초)

        Returns:
            느린 쿼리 리스트
        """
        from django.db import connection

        slow_queries = []

        for query in connection.queries:
            time_ms = float(query['time']) * 1000
            if time_ms > threshold_ms:
                slow_queries.append({
                    'sql': query['sql'],
                    'time_ms': time_ms
                })

        return slow_queries


class CacheHelper:
    """
    캐싱 헬퍼 클래스
    """

    @staticmethod
    def get_or_set(cache_key, func, timeout=300):
        """
        캐시 조회 또는 설정

        Args:
            cache_key: 캐시 키
            func: 캐시 미스 시 실행할 함수
            timeout: 캐시 유효 시간 (초)

        Returns:
            캐시된 값 또는 함수 실행 결과
        """
        from django.core.cache import cache

        value = cache.get(cache_key)

        if value is None:
            value = func()
            cache.set(cache_key, value, timeout)
            logger.debug(f"Cache miss: {cache_key}")
        else:
            logger.debug(f"Cache hit: {cache_key}")

        return value

    @staticmethod
    def invalidate_pattern(pattern):
        """
        패턴에 맞는 캐시 키 모두 삭제

        Args:
            pattern: 캐시 키 패턴 (예: 'patient:*')
        """
        from django.core.cache import cache
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")

        # 패턴 매칭 키 찾기
        keys = redis_conn.keys(f'*{pattern}*')

        # 삭제
        if keys:
            cache.delete_many([key.decode() for key in keys])
            logger.info(f"Invalidated {len(keys)} cache keys matching '{pattern}'")

    @staticmethod
    def get_cache_stats():
        """
        캐시 통계 조회

        Returns:
            캐시 통계 딕셔너리
        """
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")
        info = redis_conn.info('stats')

        total_requests = info['keyspace_hits'] + info['keyspace_misses']
        hit_rate = 0

        if total_requests > 0:
            hit_rate = (info['keyspace_hits'] / total_requests) * 100

        return {
            'hits': info['keyspace_hits'],
            'misses': info['keyspace_misses'],
            'hit_rate': f'{hit_rate:.2f}%',
            'total_keys': len(redis_conn.keys('*'))
        }


# 전역 인스턴스
query_optimizer = QueryOptimizer()
cache_helper = CacheHelper()
