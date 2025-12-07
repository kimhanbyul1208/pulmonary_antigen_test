import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/appointment_provider.dart';
import '../../data/models/appointment_model.dart';
import '../../data/repositories/auth_repository.dart';

class AppointmentCreateScreen extends StatefulWidget {
  const AppointmentCreateScreen({super.key});

  @override
  State<AppointmentCreateScreen> createState() => _AppointmentCreateScreenState();
}

class _AppointmentCreateScreenState extends State<AppointmentCreateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _reasonController = TextEditingController();
  DateTime _selectedDate = DateTime.now().add(const Duration(days: 1));
  TimeOfDay _selectedTime = const TimeOfDay(hour: 9, minute: 0);
  String _visitType = 'CHECK_UP';

  final List<Map<String, String>> _visitTypes = [
    {'value': 'CHECK_UP', 'label': '정기 검진'},
    {'value': 'FIRST_VISIT', 'label': '초진'},
    {'value': 'FOLLOW_UP', 'label': '재진'},
    {'value': 'EMERGENCY', 'label': '응급'},
  ];

  @override
  void dispose() {
    _reasonController.dispose();
    super.dispose();
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Future<void> _selectTime(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: _selectedTime,
    );
    if (picked != null && picked != _selectedTime) {
      setState(() {
        _selectedTime = picked;
      });
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final scheduledAt = DateTime(
      _selectedDate.year,
      _selectedDate.month,
      _selectedDate.day,
      _selectedTime.hour,
      _selectedTime.minute,
    );

    // Get current user ID (assuming AuthRepository has it or we pass 0 and backend handles it)
    // For now, we'll try to get it from AuthRepository if possible, or default to 0
    // In a real app, the backend might infer the patient from the token
    int patientId = 0;
    try {
        final authRepo = context.read<AuthRepository>();
        final userInfo = await authRepo.getUserInfo();
        if (userInfo['userId'] != null) {
            patientId = int.tryParse(userInfo['userId']!) ?? 0;
        }
    } catch (e) {
        print('Error getting user ID: $e');
    }

    final newAppointment = AppointmentModel(
      patientId: patientId, 
      scheduledAt: scheduledAt,
      status: 'PENDING',
      visitType: _visitType,
      reason: _reasonController.text,
      createdAt: DateTime.now(),
      expireAt: DateTime.now().add(const Duration(days: 90)),
    );

    final success = await context
        .read<AppointmentProvider>()
        .createAppointment(newAppointment);

    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('예약이 접수되었습니다.')),
        );
        Navigator.pop(context, true);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('예약 접수에 실패했습니다.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('새 예약'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '진료 정보 입력',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 24),
              
              // Date Picker
              ListTile(
                title: const Text('날짜'),
                subtitle: Text(
                  '${_selectedDate.year}년 ${_selectedDate.month}월 ${_selectedDate.day}일',
                  style: const TextStyle(fontSize: 16),
                ),
                trailing: const Icon(Icons.calendar_today),
                onTap: () => _selectDate(context),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                  side: BorderSide(color: Colors.grey.shade300),
                ),
              ),
              const SizedBox(height: 16),

              // Time Picker
              ListTile(
                title: const Text('시간'),
                subtitle: Text(
                  _selectedTime.format(context),
                  style: const TextStyle(fontSize: 16),
                ),
                trailing: const Icon(Icons.access_time),
                onTap: () => _selectTime(context),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                  side: BorderSide(color: Colors.grey.shade300),
                ),
              ),
              const SizedBox(height: 24),

              // Visit Type Dropdown
              DropdownButtonFormField<String>(
                value: _visitType,
                decoration: const InputDecoration(
                  labelText: '진료 유형',
                  border: OutlineInputBorder(),
                ),
                items: _visitTypes.map((type) {
                  return DropdownMenuItem(
                    value: type['value'],
                    child: Text(type['label']!),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _visitType = value!;
                  });
                },
              ),
              const SizedBox(height: 24),

              // Reason Text Field
              TextFormField(
                controller: _reasonController,
                decoration: const InputDecoration(
                  labelText: '진료 사유',
                  hintText: '증상이나 방문 목적을 입력해주세요',
                  border: OutlineInputBorder(),
                  alignLabelWithHint: true,
                ),
                maxLines: 3,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return '진료 사유를 입력해주세요';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 32),

              // Submit Button
              SizedBox(
                width: double.infinity,
                height: 50,
                child: Consumer<AppointmentProvider>(
                  builder: (context, provider, child) {
                    return ElevatedButton(
                      onPressed: provider.isLoading ? null : _submit,
                      child: provider.isLoading
                          ? const CircularProgressIndicator()
                          : const Text(
                              '예약하기',
                              style: TextStyle(fontSize: 16),
                            ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
