import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../data/models/appointment_model.dart';
import '../core/config/app_config.dart';
import '../core/utils/logger.dart';

class AppointmentService {
  final Dio _dio;
  final FlutterSecureStorage _storage;

  AppointmentService({Dio? dio, FlutterSecureStorage? storage})
      : _dio = dio ?? Dio(),
        _storage = storage ?? const FlutterSecureStorage();

  // API에서 예약 목록 가져오기
  Future<List<AppointmentModel>> getAppointments() async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token == null) {
        // 토큰이 없으면 빈 리스트 반환하거나 에러 발생
        // 여기서는 빈 리스트 반환하여 UI에서 처리하도록 함 (또는 로그인 화면으로 이동)
        AppLogger.warning('No access token found');
        return [];
      }

      final response = await _dio.get(
        '${AppConfig.apiBaseUrl}/api/v1/emr/encounters/',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        ),
      );

      if (response.statusCode == 200) {
        final data = response.data;
        List<dynamic> results;

        // DRF Pagination 처리
        if (data is Map<String, dynamic> && data.containsKey('results')) {
          results = data['results'];
        } else if (data is List) {
          results = data;
        } else {
          results = [];
        }

        return results
            .map((json) => AppointmentModel.fromJson(json))
            .toList();
      } else {
        throw Exception('예약 정보를 불러오는데 실패했습니다: ${response.statusCode}');
      }
    } on DioException catch (e) {
      AppLogger.error('Fetch appointments error: ${e.message}');
      // 네트워크 에러 시 빈 리스트 반환 또는 재시도 로직
      // 여기서는 에러를 throw하여 Provider에서 처리
      throw Exception('서버 연결 중 오류가 발생했습니다.');
    } catch (e) {
      AppLogger.error('Unexpected error fetching appointments: $e');
      throw Exception('예약 정보를 불러오는 중 오류가 발생했습니다.');
    }
  }

  // 예약 생성 (API 연동)
  Future<AppointmentModel> createAppointment(AppointmentModel appointment) async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token == null) throw Exception('로그인이 필요합니다.');

      // API 필드에 맞게 변환
      final data = appointment.toJson();
      
      // Backend expects 'encounter_date' instead of 'scheduled_at'
      if (data.containsKey('scheduled_at')) {
        data['encounter_date'] = data['scheduled_at'];
        data.remove('scheduled_at');
      }
      
      // Backend expects 'facility' (use visitType or default)
      data['facility'] = appointment.visitType; 
      
      // Backend expects 'patient' ID (ensure it's sent)
      if (!data.containsKey('patient')) {
         data['patient'] = appointment.patientId;
      }

      final response = await _dio.post(
        '${AppConfig.apiBaseUrl}/api/v1/emr/encounters/',
        data: data,
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        ),
      );

      if (response.statusCode == 201) {
        return AppointmentModel.fromJson(response.data);
      } else {
        throw Exception('예약 생성 실패: ${response.statusCode}');
      }
    } catch (e) {
      AppLogger.error('Create appointment error: $e');
      throw e;
    }
  }
  // 예약 취소
  Future<void> cancelAppointment(int id) async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token == null) throw Exception('로그인이 필요합니다.');

      final response = await _dio.post(
        '${AppConfig.apiBaseUrl}/api/v1/emr/encounters/$id/cancel/',
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        ),
      );

      if (response.statusCode != 200) {
        throw Exception('예약 취소 실패: ${response.statusCode}');
      }
    } catch (e) {
      AppLogger.error('Cancel appointment error: $e');
      throw e;
    }
  }
}
