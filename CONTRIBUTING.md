# Contributing to NeuroNova

NeuroNova 프로젝트에 기여해주셔서 감사합니다! 이 문서는 프로젝트 기여 가이드라인입니다.

## 시작하기

### 1. 저장소 클론
```bash
git clone https://github.com/kimhanbyul1208/NeuroNova.git
cd NeuroNova
```

### 2. 개발 환경 설정
각자 담당 분야의 README를 참고하세요:
- [Django Backend](backend/django_main/README.md)
- [React Web](frontend/react_web/README.md)
- [Flutter App](frontend/flutter_app/README.md)

## 코딩 규칙

### 1. 개발 환경 & 기초 설정
- ✅ **가상환경 사용**: `venv` 생성 및 활성화
- ✅ **의존성 관리**: `requirements.txt` 또는 `package.json` 업데이트
- ✅ **버전 관리**: Git으로 모든 변경사항 추적

### 2. 설정 & 구성 관리 (Soft-coding)
- ✅ **보안 변수**: API Key, 비밀번호 등은 `.env` 파일에 저장
- ✅ **일반 설정**: URL, 버전 정보는 설정 파일에 변수로 관리
- ❌ **하드코딩 금지**: 코드에 직접 값을 넣지 않기

### 3. 코드 품질 & 설계
- ✅ **타입 힌트**: Python은 모든 함수에 타입 명시
- ✅ **로깅**: `logging` 모듈 사용 (print 대신)
- ✅ **디자인 패턴**: Factory, Strategy, Abstract 등 적용
- ✅ **OOP**: 재사용성과 구조적 설계 고려

### 4. 안정성 & 문서화
- ✅ **테스트**: 단위 테스트 작성
- ✅ **문서화**: 복잡한 로직에 주석 추가
- ✅ **README 업데이트**: 새 기능 추가 시 문서 갱신

## Git 워크플로우

### 브랜치 전략
- `main`: 프로덕션 브랜치
- `develop`: 개발 브랜치 (선택사항)
- `feature/*`: 새 기능 개발
- `bugfix/*`: 버그 수정
- `hotfix/*`: 긴급 수정

### 작업 프로세스

1. **최신 코드 받기**
```bash
git checkout main
git pull origin main
```

2. **새 브랜치 생성**
```bash
git checkout -b feature/your-feature-name
```

3. **작업 및 커밋**
```bash
git add .
git commit -m "feat: Add your feature description"
```

4. **푸시 및 PR 생성**
```bash
git push origin feature/your-feature-name
```
그 후 GitHub에서 Pull Request 생성

### 커밋 메시지 규칙

형식:
```
<type>: <subject>

<body> (선택사항)
```

**Type**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `chore`: 기타 작업

**예시**:
```bash
feat: Add patient appointment API
fix: Fix BMI calculation error
docs: Update API documentation
refactor: Improve database query performance
test: Add unit tests for SOAP model
```

## Pull Request 가이드라인

### PR 생성 전 체크리스트
- [ ] 코드가 정상 작동하는지 테스트
- [ ] 타입 힌트 추가
- [ ] 로깅 추가
- [ ] 환경변수 사용 (하드코딩 제거)
- [ ] 테스트 코드 작성
- [ ] 문서 업데이트

### PR 템플릿
```markdown
## 변경 사항
- 무엇을 변경했나요?

## 작업 이유
- 왜 이 작업이 필요한가요?

## 테스트 방법
- 어떻게 테스트했나요?

## 스크린샷 (선택사항)
- UI 변경이 있다면 스크린샷 첨부

## 체크리스트
- [ ] 코드 테스트 완료
- [ ] 타입 힌트 추가
- [ ] 문서 업데이트
```

## 코드 리뷰

### 리뷰어 체크사항
1. **기능성**: 코드가 의도한 대로 작동하는가?
2. **코드 품질**: 타입 힌트, 로깅, 주석이 있는가?
3. **보안**: 민감 정보가 하드코딩되지 않았는가?
4. **성능**: 비효율적인 쿼리나 로직이 없는가?
5. **테스트**: 테스트 코드가 작성되었는가?

### 리뷰 받는 사람
- 피드백을 긍정적으로 받아들이기
- 수정 요청 시 신속하게 대응
- 궁금한 점은 댓글로 질문

## 이슈 관리

### 이슈 생성
GitHub Issues에서 다음 정보 포함:
- **제목**: 명확하고 간결하게
- **설명**: 문제 상황, 재현 방법
- **라벨**: `bug`, `feature`, `documentation` 등
- **담당자**: 가능하면 담당자 지정

### 이슈 라벨
- `bug`: 버그 수정
- `feature`: 새 기능
- `documentation`: 문서 작업
- `enhancement`: 기능 개선
- `question`: 질문
- `help wanted`: 도움 필요

## 개발 환경별 가이드

### Python (Django/Flask)
```python
# 좋은 예
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

def get_patient_by_id(patient_id: int) -> Optional[Patient]:
    """
    Get patient by ID.

    Args:
        patient_id: Patient ID

    Returns:
        Patient object or None
    """
    try:
        patient = Patient.objects.get(id=patient_id)
        logger.info(f"Patient found: {patient_id}")
        return patient
    except Patient.DoesNotExist:
        logger.warning(f"Patient not found: {patient_id}")
        return None
```

### JavaScript/TypeScript (React)
```typescript
// 좋은 예
import { useState, useEffect } from 'react';
import { Patient } from '@/types';
import { getPatients } from '@/api';

interface PatientListProps {
  searchQuery?: string;
}

const PatientList: React.FC<PatientListProps> = ({ searchQuery }) => {
  const [patients, setPatients] = useState<Patient[]>([]);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const data = await getPatients(searchQuery);
        setPatients(data);
      } catch (error) {
        console.error('Failed to fetch patients:', error);
      }
    };

    fetchPatients();
  }, [searchQuery]);

  return (
    // JSX...
  );
};
```

### Dart (Flutter)
```dart
// 좋은 예
import 'package:flutter/material.dart';
import 'package:logging/logging.dart';

class AppointmentService {
  final Logger _logger = Logger('AppointmentService');

  Future<List<Appointment>> getAppointments({
    required String patientId,
  }) async {
    try {
      _logger.info('Fetching appointments for patient: $patientId');
      // API call...
      return appointments;
    } catch (e) {
      _logger.severe('Failed to fetch appointments', e);
      rethrow;
    }
  }
}
```

## 문의

질문이나 도움이 필요하면:
- GitHub Issues에 질문 등록
- 팀 채팅방에 문의
- [팀원 역할 분담 문서](docs/TEAM_ROLES.md) 참고

---

**Happy Coding! 🚀**
