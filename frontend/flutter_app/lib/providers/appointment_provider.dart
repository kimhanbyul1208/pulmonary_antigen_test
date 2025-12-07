import 'package:flutter/foundation.dart';
import '../services/appointment_service.dart';
import '../data/models/appointment_model.dart';

class AppointmentProvider with ChangeNotifier {
  final AppointmentService _service = AppointmentService();
  
  List<AppointmentModel> _appointments = [];
  List<AppointmentModel> get appointments => _appointments;
  
  bool _isLoading = false;
  bool get isLoading => _isLoading;

  Future<void> loadAppointments() async {
    _isLoading = true;
    notifyListeners();

    try {
      _appointments = await _service.getAppointments();
    } catch (e) {
      print('Error loading appointments: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  List<AppointmentModel> get upcomingAppointments {
    final now = DateTime.now();
    return _appointments.where((a) => 
      (a.status == 'PENDING' || a.status == 'CONFIRMED') && 
      a.scheduledAt.isAfter(now)
    ).toList()..sort((a, b) => a.scheduledAt.compareTo(b.scheduledAt));
  }

  List<AppointmentModel> get pastAppointments {
    final now = DateTime.now();
    return _appointments.where((a) => 
      a.status == 'COMPLETED' || 
      a.status == 'CANCELLED' ||
      a.scheduledAt.isBefore(now)
    ).toList()..sort((a, b) => b.scheduledAt.compareTo(a.scheduledAt));
  }
}
