/**
 * About Page with QR Code for app download.
 */
const AboutPage = () => {
  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>NeuroNova 소개</h1>

      <section style={{ marginTop: '2rem' }}>
        <h2>프로젝트 개요</h2>
        <p>
          NeuroNova는 뇌종양 진단을 위한 임상 의사결정 지원 시스템(CDSS)입니다.
          AI 기술을 활용하여 의료진의 진단을 보조하고, 환자에게는 편리한 예약 및 알림 서비스를 제공합니다.
        </p>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h2>주요 기능</h2>
        <ul>
          <li>AI 기반 뇌종양 진단 (Glioma, Meningioma, Pituitary)</li>
          <li>설명가능한 AI (XAI) - SHAP, Grad-CAM</li>
          <li>DICOM 의료 영상 뷰어</li>
          <li>진료 기록 관리 (SOAP 차트)</li>
          <li>예약 시스템</li>
          <li>환자 알림 서비스</li>
        </ul>
      </section>

      <section style={{ marginTop: '2rem', textAlign: 'center' }}>
        <h2>환자용 모바일 앱</h2>
        <p>QR 코드를 스캔하여 NeuroNova 환자 앱을 다운로드하세요</p>

        <div style={{
          width: '200px',
          height: '200px',
          margin: '2rem auto',
          border: '2px solid #ccc',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#f5f5f5'
        }}>
          <p>[QR 코드 위치]</p>
        </div>

        <p style={{ fontSize: '0.9rem', color: '#666' }}>
          앱에서 예약, 진료 요약, 알림 서비스를 이용하실 수 있습니다
        </p>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h2>기술 스택</h2>
        <ul>
          <li>Frontend: React (의료진용 웹), Flutter (환자용 앱)</li>
          <li>Backend: Django (메인 API), Flask (AI 추론)</li>
          <li>Database: PostgreSQL, Redis</li>
          <li>AI/ML: Google Colab, ONNX</li>
          <li>DICOM: Orthanc Server</li>
        </ul>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h2>팀 NeuroNova</h2>
        <p>Neurology + Nova - 뇌과학의 새로운 별</p>
        <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '1rem' }}>
          GitHub: <a href="https://github.com/kimhanbyul1208/NeuroNova" target="_blank" rel="noopener noreferrer">
            https://github.com/kimhanbyul1208/NeuroNova
          </a>
        </p>
      </section>
    </div>
  );
};

export default AboutPage;
