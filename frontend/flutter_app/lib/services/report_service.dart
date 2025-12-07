import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../core/config/app_config.dart';
import '../core/utils/logger.dart';
import '../data/models/report_model.dart';

class ReportService {
  final Dio _dio = Dio();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<ReportModel?> getLatestReport(int patientId) async {
    try {
      final token = await _storage.read(key: 'access_token');
      if (token == null) {
        AppLogger.warning('No access token found');
        return null;
      }

      final response = await _dio.get(
        '${AppConfig.apiBaseUrl}/api/v1/emr/reports/latest/',
        queryParameters: {'patient_id': patientId},
        options: Options(
          headers: {
            'Authorization': 'Bearer $token',
            'Content-Type': 'application/json',
          },
        ),
      );

      if (response.statusCode == 200) {
        return ReportModel.fromJson(response.data);
      } else {
        AppLogger.error('Failed to load report: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      AppLogger.error('Error fetching report', e);
      return null;
    }
  }
}
