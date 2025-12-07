import 'package:flutter/material.dart';

import '../../data/models/report_model.dart';

class ReportDetailScreen extends StatefulWidget {
  final int initialTab;
  final ReportModel? report;

  const ReportDetailScreen({
    super.key, 
    this.initialTab = 0,
    this.report,
  });

  @override
  State<ReportDetailScreen> createState() => _ReportDetailScreenState();
}

class _ReportDetailScreenState extends State<ReportDetailScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  bool _isObscured = false; // Privacy mode

  @override
  void initState() {
    super.initState();
    _tabController = TabController(
      length: 3,
      vsync: this,
      initialIndex: widget.initialTab,
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('상세 분석 리포트'),
        actions: [
          IconButton(
            icon: Icon(_isObscured ? Icons.visibility_off : Icons.visibility),
            onPressed: () {
              setState(() {
                _isObscured = !_isObscured;
              });
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(_isObscured ? '민감 정보가 가려집니다.' : '민감 정보가 표시됩니다.'),
                  duration: const Duration(seconds: 1),
                ),
              );
            },
            tooltip: '정보 숨기기',
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'CT 분류'),
            Tab(text: 'MRI 분할'),
            Tab(text: '바이오마커'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildCtAnalysisTab(),
          _buildMriSegmentationTab(),
          _buildBiomarkerTab(),
        ],
      ),
    );
  }

  Widget _buildCtAnalysisTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '뇌종양 종류 예측 (CT 기반)',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'CNN (ResNet/VGG) 모델을 사용하여 CT 이미지를 분석한 결과입니다.',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 24),
          
          // Image Placeholder
          Container(
            height: 250,
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Center(
              child: Icon(Icons.image, size: 64, color: Colors.grey),
            ),
          ),
          const SizedBox(height: 24),

          if (widget.report != null && widget.report!.models.containsKey('ct')) ...[
            Text(
              '예측 확률 분포',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            ...(widget.report!.models['ct']!.details['probabilities'] as List<dynamic>).map((prob) {
              return _buildProbabilityBar(
                prob['label'],
                (prob['value'] as num).toDouble(),
                _getColorForLabel(prob['label']),
              );
            }).toList(),
          ] else
            const Text('CT 분석 결과가 없습니다.'),
        ],
      ),
    );
  }

  Widget _buildProbabilityBar(String label, double probability, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: const TextStyle(fontWeight: FontWeight.w500)),
              _buildSensitiveText(
                '${(probability * 100).toStringAsFixed(1)}%',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: probability,
              backgroundColor: Colors.grey[200],
              color: color,
              minHeight: 10,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMriSegmentationTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '뇌종양 분할 예측 (MRI 기반)',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'U-Net 모델을 사용하여 종양의 영역을 정밀하게 분할한 결과입니다.',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 24),

          // MRI Image Placeholder with Overlay
          Stack(
            children: [
              Container(
                height: 300,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Center(
                  child: Icon(Icons.medical_services, size: 64, color: Colors.white24),
                ),
              ),
              // Mock Overlay Legend
              Positioned(
                bottom: 16,
                right: 16,
                child: Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: Colors.black54,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildLegendItem('Whole Tumor', Colors.green),
                      const SizedBox(height: 4),
                      _buildLegendItem('Tumor Core', Colors.red),
                      const SizedBox(height: 4),
                      _buildLegendItem('Enhancing Tumor', Colors.yellow),
                    ],
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),

          if (widget.report != null && widget.report!.models.containsKey('mri')) ...[
            const Text(
              '영역별 분석',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildAnalysisRow('전체 종양 크기', widget.report!.models['mri']!.details['tumor_size'] ?? 'Unknown'),
            _buildAnalysisRow('활성 종양 비율', '65%'), // Mock for now if not in details
            _buildAnalysisRow('부종 영역', widget.report!.models['mri']!.details['edema'] ?? 'Unknown'),
          ] else
            const Text('MRI 분석 결과가 없습니다.'),
        ],
      ),
    );
  }

  Widget _buildLegendItem(String label, Color color) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 8),
        Text(label, style: const TextStyle(color: Colors.white, fontSize: 12)),
      ],
    );
  }

  Widget _buildBiomarkerTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '전이 및 심각도 예측 (바이오마커)',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            '단백체/유전체 분석을 통해 종양의 성격과 예후를 예측합니다.',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 24),

          // Risk Level Indicator
          Center(
            child: Column(
              children: [
                Container(
                  width: 120,
                  height: 120,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.red, width: 8),
                  ),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: const [
                        Text(
                          'Grade',
                          style: TextStyle(fontSize: 16, color: Colors.grey),
                        ),
                        Text(
                          'IV',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.red,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  '고위험군 (High Risk)',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),

          if (widget.report != null && widget.report!.models.containsKey('biomarker')) ...[
            const Text(
              '주요 바이오마커 수치',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Card(
              child: Column(
                children: (widget.report!.models['biomarker']!.details['markers'] as List<dynamic>).map((marker) {
                  return Column(
                    children: [
                      _buildBiomarkerItem(
                        marker['name'],
                        marker['value'],
                        marker['status'],
                        _getColorForStatus(marker['status']),
                      ),
                      const Divider(height: 1),
                    ],
                  );
                }).toList(),
              ),
            ),
          ] else
            const Text('바이오마커 분석 결과가 없습니다.'),
        ],
      ),
    );
  }

  Widget _buildBiomarkerItem(String name, String value, String interpretation, Color color) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(name, style: const TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 4),
              _buildSensitiveText(value, style: TextStyle(color: Colors.grey[700])),
            ],
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(20),
            ),
            child: _buildSensitiveText(
              interpretation,
              style: TextStyle(
                color: color,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAnalysisRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.grey)),
          _buildSensitiveText(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Color _getColorForLabel(String label) {
    if (label.contains('Glioblastoma')) return Colors.red;
    if (label.contains('Meningioma')) return Colors.orange;
    return Colors.green;
  }

  Color _getColorForStatus(String status) {
    if (status == 'Negative' || status == 'Resistant' || status == 'High') return Colors.red;
    if (status == 'Positive' || status == 'Sensitive' || status == 'Low') return Colors.blue;
    return Colors.orange;
  }

  Widget _buildSensitiveText(String text, {TextStyle? style}) {
    if (_isObscured) {
      return Text(
        '*****',
        style: style?.copyWith(color: Colors.grey) ?? const TextStyle(color: Colors.grey),
      );
    }
    return Text(text, style: style);
  }
}
