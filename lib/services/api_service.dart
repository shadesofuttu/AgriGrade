import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../utils/constants.dart';
import '../models/user.dart';
import '../models/batch.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  String? _token;

  Future<void> _loadToken() async {
    if (_token == null) {
      final prefs = await SharedPreferences.getInstance();
      _token = prefs.getString(AppConstants.tokenKey);
    }
  }

  Future<void> _saveToken(String token) async {
    _token = token;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(AppConstants.tokenKey, token);
  }

  Future<void> clearToken() async {
    _token = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.tokenKey);
  }

  Map<String, String> _getHeaders({bool includeAuth = true}) {
    final headers = {
      'Content-Type': 'application/json',
    };
    if (includeAuth && _token != null) {
      headers['Authorization'] = 'Bearer $_token';
    }
    return headers;
  }

  // Auth APIs
  Future<String> login(String username, String password) async {
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.loginEndpoint}');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {
        'username': username,
        'password': password,
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final token = data['access_token'];
      await _saveToken(token);
      return token;
    } else {
      throw Exception('Login failed: ${response.body}');
    }
  }

  Future<User> register(String username, String email, String fullName, String password) async {
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.registerEndpoint}');
    final response = await http.post(
      url,
      headers: _getHeaders(includeAuth: false),
      body: jsonEncode({
        'username': username,
        'email': email,
        'full_name': fullName,
        'password': password,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return User.fromJson(data);
    } else {
      throw Exception('Registration failed: ${response.body}');
    }
  }

  Future<User> getCurrentUser() async {
    await _loadToken();
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.meEndpoint}');
    final response = await http.get(
      url,
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return User.fromJson(data);
    } else {
      throw Exception('Failed to get user: ${response.body}');
    }
  }

  // Batch APIs
  Future<List<Batch>> getBatches({int skip = 0, int limit = 20}) async {
    await _loadToken();
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.batchesEndpoint}?skip=$skip&limit=$limit');
    final response = await http.get(
      url,
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final batches = (data['batches'] as List)
          .map((batch) => Batch.fromJson(batch))
          .toList();
      return batches;
    } else {
      throw Exception('Failed to get batches: ${response.body}');
    }
  }

  Future<Batch> getBatch(String batchId) async {
    await _loadToken();
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.batchesEndpoint}/$batchId');
    final response = await http.get(
      url,
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return Batch.fromJson(data);
    } else {
      throw Exception('Failed to get batch: ${response.body}');
    }
  }

  Future<void> deleteBatch(String batchId) async {
    await _loadToken();
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.batchesEndpoint}/$batchId');
    final response = await http.delete(
      url,
      headers: _getHeaders(),
    );

    if (response.statusCode != 204) {
      throw Exception('Failed to delete batch: ${response.body}');
    }
  }

  // Analysis APIs
  Future<Batch> uploadAndAnalyze(File imageFile) async {
    await _loadToken();
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.analysisEndpoint}');
    
    var request = http.MultipartRequest('POST', url);
    request.headers['Authorization'] = 'Bearer $_token';
    request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return Batch.fromJson(data);
    } else {
      throw Exception('Failed to analyze image: ${response.body}');
    }
  }

  Future<List<int>> downloadReport(String batchId) async {
    await _loadToken();
    final url = Uri.parse('${AppConstants.baseUrl}${AppConstants.reportEndpoint}/$batchId');
    final response = await http.get(
      url,
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return response.bodyBytes;
    } else {
      throw Exception('Failed to download report: ${response.body}');
    }
  }
}