from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PatientReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the latest multi-modal report for a patient",
        manual_parameters=[
            openapi.Parameter('patient_id', openapi.IN_QUERY, description="Patient ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: "Success"}
    )
    @action(detail=False, methods=['get'])
    def latest(self, request):
        patient_id = request.query_params.get('patient_id')
        
        # In a real scenario, we would fetch data from ML models or InferenceLog
        # For now, we return the structured mock data that the frontend expects
        
        mock_data = {
            "patient_id": patient_id,
            "generated_at": "2024-12-08T10:00:00Z",
            "overall_score": 85,
            "risk_level": "HIGH",
            "summary": "환자의 뇌 영상(CT/MRI) 및 바이오마커 분석 결과, 악성 교모세포종(Glioblastoma)의 가능성이 높습니다. 종양의 위치는 좌측 전두엽이며, 주변 조직으로의 침윤이 관찰됩니다.",
            "models": {
                "ct": {
                    "model_name": "Brain Tumor Classification (CT)",
                    "result": "Glioblastoma",
                    "confidence": 0.985,
                    "details": {
                        "probabilities": [
                            {"label": "Glioblastoma", "value": 0.85},
                            {"label": "Meningioma", "value": 0.10},
                            {"label": "Pituitary", "value": 0.05}
                        ]
                    }
                },
                "mri": {
                    "model_name": "Brain Tumor Segmentation (MRI)",
                    "result": "Active Tumor Detected",
                    "confidence": 0.92,
                    "details": {
                        "tumor_size": "4.2cm x 3.5cm",
                        "tumor_type": "Active",
                        "edema": "Moderate"
                    }
                },
                "biomarker": {
                    "model_name": "Biomarker Risk Analysis",
                    "result": "Grade IV",
                    "confidence": 0.88,
                    "details": {
                        "grade": "IV",
                        "markers": [
                            {"name": "IDH1", "value": "Wild-type", "status": "Negative"},
                            {"name": "MGMT", "value": "Unmethylated", "status": "Resistant"},
                            {"name": "Ki-67", "value": "45%", "status": "High"}
                        ]
                    }
                }
            }
        }
        
        return Response(mock_data)

    @swagger_auto_schema(
        operation_description="Get patient risk score history statistics",
        manual_parameters=[
            openapi.Parameter('patient_id', openapi.IN_QUERY, description="Patient ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: "Success"}
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        patient_id = request.query_params.get('patient_id')
        
        # Mock data for the last 6 months
        statistics_data = [
            {"date": "2025-07", "score": 65, "risk_level": "MODERATE"},
            {"date": "2025-08", "score": 68, "risk_level": "MODERATE"},
            {"date": "2025-09", "score": 72, "risk_level": "HIGH"},
            {"date": "2025-10", "score": 75, "risk_level": "HIGH"},
            {"date": "2025-11", "score": 80, "risk_level": "HIGH"},
            {"date": "2025-12", "score": 85, "risk_level": "HIGH"},
        ]
        
        return Response({
            "patient_id": patient_id,
            "history": statistics_data
        })
