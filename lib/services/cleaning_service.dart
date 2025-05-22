import 'dart:convert';
import 'package:http/http.dart' as http;

class CleaningService {
  static const String baseUrl = 'http://localhost:8000';

  Future<List<dynamic>> getCleaningPlans({
    int? floor,
    String? plan,
    int? bhk,
  }) async {
    try {
      final queryParams = <String, String>{};
      if (floor != null) queryParams['floor'] = floor.toString();
      if (plan != null) queryParams['plan'] = plan;
      if (bhk != null) queryParams['bhk'] = bhk.toString();

      final uri = Uri.parse('$baseUrl/cleaning').replace(queryParameters: queryParams);
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load cleaning plans');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<List<dynamic>> getAdditionalCleaningPlans({
    String? code,
    String? plan,
    int? floor,
  }) async {
    try {
      final queryParams = <String, String>{};
      if (code != null) queryParams['code'] = code;
      if (plan != null) queryParams['plan'] = plan;
      if (floor != null) queryParams['floor'] = floor.toString();

      final uri = Uri.parse('$baseUrl/additional-cleaning').replace(queryParameters: queryParams);
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to load additional cleaning plans');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  Future<Map<String, dynamic>> calculateCleaningTotal({
    required int floor,
    required String plan,
    required int bhk,
    List<String>? code,
  }) async {
    try {
      final queryParams = <String, String>{
        'floor': floor.toString(),
        'plan': plan,
        'bhk': bhk.toString(),
      };
      if (code != null && code.isNotEmpty) {
        queryParams['code'] = code.join(',');
      }

      print('=== Cleaning Service Request ===');
      print('Query Parameters:');
      print('floor: $floor');
      print('plan: $plan');
      print('bhk: $bhk');
      print('code: ${code?.join(',') ?? '[]'}');

      final uri = Uri.parse('$baseUrl/calculate-cleaning-total').replace(queryParameters: queryParams);
      final response = await http.get(uri);

      print('=== Cleaning Service Response ===');
      print('Status Code: ${response.statusCode}');
      print('Response Body: ${response.body}');

      if (response.statusCode == 200) {
        final result = json.decode(response.body);
        print('Processed Response:');
        print('Base Price: ${result['base_price']}');
        print('Total Price: ${result['total_price']}');
        print('Floor: ${result['floor']}');
        print('Plan: ${result['plan']}');
        print('BHK: ${result['bhk']}');
        print('Services: ${result['services']}');
        return result;
      } else {
        throw Exception('Failed to calculate cleaning total: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      print('=== Cleaning Service Error ===');
      print('Error: $e');
      throw Exception('Error: $e');
    }
  }
} 