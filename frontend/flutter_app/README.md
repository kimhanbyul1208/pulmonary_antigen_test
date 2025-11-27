# NeuroNova Patient App

환자용 Flutter 모바일 애플리케이션

## 기술 스택

- **Flutter 3.0+** - UI 프레임워크
- **Dart 3.0+** - 프로그래밍 언어
- **SQLCipher** - 암호화된 로컬 데이터베이스
- **Dio** - HTTP 클라이언트
- **Provider** - 상태 관리
- **Firebase** - Push 알림 (FCM)

## 주요 기능

### 보안
- ✅ **암호화 저장소**: SQLCipher로 모든 로컬 데이터 암호화
- ✅ **90일 자동 삭제**: 개인정보 보호를 위한 자동 데이터 삭제
- ✅ **JWT 인증**: 안전한 API 통신

### 핵심 기능
- 병원 예약 (생성, 조회, 취소)
- 진료 요약 조회
- Push 알림 수신
- 프로필 관리

## 설치 및 실행

### 1. Flutter 설치
Flutter SDK 설치: https://flutter.dev/docs/get-started/install

### 2. 의존성 설치
```bash
flutter pub get
```

### 3. 환경 설정
API URL 설정 (선택사항):
```bash
# Android Emulator (기본값)
flutter run

# 실제 서버 URL 사용
flutter run --dart-define=API_BASE_URL=http://your-server:8000
```

### 4. 앱 실행
```bash
# Android
flutter run

# iOS
flutter run -d ios

# 특정 디바이스
flutter devices
flutter run -d <device-id>
```

## 프로젝트 구조

```
lib/
├── core/
│   ├── config/
│   │   └── app_config.dart      # 앱 설정 (Soft-coding)
│   ├── constants/
│   │   └── app_constants.dart   # 상수 정의
│   └── utils/
│       └── logger.dart           # 로깅 유틸리티
├── data/
│   ├── local/
│   │   └── local_database.dart  # SQLCipher 암호화 DB
│   ├── models/
│   │   └── appointment_model.dart
│   └── repositories/
│       └── appointment_repository.dart
├── features/
│   ├── auth/                    # 로그인/로그아웃
│   ├── appointment/             # 예약 관리
│   ├── home/                    # 홈 화면
│   └── profile/                 # 프로필
└── main.dart                    # 앱 엔트리 포인트
```

## 데이터 보안 정책

### 암호화
모든 로컬 데이터는 SQLCipher로 암호화되어 저장됩니다:
- 예약 정보
- 진료 요약
- 알림 기록

### 90일 자동 삭제
개인정보 보호를 위해 모든 데이터는 생성일로부터 90일 후 자동 삭제됩니다:
- 앱 시작 시 만료된 데이터 검사
- 만료된 데이터 영구 삭제
- 삭제 로그 기록

```dart
// 예시: 앱 시작 시 자동 삭제
final deletedCount = await LocalDatabase.deleteExpiredData();
AppLogger.info('Deleted $deletedCount expired records');
```

## API 통신

### 엔드포인트
설정은 `lib/core/config/app_config.dart`에서 관리:

```dart
static const String apiBaseUrl = 'http://10.0.2.2:8000';  // Android emulator
static const String appointmentsEndpoint = '/api/v1/custom/appointments/';
```

### 인증
JWT 토큰을 사용한 인증:
- Access Token: API 요청에 사용
- Refresh Token: Access Token 갱신

## Firebase Push 알림

### 설정
1. Firebase 프로젝트 생성
2. `google-services.json` (Android) 또는 `GoogleService-Info.plist` (iOS) 추가
3. FCM 토큰 서버에 등록

### 알림 타입
- 예약 확정 알림
- 예약 리마인더
- 진료 결과 알림
- 처방전 발급 알림

## 빌드

### Android APK
```bash
flutter build apk --release
```

### Android App Bundle
```bash
flutter build appbundle --release
```

### iOS
```bash
flutter build ios --release
```

## 테스트

```bash
# 단위 테스트
flutter test

# 통합 테스트
flutter drive --target=test_driver/app.dart
```

## 코딩 규칙

- ✅ **Soft-coding**: 모든 설정 값은 `app_config.dart`에서 관리
- ✅ **타입 안정성**: 명시적 타입 선언
- ✅ **로깅**: `AppLogger` 사용
- ✅ **에러 처리**: try-catch 및 적절한 에러 메시지

## 문제 해결

### SQLCipher 빌드 오류
```bash
flutter clean
flutter pub get
flutter run
```

### API 연결 오류
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- 실제 디바이스: 서버의 실제 IP 주소 사용

## 배포

### Android
1. 서명 키 생성
2. `android/key.properties` 설정
3. `flutter build appbundle --release`
4. Google Play Console에 업로드

### iOS
1. Apple Developer 계정 필요
2. Xcode에서 서명 설정
3. `flutter build ios --release`
4. App Store Connect에 업로드

## 라이선스

TBD
