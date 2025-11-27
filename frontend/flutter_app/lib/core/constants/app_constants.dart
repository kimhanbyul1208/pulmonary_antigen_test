/// App Constants
/// All constant values used throughout the app

class AppConstants {
  // User Roles
  static const String roleAdmin = 'ADMIN';
  static const String roleDoctor = 'DOCTOR';
  static const String roleNurse = 'NURSE';
  static const String rolePatient = 'PATIENT';

  // Appointment Status
  static const String appointmentPending = 'PENDING';
  static const String appointmentConfirmed = 'CONFIRMED';
  static const String appointmentCancelled = 'CANCELLED';
  static const String appointmentNoShow = 'NO_SHOW';
  static const String appointmentCompleted = 'COMPLETED';

  // Visit Types
  static const String visitFirstVisit = 'FIRST_VISIT';
  static const String visitFollowUp = 'FOLLOW_UP';
  static const String visitCheckUp = 'CHECK_UP';
  static const String visitEmergency = 'EMERGENCY';

  // Tumor Types
  static const String tumorGlioma = 'Glioma';
  static const String tumorMeningioma = 'Meningioma';
  static const String tumorPituitary = 'Pituitary';
  static const String tumorNone = 'No Tumor';

  // Notification Types
  static const String notificationAppointmentReminder = 'APPOINTMENT_REMINDER';
  static const String notificationAppointmentConfirmed = 'APPOINTMENT_CONFIRMED';
  static const String notificationAppointmentCancelled = 'APPOINTMENT_CANCELLED';
  static const String notificationDiagnosisReady = 'DIAGNOSIS_READY';
  static const String notificationPrescriptionReady = 'PRESCRIPTION_READY';

  // Local Storage Keys
  static const String keyAccessToken = 'access_token';
  static const String keyRefreshToken = 'refresh_token';
  static const String keyUserId = 'user_id';
  static const String keyUserRole = 'user_role';
  static const String keyFcmToken = 'fcm_token';
  static const String keyLastSyncTime = 'last_sync_time';

  // Date Formats
  static const String dateFormatDisplay = 'yyyy-MM-dd';
  static const String dateTimeFormatDisplay = 'yyyy-MM-dd HH:mm';
  static const String dateFormatApi = 'yyyy-MM-ddTHH:mm:ss';

  // Error Messages
  static const String errorNetwork = '네트워크 연결을 확인해주세요';
  static const String errorAuth = '인증에 실패했습니다. 다시 로그인해주세요';
  static const String errorServer = '서버 오류가 발생했습니다';
  static const String errorUnknown = '알 수 없는 오류가 발생했습니다';
}
