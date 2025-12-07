import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Grid,
  Chip
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { LoadingSpinner, ErrorAlert } from '../components';
import axiosClient from '../api/axios';
import { API_ENDPOINTS, API_CONFIG } from '../utils/config';

/**
 * DICOM 뷰어 페이지
 * Orthanc 서버와 통합하여 의료 영상 표시
 */
const DicomViewerPage = () => {
  const { studyId } = useParams();
  const navigate = useNavigate();
  const [studyInfo, setStudyInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDemoMode, setIsDemoMode] = useState(false);

  // Orthanc 서버 URL (환경 변수 또는 config에서 가져와야 함)
  const orthancUrl = API_CONFIG.ORTHANC_URL || 'http://localhost:8042';

  useEffect(() => {
    const fetchStudyInfo = async () => {
      try {
        setLoading(true);
        setError(null);

        // Orthanc API로 Study 정보 가져오기
        // Set a timeout to fail fast if Orthanc is not running
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2000);

        const response = await fetch(`${orthancUrl}/studies/${studyId}`, {
          headers: {
            'Authorization': 'Basic ' + btoa('orthanc:orthanc')
          },
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!response.ok) {
          throw new Error('Study를 불러올 수 없습니다.');
        }

        const data = await response.json();
        setStudyInfo(data);
      } catch (err) {
        console.warn('Orthanc connection failed, switching to Demo Mode:', err);
        setIsDemoMode(true);
        // Mock Data for Demo
        setStudyInfo({
          ID: studyId || 'demo-study-123',
          MainDicomTags: {
            PatientID: 'DEMO-PATIENT-001',
            StudyDate: '2023-12-08',
            ModalitiesInStudy: 'MRI',
            StudyDescription: 'Brain MRI (Demo)'
          }
        });
      } finally {
        setLoading(false);
      }
    };

    if (studyId) {
      fetchStudyInfo();
    }
  }, [studyId, orthancUrl]);

  // Orthanc Web Viewer URL
  const viewerUrl = `${orthancUrl}/app/explorer.html#study?uuid=${studyId}`;
  // Demo Image (Placeholder)
  const demoImageUrl = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/MRI_of_Human_Brain.jpg/600px-MRI_of_Human_Brain.jpg";

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  // Error is only shown if even Demo Mode fails (unlikely here)
  if (error && !isDemoMode) {
    return (
      <Container maxWidth="lg" sx={{ marginTop: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate(-1)}
          sx={{ marginBottom: 2 }}
        >
          뒤로 가기
        </Button>
        <ErrorAlert
          message={error}
          title="DICOM 로딩 오류"
          onRetry={() => window.location.reload()}
        />
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ marginTop: 2, marginBottom: 2 }}>
      {/* 헤더 */}
      <Box sx={{ marginBottom: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate(-1)}
        >
          뒤로 가기
        </Button>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="h5" component="h1">
            DICOM 뷰어
          </Typography>
          {isDemoMode && (
            <Chip label="Demo Mode" color="warning" size="small" />
          )}
        </Box>
        <Box sx={{ width: 100 }} /> {/* Spacer for centering */}
      </Box>

      {/* Study 정보 */}
      {studyInfo && (
        <Paper sx={{ padding: 2, marginBottom: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Study ID
              </Typography>
              <Typography variant="body1">{studyInfo.ID || '-'}</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Patient ID
              </Typography>
              <Typography variant="body1">
                {studyInfo.MainDicomTags?.PatientID || '-'}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Study Date
              </Typography>
              <Typography variant="body1">
                {studyInfo.MainDicomTags?.StudyDate || '-'}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">
                Modality
              </Typography>
              <Chip
                label={studyInfo.MainDicomTags?.ModalitiesInStudy || 'Unknown'}
                size="small"
                color="primary"
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="text.secondary">
                Study Description
              </Typography>
              <Typography variant="body1">
                {studyInfo.MainDicomTags?.StudyDescription || '-'}
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* DICOM Viewer Area */}
      <Paper sx={{ padding: 0, height: 'calc(100vh - 250px)', overflow: 'hidden', display: 'flex', justifyContent: 'center', alignItems: 'center', bgcolor: 'black' }}>
        {isDemoMode ? (
          <Box sx={{ textAlign: 'center', color: 'white' }}>
            <img
              src={demoImageUrl}
              alt="Demo MRI"
              style={{ maxHeight: '60vh', maxWidth: '100%', objectFit: 'contain' }}
            />
            <Typography variant="subtitle1" sx={{ mt: 2 }}>
              Orthanc 서버에 연결할 수 없어 데모 이미지를 표시합니다.
            </Typography>
          </Box>
        ) : (
          <iframe
            src={viewerUrl}
            title="DICOM Viewer"
            width="100%"
            height="100%"
            style={{
              border: 'none',
              display: 'block'
            }}
          />
        )}
      </Paper>

      {/* 안내 메시지 */}
      <Box sx={{ marginTop: 2, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Orthanc Web Viewer를 사용하여 DICOM 영상을 표시합니다.
        </Typography>
        <Typography variant="body2" color="text.secondary">
          더 나은 시각화를 위해 OHIF Viewer 또는 Cornerstone.js 통합을 권장합니다.
        </Typography>
      </Box>
    </Container>
  );
};

export default DicomViewerPage;
