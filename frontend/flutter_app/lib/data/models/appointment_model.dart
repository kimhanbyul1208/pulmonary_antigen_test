/// Appointment Model
class AppointmentModel {
  final int? id;
  final int? serverId;
  final int patientId;
  final int? doctorId;
  final String? doctorName;
  final DateTime scheduledAt;
  final int durationMinutes;
  final String status;
  final String visitType;
  final String? reason;
  final String? notes;
  final DateTime createdAt;
  final DateTime expireAt;
  final bool synced;

  AppointmentModel({
    this.id,
    this.serverId,
    required this.patientId,
    this.doctorId,
    this.doctorName,
    required this.scheduledAt,
    this.durationMinutes = 30,
    required this.status,
    required this.visitType,
    this.reason,
    this.notes,
    required this.createdAt,
    required this.expireAt,
    this.synced = false,
  });

  /// From JSON (API response)
  factory AppointmentModel.fromJson(Map<String, dynamic> json) {
    return AppointmentModel(
      serverId: json['id'] as int?,
      patientId: json['patient_id'] as int? ?? json['patient'] as int,
      doctorId: json['doctor_id'] as int? ?? json['doctor'] as int?,
      doctorName: json['doctor_name'] as String?,
      scheduledAt: DateTime.parse(json['scheduled_at'] as String),
      durationMinutes: json['duration_minutes'] as int? ?? 30,
      status: json['status'] as String,
      visitType: json['visit_type'] as String,
      reason: json['reason'] as String?,
      notes: json['notes'] as String?,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'] as String)
          : DateTime.now(),
      expireAt: DateTime.now().add(const Duration(days: 90)),
      synced: true,
    );
  }

  /// To JSON (API request)
  Map<String, dynamic> toJson() {
    return {
      if (serverId != null) 'id': serverId,
      'patient_id': patientId,
      if (doctorId != null) 'doctor_id': doctorId,
      'scheduled_at': scheduledAt.toIso8601String(),
      'duration_minutes': durationMinutes,
      'status': status,
      'visit_type': visitType,
      if (reason != null) 'reason': reason,
      if (notes != null) 'notes': notes,
    };
  }

  /// From local database
  factory AppointmentModel.fromMap(Map<String, dynamic> map) {
    return AppointmentModel(
      id: map['id'] as int?,
      serverId: map['server_id'] as int?,
      patientId: map['patient_id'] as int,
      doctorId: map['doctor_id'] as int?,
      doctorName: map['doctor_name'] as String?,
      scheduledAt: DateTime.parse(map['scheduled_at'] as String),
      durationMinutes: map['duration_minutes'] as int? ?? 30,
      status: map['status'] as String,
      visitType: map['visit_type'] as String,
      reason: map['reason'] as String?,
      notes: map['notes'] as String?,
      createdAt: DateTime.parse(map['created_at'] as String),
      expireAt: DateTime.parse(map['expire_at'] as String),
      synced: (map['synced'] as int) == 1,
    );
  }

  /// To local database
  Map<String, dynamic> toMap() {
    return {
      if (id != null) 'id': id,
      if (serverId != null) 'server_id': serverId,
      'patient_id': patientId,
      if (doctorId != null) 'doctor_id': doctorId,
      if (doctorName != null) 'doctor_name': doctorName,
      'scheduled_at': scheduledAt.toIso8601String(),
      'duration_minutes': durationMinutes,
      'status': status,
      'visit_type': visitType,
      if (reason != null) 'reason': reason,
      if (notes != null) 'notes': notes,
      'created_at': createdAt.toIso8601String(),
      'expire_at': expireAt.toIso8601String(),
      'synced': synced ? 1 : 0,
    };
  }

  /// Copy with
  AppointmentModel copyWith({
    int? id,
    int? serverId,
    int? patientId,
    int? doctorId,
    String? doctorName,
    DateTime? scheduledAt,
    int? durationMinutes,
    String? status,
    String? visitType,
    String? reason,
    String? notes,
    DateTime? createdAt,
    DateTime? expireAt,
    bool? synced,
  }) {
    return AppointmentModel(
      id: id ?? this.id,
      serverId: serverId ?? this.serverId,
      patientId: patientId ?? this.patientId,
      doctorId: doctorId ?? this.doctorId,
      doctorName: doctorName ?? this.doctorName,
      scheduledAt: scheduledAt ?? this.scheduledAt,
      durationMinutes: durationMinutes ?? this.durationMinutes,
      status: status ?? this.status,
      visitType: visitType ?? this.visitType,
      reason: reason ?? this.reason,
      notes: notes ?? this.notes,
      createdAt: createdAt ?? this.createdAt,
      expireAt: expireAt ?? this.expireAt,
      synced: synced ?? this.synced,
    );
  }
}
