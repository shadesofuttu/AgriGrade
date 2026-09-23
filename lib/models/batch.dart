class Batch {
  final int id;
  final String batchId;
  final int userId;
  final DateTime createdAt;
  final String? imageUrl;
  final int imageCount;
  final int totalOnions;
  final int gradeACount;
  final int ursCount;
  final int damagedCount;
  final int rottenCount;
  final int sproutedCount;
  final double gradeAPercentage;
  final double ursPercentage;
  final double damagedPercentage;
  final double rottenPercentage;
  final double sproutedPercentage;
  final double aiConfidence;
  final String modelVersion;

  Batch({
    required this.id,
    required this.batchId,
    required this.userId,
    required this.createdAt,
    this.imageUrl,
    required this.imageCount,
    required this.totalOnions,
    required this.gradeACount,
    required this.ursCount,
    required this.damagedCount,
    required this.rottenCount,
    required this.sproutedCount,
    required this.gradeAPercentage,
    required this.ursPercentage,
    required this.damagedPercentage,
    required this.rottenPercentage,
    required this.sproutedPercentage,
    required this.aiConfidence,
    required this.modelVersion,
  });

  factory Batch.fromJson(Map<String, dynamic> json) {
    return Batch(
      id: json['id'],
      batchId: json['batch_id'],
      userId: json['user_id'],
      createdAt: DateTime.parse(json['created_at']),
      imageUrl: json['image_url'],
      imageCount: json['image_count'],
      totalOnions: json['total_onions'],
      gradeACount: json['grade_a_count'],
      ursCount: json['urs_count'],
      damagedCount: json['damaged_count'],
      rottenCount: json['rotten_count'],
      sproutedCount: json['sprouted_count'],
      gradeAPercentage: json['grade_a_percentage'].toDouble(),
      ursPercentage: json['urs_percentage'].toDouble(),
      damagedPercentage: json['damaged_percentage'].toDouble(),
      rottenPercentage: json['rotten_percentage'].toDouble(),
      sproutedPercentage: json['sprouted_percentage'].toDouble(),
      aiConfidence: json['ai_confidence'].toDouble(),
      modelVersion: json['model_version'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'batch_id': batchId,
      'user_id': userId,
      'created_at': createdAt.toIso8601String(),
      'image_url': imageUrl,
      'image_count': imageCount,
      'total_onions': totalOnions,
      'grade_a_count': gradeACount,
      'urs_count': ursCount,
      'damaged_count': damagedCount,
      'rotten_count': rottenCount,
      'sprouted_count': sproutedCount,
      'grade_a_percentage': gradeAPercentage,
      'urs_percentage': ursPercentage,
      'damaged_percentage': damagedPercentage,
      'rotten_percentage': rottenPercentage,
      'sprouted_percentage': sproutedPercentage,
      'ai_confidence': aiConfidence,
      'model_version': modelVersion,
    };
  }
}