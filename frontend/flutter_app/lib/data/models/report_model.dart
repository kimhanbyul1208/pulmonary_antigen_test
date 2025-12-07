class ReportModel {
  final int? patientId;
  final DateTime? generatedAt;
  final int overallScore;
  final String riskLevel;
  final String summary;
  final Map<String, ModelResult> models;

  ReportModel({
    this.patientId,
    this.generatedAt,
    required this.overallScore,
    required this.riskLevel,
    required this.summary,
    required this.models,
  });

  factory ReportModel.fromJson(Map<String, dynamic> json) {
    return ReportModel(
      patientId: json['patient_id'] != null ? int.tryParse(json['patient_id'].toString()) : null,
      generatedAt: json['generated_at'] != null ? DateTime.parse(json['generated_at']) : null,
      overallScore: json['overall_score'] ?? 0,
      riskLevel: json['risk_level'] ?? 'UNKNOWN',
      summary: json['summary'] ?? '',
      models: (json['models'] as Map<String, dynamic>?)?.map(
            (key, value) => MapEntry(key, ModelResult.fromJson(value)),
          ) ??
          {},
    );
  }
}

class ModelResult {
  final String modelName;
  final String result;
  final double confidence;
  final Map<String, dynamic> details;

  ModelResult({
    required this.modelName,
    required this.result,
    required this.confidence,
    required this.details,
  });

  factory ModelResult.fromJson(Map<String, dynamic> json) {
    return ModelResult(
      modelName: json['model_name'] ?? '',
      result: json['result'] ?? '',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      details: json['details'] as Map<String, dynamic>? ?? {},
    );
  }
}
