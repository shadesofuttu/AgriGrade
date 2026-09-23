import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../providers/batch_provider.dart';
import '../models/batch.dart';
import '../utils/constants.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class BatchDetailScreen extends StatefulWidget {
  final String batchId;

  const BatchDetailScreen({super.key, required this.batchId});

  @override
  State<BatchDetailScreen> createState() => _BatchDetailScreenState();
}

class _BatchDetailScreenState extends State<BatchDetailScreen> {
  @override
  void initState() {
    super.initState();
    _loadBatch();
  }

  Future<void> _loadBatch() async {
    await Provider.of<BatchProvider>(context, listen: false)
        .loadBatch(widget.batchId);
  }

  Color _getCategoryColor(String category) {
    switch (category) {
      case 'Grade A':
        return const Color(AppConstants.colorGradeA);
      case 'URS':
        return const Color(AppConstants.colorURS);
      case 'Damaged':
        return const Color(AppConstants.colorDamaged);
      case 'Rotten':
        return const Color(AppConstants.colorRotten);
      case 'Sprouted':
        return const Color(AppConstants.colorSprouted);
      default:
        return Colors.grey;
    }
  }

  Future<void> _downloadReport() async {
    final batchProvider = Provider.of<BatchProvider>(context, listen: false);
    
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Downloading report...')),
    );

    final pdfBytes = await batchProvider.downloadReport(widget.batchId);
    
    if (pdfBytes != null && mounted) {
      try {
        final directory = await getApplicationDocumentsDirectory();
        final file = File('${directory.path}/onion_report_${widget.batchId}.pdf');
        await file.writeAsBytes(pdfBytes);
        
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Report saved to ${file.path}'),
              backgroundColor: Colors.green,
            ),
          );
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error saving report: $e'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Failed to download report'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Batch Details'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.download),
            onPressed: _downloadReport,
            tooltip: 'Download Report',
          ),
        ],
      ),
      body: Consumer<BatchProvider>(
        builder: (context, batchProvider, child) {
          if (batchProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (batchProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 64, color: Colors.red),
                  const SizedBox(height: 16),
                  Text('Error: ${batchProvider.error}'),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _loadBatch,
                    child: const Text('Retry'),
                  ),
                ],
              ),
            );
          }

          final batch = batchProvider.currentBatch;
          if (batch == null) {
            return const Center(child: Text('Batch not found'));
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Batch info
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Batch Information',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 12),
                        _buildInfoRow('Batch ID', batch.batchId),
                        _buildInfoRow(
                          'Date',
                          DateFormat('yyyy-MM-dd HH:mm').format(batch.createdAt),
                        ),
                        _buildInfoRow('Total Sample', '${batch.totalOnions} onions'),
                        _buildInfoRow(
                          'AI Confidence',
                          '${batch.aiConfidence.toStringAsFixed(1)}%',
                        ),
                        _buildInfoRow('Model Version', batch.modelVersion),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                // Quality distribution
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Quality Distribution',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 16),
                        _buildCategoryBar(
                          'Grade A (Healthy)',
                          batch.gradeACount,
                          batch.gradeAPercentage,
                        ),
                        const SizedBox(height: 12),
                        _buildCategoryBar(
                          'URS (Undersized)',
                          batch.ursCount,
                          batch.ursPercentage,
                        ),
                        const SizedBox(height: 12),
                        _buildCategoryBar(
                          'Damaged',
                          batch.damagedCount,
                          batch.damagedPercentage,
                        ),
                        const SizedBox(height: 12),
                        _buildCategoryBar(
                          'Rotten',
                          batch.rottenCount,
                          batch.rottenPercentage,
                        ),
                        const SizedBox(height: 12),
                        _buildCategoryBar(
                          'Sprouted',
                          batch.sproutedCount,
                          batch.sproutedPercentage,
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                // Assessment
                _buildAssessmentCard(batch),
                const SizedBox(height: 24),
                // Download button
                ElevatedButton.icon(
                  onPressed: _downloadReport,
                  icon: const Icon(Icons.picture_as_pdf),
                  label: const Text('Download PDF Report'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
          Text(value),
        ],
      ),
    );
  }

  Widget _buildCategoryBar(String category, int count, double percentage) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              category,
              style: const TextStyle(fontWeight: FontWeight.w500),
            ),
            Text(
              '$count (${percentage.toStringAsFixed(1)}%)',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 4),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: percentage / 100,
            minHeight: 8,
            backgroundColor: Colors.grey[300],
            valueColor: AlwaysStoppedAnimation<Color>(
              _getCategoryColor(category.split(' ')[0]),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAssessmentCard(Batch batch) {
    String assessment;
    Color color;
    IconData icon;

    if (batch.gradeAPercentage >= 70) {
      assessment = 'Excellent quality batch. Suitable for premium markets.';
      color = Colors.green;
      icon = Icons.thumb_up;
    } else if (batch.gradeAPercentage >= 50) {
      assessment = 'Good quality batch. Suitable for standard markets.';
      color = Colors.orange;
      icon = Icons.check_circle;
    } else {
      assessment = 'Below standard quality. Further sorting recommended.';
      color = Colors.red;
      icon = Icons.warning;
    }

    return Card(
      color: color.withValues(alpha: 0.1),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Quality Assessment',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: color,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    assessment,
                    style: const TextStyle(fontSize: 14),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}