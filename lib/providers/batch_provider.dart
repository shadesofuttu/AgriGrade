import 'package:flutter/material.dart';
import 'dart:io';
import '../models/batch.dart';
import '../services/api_service.dart';

class BatchProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<Batch> _batches = [];
  Batch? _currentBatch;
  bool _isLoading = false;
  String? _error;

  List<Batch> get batches => _batches;
  Batch? get currentBatch => _currentBatch;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadBatches() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _batches = await _apiService.getBatches();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadBatch(String batchId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _currentBatch = await _apiService.getBatch(batchId);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> uploadAndAnalyze(File imageFile) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _currentBatch = await _apiService.uploadAndAnalyze(imageFile);
      // Reload batches list
      await loadBatches();
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> deleteBatch(String batchId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _apiService.deleteBatch(batchId);
      _batches.removeWhere((batch) => batch.batchId == batchId);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<List<int>?> downloadReport(String batchId) async {
    try {
      return await _apiService.downloadReport(batchId);
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return null;
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }

  void clearCurrentBatch() {
    _currentBatch = null;
    notifyListeners();
  }
}