class AppConstants {
  // API Configuration
  static const String baseUrl = 'http://192.168.26.48:8000';
  static const String apiVersion = '/api';
  
  // API Endpoints
  static const String loginEndpoint = '$apiVersion/auth/login';
  static const String registerEndpoint = '$apiVersion/auth/register';
  static const String meEndpoint = '$apiVersion/auth/me';
  static const String batchesEndpoint = '$apiVersion/batches';
  static const String analysisEndpoint = '$apiVersion/analysis/upload';
  static const String reportEndpoint = '$apiVersion/analysis/report';
  
  // Storage Keys
  static const String tokenKey = 'auth_token';
  static const String userIdKey = 'user_id';
  static const String usernameKey = 'username';
  
  // Onion Quality Categories
  static const String gradeA = 'Grade A';
  static const String urs = 'URS';
  static const String damaged = 'Damaged';
  static const String rotten = 'Rotten';
  static const String sprouted = 'Sprouted';
  
  // Colors for categories
  static const int colorGradeA = 0xFF27AE60;
  static const int colorURS = 0xFFF39C12;
  static const int colorDamaged = 0xFFE67E22;
  static const int colorRotten = 0xFFE74C3C;
  static const int colorSprouted = 0xFF9B59B6;
  
  // App Settings
  static const int defaultTimeout = 30; // seconds
  static const int maxImageSize = 10 * 1024 * 1024; // 10MB
}